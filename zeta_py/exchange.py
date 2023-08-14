from __future__ import annotations

import asyncio
import statistics
from typing import Any, Callable, Coroutine, Dict, List, Optional
from anchorpy import Idl, Program, Provider, Wallet
from solders.pubkey import Pubkey
from solana.rpc.api import Commitment
from solana.rpc.async_api import AsyncClient
from solana.utils.cluster import Cluster, cluster_api_url
import os
from zeta_py.subexchange import SubExchange
from solders.sysvar import CLOCK
import requests
from pyserum.market import AsyncMarket as SerumMarket
from solders.rpc.responses import GetAccountInfoResp

from zeta_py import types, assets, constants, utils
from zeta_py.constants import Asset
from solana.rpc.types import TxOpts
from zeta_py.events import EventType
from zeta_py.market import Market, ZetaGroupMarkets

from zeta_py.zeta_client.accounts.perp_sync_queue import PerpSyncQueue
from zeta_py.zeta_client.accounts.pricing import Pricing
from zeta_py.zeta_client.accounts.state import State

# from zeta_client.accounts import

idl_path = os.path.join(os.path.dirname(__file__), "idl/zeta.json")
with open(idl_path, "rb") as f:
    idl = Idl.from_bytes(f.read())
print(idl)


# Change from instance to singleton?
# https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
class Exchange:
    def __init__(
        self,
        load_config: types.LoadExchangeConfig,
        wallet: Wallet,
    ):
        # self._program_id = load_config.
        # self._provider = provider
        # self._opts = opts
        # self._assets = None
        # self._oracle = None
        # self._risk_calculator = None
        # self._is_setup = False
        # self._is_initialized = False
        # self._state = None
        # self._pricing = None
        # self._network = None
        # self._program = None
        # self._serum_authority = None
        # self._mint_authority = None
        # self._usdc_mint_address = None
        # self._sub_exchanges = None

        self.sub_exchanges = {}
        self._is_loaded = False

        # Initialize #
        self._assets = assets.all_assets()
        self._provider = Provider(
            load_config.connection,
            wallet,
            load_config.opts
            or utils.commitment_config(load_config.connection.commitment),
        )
        self._opts = load_config.opts
        self._network = load_config.network
        self._program = Program(
            idl, constants.ZETA_PID[load_config.network], self._provider
        )

        for asset in self._assets:
            self.add_sub_exchange(asset, SubExchange(asset, self))

        self._combined_vault_address = utils.get_combined_vault(self.program_id)[0]
        self._combined_insurance_vault_address = (
            utils.get_zeta_combined_insurance_vault(self.program_id)[0]
        )
        self._combined_socialized_loss_account_address = (
            utils.get_combined_socialized_loss_account(self.program_id)[0]
        )

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    @property
    def state(self) -> State:
        return self._state

    @property
    def pricing(self) -> Pricing:
        return self._pricing

    @property
    def network(self) -> Cluster:
        return self._network

    @property
    def program(self) -> Program:
        return self._program

    @property
    def program_id(self) -> Pubkey:
        return self._program_id

    @property
    def provider(self) -> Provider:
        return self._provider

    @property
    def connection(self) -> AsyncClient:
        return self._provider.connection

    @property
    def usdc_mint_address(self) -> Pubkey:
        return self._usdc_mint_address

    @property
    def opts(self) -> TxOpts:
        return self._opts

    @property
    def sub_exchanges(self) -> Dict[Asset, SubExchange]:
        return self._sub_exchanges

    @sub_exchanges.setter
    def sub_exchanges(self, sub_exchanges: Dict[Asset, SubExchange]):
        self._sub_exchanges = sub_exchanges

    @property
    def assets(self) -> List[Asset]:
        return self._assets

    @property
    def oracle(self) -> Oracle:
        return self._oracle

    @property
    def risk_calculator(self) -> RiskCalculator:
        return self._risk_calculator

    @property
    def serum_authority(self) -> Pubkey:
        return self._serum_authority

    @property
    def mint_authority(self) -> Pubkey:
        return self._mint_authority

    # # Public key for treasury wallet.
    # @property
    # def treasury_wallet_address(self) -> Pubkey:
    #     return self._treasury_wallet_address

    # _treasury_wallet_address: Pubkey = None

    # # Public key for referral rewards wallet.
    # @property
    # def referrals_rewards_wallet_address(self) -> Pubkey:
    #     return self._referrals_rewards_wallet_address

    # _referrals_rewards_wallet_address: Pubkey = None

    # # Public key for combined insurance fund.
    # @property
    # def combinedInsuranceVaultAddress(self) -> Pubkey:
    #     return self._combinedInsuranceVaultAddress

    # _combinedInsuranceVaultAddress: Pubkey = None

    # # Public key for combined deposit vault.
    # @property
    # def combinedVaultAddress(self) -> Pubkey:
    #     return self._combinedVaultAddress

    # _combinedVaultAddress: Pubkey = None

    # # Public key for combined socialized loss account.
    # @property
    # def combinedSocializedLossAccountAddress(self) -> Pubkey:
    #     return self._combinedSocializedLossAccountAddress

    # _combinedSocializedLossAccountAddress: Pubkey = None

    # Stores the latest timestamp received by websocket subscription
    # to the system clock account.
    @property
    def clock_timestamp(self) -> int:
        return self._clock_timestamp

    _clock_timestamp: int = None

    # Stores the latest clock slot from clock subscription.
    @property
    def clock_slot(self) -> int:
        return self._clock_slot

    _clock_slot: int = None

    # Websocket subscription id for clock.
    _clock_subscription_id: int = None

    # @param interval   How often to poll zeta group and state in seconds.
    @property
    def poll_interval(self) -> int:
        return self._poll_interval

    @poll_interval.setter
    def poll_interval(self, interval: int):
        if interval < 0:
            raise Exception("Invalid polling interval")
        self._poll_interval = interval

    _poll_interval: int = None
    _last_poll_timestamp: int = None

    def zeta_group_pubkey_to_asset(self, key: Pubkey) -> Asset:
        return self._zeta_group_pubkey_to_asset.get(key)

    def toggle_auto_priority_fee(self):
        self._use_auto_priority_fee = not self._use_auto_priority_fee

    def update_priority_fee(self, micro_lamports_per_cu: int):
        self._priority_fee = micro_lamports_per_cu

    def update_auto_priority_fee_upper_limit(self, micro_lamports_per_cu: int):
        self._auto_priority_fee_upper_limit = micro_lamports_per_cu

    def update_blockhash_commitment(self, commitment: Commitment):
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

        # Load variables from state.
        self._mint_authority = utils.get_mint_authority(self.program_id)[0]
        self._state_address = utils.get_state(self.program_id)[0]
        self._pricing_address = utils.get_pricing(self.program_id)[0]
        self._serum_authority = utils.get_serum_authority(self.program_id)[0]
        self._usdc_mint_address = constants.USDC_MINT_ADDRESS[load_config.network]
        self._treasury_wallet_address = utils.get_zeta_treasury_wallet(
            self.program_id, self._usdc_mint_address
        )[0]
        self._referrals_rewards_wallet_address = (
            utils.get_zeta_referrals_rewards_wallet(
                self.program_id, self._usdc_mint_address
            )[0]
        )

        self._last_poll_timestamp = 0
        await self.update_zeta_pricing()
        # TODO add oracle
        #   self._oracle = Oracle(self.network, self.provider.connection)

        sub_exchange_to_fetch_addrs: List[Pubkey] = (
            self.assets.map(lambda a: self.get_sub_exchange(a))
            .map(lambda se: se.perp_sync_queue_address)
            .append(CLOCK)
        )

        acc_fetch_promises: List[
            Coroutine[Any, Any, GetAccountInfoResp]
        ] = sub_exchange_to_fetch_addrs.map(
            lambda addr: self.provider.connection.get_account_info(addr)
        )
        all_promises: List[Coroutine[Any, Any, List[Any]]] = acc_fetch_promises.append(
            self.subscribe_oracle(self.assets, callback)
        )

        acc_fetches = (await asyncio.gather(*all_promises)).slice(
            0, assets.all_assets().length
        )

        perp_sync_queue_accs: List[PerpSyncQueue] = []
        for i in range(acc_fetches.length - 1):
            perp_sync_queue_accs.append(
                self.program.account.perp_sync_queue.coder.accounts.decode(
                    types.ProgramAccountType.PerpSyncQueue, acc_fetches[i].data
                )
            )

        clock_data = utils.get_clock_data(acc_fetches.at(-1))
        self.subscribe_clock(clock_data, callback)
        self.subscribe_pricing(callback)

        await asyncio.gather(
            *[
                asyncio.create_task(
                    self.get_sub_exchange(asset).load(
                        asset,
                        self.opts,
                        [perp_sync_queue_accs[i]],
                        load_config.load_from_store,
                        callback,
                    )
                )
                for i, asset in enumerate(self.assets)
            ]
        )
        for se in self.get_all_sub_exchanges():
            self.zeta_group_pubkey_to_asset[se.zeta_group_address] = se.asset

        self.update_exchange_state()

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

    def add_sub_exchange(self, asset: str, sub_exchange: SubExchange):
        self.sub_exchanges[asset] = sub_exchange

    def get_sub_exchange(self, asset: str) -> SubExchange:
        try:
            return self.sub_exchanges[asset]
        except KeyError:
            raise Exception(
                f"Failed to get subExchange for asset={asset}, have you called Exchange.load()?"
            )

    def get_all_sub_exchanges(self) -> List[SubExchange]:
        return list(self.sub_exchanges.values())

    def update_auto_fee(self):
        account_list = []

        # Query the most written-to accounts
        # Note: getRecentPrioritizationFees() will account for global fees too if no one is writing to our accs
        for asset in self.assets:
            sub = self.get_sub_exchange(asset)
            account_list.append(sub.perp_sync_queue_address)
            account_list.append(sub.greeks_address)

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
            self._priority_fee = min(median, self._auto_priority_fee_upper_limit)
            print(
                f"AutoUpdate priority fee. New fee = {self._priority_fee} microlamports per compute unit"
            )
        except Exception as e:
            print(f"updateAutoFee failed {e}")

    async def subscribe_oracle(
        self,
        assets: List[Asset],
        callback: Optional[Callable[[Asset, EventType, Any], None]] = None,
    ) -> List[Any]:
        return await self._oracle.subscribe_price_feeds(
            assets,
            lambda asset, price: (
                self._risk_calculator.update_margin_requirements(asset)
                if self.is_initialized
                else None
            )
            if callback is None
            else callback(asset, EventType.ORACLE, price),
        )

    def set_clock_data(self, data: types.ClockData) -> None:
        self._clock_timestamp = data.timestamp
        self._clock_slot = data.slot

    def subscribe_clock(
        self,
        clock_data: types.ClockData,
        callback: Optional[Callable[[Asset, EventType, Any], None]] = None,
    ) -> None:
        if self._clock_subscription_id is not None:
            raise Exception("Clock already subscribed to.")
        self._clock_subscription_id = self.provider.connection.onAccountChange(
            CLOCK,
            lambda account_info, context: self.set_clock_data(
                utils.get_clock_data(account_info)
            ),
            self.provider.connection.commitment,
        )
        self.setClockData(clock_data)

    def add_program_subscription_id(self, id: int):
        self._program_subscription_ids.append(id)

    async def update_exchange_state(self):
        await self.update_state()
        await self.update_zeta_pricing()
        await asyncio.gather(
            *[
                self.get_zeta_group_markets(asset).update_expiry_series()
                for asset in self.assets
            ]
        )

    async def update_state(self):
        self._state = await self.program.account.state.fetch(self.state_address)

    def update_zeta_pricing(self):
        self._pricing = self.program.account.pricing[self.pricing_address]

    # TODO: figure out account subscriptions
    async def subscribe_pricing(self, callback: Optional[Callable] = None) -> Any:
        event_emitter = self.program.account["pricing"].subscribe(
            self._pricing_address,
            self.provider.connection.commitment,
        )

        async def callback_wrapper(pricing: Any) -> None:
            self._pricing = pricing
            if callback is not None:
                callback

    def subscribe_perp(self, asset: Asset):
        self.get_sub_exchange(asset).markets.subscribe_perp()

    def unsubscribe_perp(self, asset: Asset):
        self.get_sub_exchange(asset).markets.unsubscribe_perp()

    async def update_orderbook(self, asset: Asset):
        return await self.get_perp_market(asset).update_orderbook()

    async def update_all_orderbooks(self, live: bool = True):
        """
        Get the orderbook for all markets, and update the market objects
        """
        live_markets = [self.get_perp_market(asset) for asset in self.assets]

        live_markets_slices = [
            live_markets[i : i + constants.MAX_MARKETS_TO_FETCH]
            for i in range(0, len(live_markets), constants.MAX_MARKETS_TO_FETCH)
        ]

        # TODO: finish
        for live_markets in live_markets_slices:
            for market in live_markets:
                pass

    def get_zeta_group_markets(self, asset: Asset) -> ZetaGroupMarkets:
        return self.get_sub_exchange(asset).markets

    def get_perp_market(self, asset: Asset) -> Market:
        return self.get_sub_exchange(asset).markets.perp_market

    def get_markets_by_expiry_index(self, asset: Asset, index: int) -> list[Market]:
        return self.get_sub_exchange(asset).markets.get_markets_by_expiry_index(index)

    def get_zeta_group_address(self, asset: Asset) -> Pubkey:
        return self.get_sub_exchange(asset).zeta_group_address

    def get_perp_sync_queue(self, asset: Asset) -> PerpSyncQueue:
        return self.get_sub_exchange(asset).perp_sync_queue

    def get_orderbook(self, asset: Asset) -> types.DepthOrderbook:
        return self.get_perp_market(asset).orderbook

    def get_mark_price(self, asset: Asset) -> float:
        return self.get_sub_exchange(asset).get_mark_price()

    def get_insurance_vault_address(self) -> Pubkey:
        return self._combined_insurance_vault_address

    def get_vault_address(self) -> Pubkey:
        return self._combined_vault_address

    def get_socialized_loss_account_address(self) -> Pubkey:
        return self._combined_socialized_loss_account_address
