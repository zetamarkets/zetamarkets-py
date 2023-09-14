from __future__ import annotations

import os
from dataclasses import dataclass

from anchorpy import Idl, Program, Provider, Wallet
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey

from zetamarkets_py import constants, pda
from zetamarkets_py.market import Market
from zetamarkets_py.solana_client.accounts.clock import Clock
from zetamarkets_py.types import Asset, Network
from zetamarkets_py.zeta_client.accounts.pricing import Pricing
from zetamarkets_py.zeta_client.accounts.state import State

idl_path = os.path.join(os.path.dirname(__file__), "idl/zeta.json")
with open(idl_path, "r") as f:
    idl = Idl.from_json(f.read())


# TODO: add logging e.g. logger = logging.getLogger("pyserum.market.Market")


@dataclass
class Exchange:
    # Initialize
    connection: AsyncClient
    program_id: Pubkey
    program: Program
    state: State
    pricing: Pricing
    markets: dict[Asset, Market] = None
    clock: Clock = None

    _state_address: Pubkey = None
    _pricing_address: Pubkey = None
    _serum_authority_address: Pubkey = None
    _mint_authority_address: Pubkey = None

    @classmethod
    async def load(
        cls,
        network: Network,
        connection: AsyncClient,
        assets: list[Asset] = Asset.all(),
    ) -> "Exchange":
        program_id = constants.ZETA_PID[network]
        provider = Provider(connection, Wallet.dummy())
        program = Program(idl, program_id, provider)

        # Accounts
        state_address = pda.get_state_address(program_id)
        state = await State.fetch(connection, state_address, connection.commitment)

        pricing_address = pda.get_pricing_address(program_id)
        pricing = await Pricing.fetch(connection, pricing_address, connection.commitment)

        # Addresses
        _serum_authority_address = pda.get_serum_authority_address(program_id)
        _mint_authority_address = pda.get_mint_authority_address(program_id)

        instance = cls(
            connection=connection,
            program_id=program_id,
            program=program,
            state=state,
            pricing=pricing,
            _state_address=state_address,
            _pricing_address=pricing_address,
            _serum_authority_address=_serum_authority_address,
            _mint_authority_address=_mint_authority_address,
        )

        instance.markets = {
            asset: await Market.load(network, connection, asset, pricing.markets[asset.to_index()]) for asset in assets
        }

        # Load Clock
        # instance.clock = await Clock.fetch(connection, connection.commitment)

        return instance

    @property
    def endpoint(self) -> str:
        return self.connection._provider.endpoint_uri

    @property
    def assets(self) -> list[Asset]:
        return list(self.markets.keys())

    # Priority Fees
    def toggle_auto_priority_fee(self):
        self._use_auto_priority_fee = not self._use_auto_priority_fee

    # TODO: add auto priority fee
    # TODO: add to solders
    # def update_auto_fee(self):
    #     account_list = []

    #     # Query the most written-to accounts
    #     # Note: getRecentPrioritizationFees() will account for global fees too if no one is writing to our accs
    #     for market in self.markets.values():
    #         account_list.append(market.address.perp_sync_queue_address)

    #     try:
    #         data = requests.post(
    #             self.endpoint,
    #             json={
    #                 "jsonrpc": "2.0",
    #                 "id": 1,
    #                 "method": "getRecentPrioritizationFees",
    #                 "params": [[account_list]],
    #             },
    #         )

    #         fees = sorted(
    #             [obj["prioritizationFee"] for obj in data.json()["result"]],
    #             key=lambda x: x["slot"],
    #             reverse=True,
    #         )[
    #             :20
    #         ]  # Grab the latest 20

    #         median = statistics.median(fees)
    #         self.priority_fee = min(median, self._auto_priority_fee_upper_limit)
    #         print(f"AutoUpdate priority fee. New fee = {self.priority_fee} microlamports per compute unit")
    #     except Exception as e:
    #         print(f"updateAutoFee failed {e}")
