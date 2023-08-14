from __future__ import annotations

import asyncio
import statistics
from typing import Any, Callable, Coroutine, Dict, List, Optional
from anchorpy import Idl, Program, Provider, Wallet
from solders.pubkey import Pubkey
from solana.rpc.api import Commitment
from solana.rpc.async_api import AsyncClient
from solana.utils.cluster import Cluster
import os

# from zeta_py.subexchange import SubExchange
from solders.sysvar import CLOCK
import requests

# from pyserum.market import AsyncMarket as SerumMarket
# from solders.rpc.responses import GetAccountInfoResp
from solana.rpc.websocket_api import connect


from zeta_py import types, assets, constants, utils, pda
from zeta_py.constants import Asset
from solana.rpc.types import TxOpts
from zeta_py.events import EventType
from zeta_py.market import Market
from zeta_py.program_account import ProgramAccount

# from zeta_py.market import Market

from zeta_py.zeta_client.accounts.perp_sync_queue import PerpSyncQueue
from zeta_py.zeta_client.accounts.pricing import Pricing
from zeta_py.zeta_client.accounts.state import State

# import zeta_client

idl_path = os.path.join(os.path.dirname(__file__), "idl/zeta.json")
with open(idl_path, "r") as f:
    idl = Idl.from_json(f.read())


# TODO: change to use attrs/cattrs


# Change from instance to singleton?
# https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
class Exchange:
    class ExchangeAccounts:
        @property
        def is_loaded(self) -> bool:
            return self._is_loaded

        def __init__(
            self, state: ProgramAccount[State], pricing: ProgramAccount[Pricing]
        ) -> None:
            self.state = state
            self.pricing = pricing
            self._is_loaded = False

        async def load(self, connection: AsyncClient):
            if self.is_loaded:
                raise Exception("Exchange already loaded")
            await asyncio.gather(
                self.state.load(connection), self.pricing.load(connection)
            )
            self._is_loaded = True

    def __init__(
        self,
        load_config: types.LoadExchangeConfig,
        wallet: Wallet = Wallet.dummy(),
    ):
        self._is_loaded = False

        # Initialize
        provider = Provider(
            load_config.connection,
            wallet,
            load_config.opts
            or utils.commitment_config(load_config.connection.commitment),
        )
        self._opts = load_config.opts
        self._network = load_config.network
        self._program = Program(idl, constants.ZETA_PID[load_config.network], provider)

        # Accounts
        state = ProgramAccount[State](pda.get_state(self.program.program_id)[0], State)
        pricing = ProgramAccount[Pricing](
            pda.get_pricing(self.program.program_id)[0], Pricing
        )
        self._accounts = self.ExchangeAccounts(state, pricing)

        self._markets = {asset: Market(asset, self) for asset in assets.all_assets()}

        # Clock
        self._clock_timestamp: int = None
        self._clock_slot: int = None
        self._clock_subscription_id: int = None
        self._poll_interval: int = None
        self._last_poll_timestamp: int = None

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    @property
    def program(self) -> Program:
        return self._program

    @property
    def network(self) -> Cluster:
        return self._network

    @property
    def connection(self) -> AsyncClient:
        return self.program.provider.connection

    @property
    def opts(self) -> TxOpts:
        return self._opts

    @property
    def accounts(self) -> ExchangeAccounts:
        return self._accounts

    @property
    def markets(self) -> Dict[Asset, Market]:
        return self._markets

    @markets.setter
    def markets(self, markets: Dict[Asset, Market]):
        self._markets = markets

    @property
    def assets(self) -> List[Asset]:
        return list(self.markets.keys())

    @property
    def risk_calculator(self) -> RiskCalculator:
        return self._risk_calculator

    # Stores the latest timestamp received by websocket subscription
    # to the system clock account.
    @property
    def clock_timestamp(self) -> int:
        return self._clock_timestamp

    # Stores the latest clock slot from clock subscription.
    @property
    def clock_slot(self) -> int:
        return self._clock_slot

    # @param interval
    # How often to poll zeta group and state in seconds.
    @property
    def poll_interval(self) -> int:
        return self._poll_interval

    @poll_interval.setter
    def poll_interval(self, interval: int):
        if interval < 0:
            raise Exception("Invalid polling interval")
        self._poll_interval = interval

    # Priority Fees
    def toggle_auto_priority_fee(self):
        self._use_auto_priority_fee = not self._use_auto_priority_fee

    @property
    def priority_fee(self) -> int:
        return self._priority_fee

    @priority_fee.setter
    def priority_fee(self, micro_lamports_per_cu: int):
        self._priority_fee = micro_lamports_per_cu

    @property
    def auto_priority_fee_upper_limit(self) -> int:
        return self._auto_priority_fee_upper_limit

    @auto_priority_fee_upper_limit.setter
    def priority_fee(self, micro_lamports_per_cu: int):
        self._auto_priority_fee_upper_limit = micro_lamports_per_cu

    @property
    def blockhash_commitment(self) -> int:
        return self._blockhash_commitment

    @blockhash_commitment.setter
    def priority_fee(self, commitment: Commitment):
        self._blockhash_commitment = commitment

    async def load(
        self,
        load_config: types.LoadExchangeConfig,
        callback: Optional[Callable[[Asset, EventType, Any], None]] = None,
    ) -> None:
        if self.is_loaded:
            raise Exception("Exchange already loaded")

        # if loadConfig.network == "localnet" and loadConfig.loadFromStore:
        #     raise Exception("Cannot load localnet from store")

        # TODO add risk
        #   self._riskCalculator = RiskCalculator(self.assets)

        self._last_poll_timestamp = 0
        # Load Program accounts
        await self.accounts.load(self.connection)

        # Load Markets TODO make async
        for market in self.markets.values():
            await market.load()

        # Load Clock
        await self.load_clock_data()

        # self.subscribe_clock(clock_data, callback)
        self.accounts.pricing.subscribe()

        # self.update_exchange_state()

        self._is_loaded = True

    # Factory method
    @classmethod
    async def create(
        cls,
        load_config: types.LoadExchangeConfig,
        wallet: Wallet,
        callback: Optional[Callable[[Asset, EventType, Any], None]] = None,
    ) -> "Exchange":
        obj = cls(load_config, wallet)
        await obj.load(load_config, callback)

    def update_auto_fee(self):
        account_list = []

        # Query the most written-to accounts
        # Note: getRecentPrioritizationFees() will account for global fees too if no one is writing to our accs
        for market in self.markets.values():
            account_list.append(market.address.perp_sync_queue_address)

        try:
            data = requests.post(
                self.provider.connection._provider.endpoint_uri,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getRecentPrioritizationFees",
                    "params": [[account_list]],
                },
            )

            fees = sorted(
                [obj["prioritizationFee"] for obj in data.json()["result"]],
                key=lambda x: x["slot"],
                reverse=True,
            )[
                :20
            ]  # Grab the latest 20

            median = statistics.median(fees)
            self.priority_fee = min(median, self._auto_priority_fee_upper_limit)
            print(
                f"AutoUpdate priority fee. New fee = {self.priority_fee} microlamports per compute unit"
            )
        except Exception as e:
            print(f"updateAutoFee failed {e}")

    async def load_clock_data(self) -> None:
        clock = await self.connection.get_account_info_json_parsed(CLOCK)
        self._clock_timestamp = clock.value.data.parsed["info"]["unixTimestamp"]
        self._clock_slot = clock.value.data.parsed["info"]["slot"]

    # def subscribe_clock(
    #     self,
    #     clock_data: types.ClockData,
    #     callback: Optional[Callable[[Asset, EventType, Any], None]] = None,
    # ) -> None:
    #     if self._clock_subscription_id is not None:
    #         raise Exception("Clock already subscribed to.")
    #     self._clock_subscription_id = self.provider.connection.onAccountChange(
    #         CLOCK,
    #         lambda account_info, context: self.set_clock_data(
    #             utils.get_clock_data(account_info)
    #         ),
    #         self.provider.connection.commitment,
    #     )
    #     self.setClockData(clock_data)

    # async def subscribe_pricing(self) -> None:
    #     ws_endpoint = utils.cluster_endpoint(self.network, ws=True)
    #     async with connect(ws_endpoint) as ws:
    #         await ws.account_subscribe(
    #             self.accounts.pricing.address,
    #             commitment="confirmed",
    #             encoding="base64",
    #         )
    #         first_resp = await ws.recv()
    #         subscription_id = first_resp[0].result
    #         while True:
    #             msg = await ws.recv()
    #             price_account = Pricing.decode(msg[0].result.value.data)
    #             self._accounts.pricing.account = price_account
    #         await ws.account_subscribe(subscription_id)

    def add_program_subscription_id(self, id: int):
        self._program_subscription_ids.append(id)

    # async def update_exchange_state(self):
    #     await self.update_state()
    #     await self.update_zeta_pricing()

    # async def update_state(self):
    #     self._state = await State.fetch(self.addresses.state_address)

    # async def update_zeta_pricing(self):
    #     self._pricing = await Pricing.fetch(self.addresses.pricing_address)
