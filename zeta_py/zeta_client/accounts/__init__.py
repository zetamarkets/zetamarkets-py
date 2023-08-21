from abc import ABC, abstractmethod
import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from zeta_py.zeta_client.program_id import PROGRAM_ID


@dataclass
class AnchorpyAccount(ABC):
    discriminator: typing.ClassVar = None
    layout: typing.ClassVar

    # @classmethod
    # @abstractmethod
    # async def fetch(
    #     cls,
    #     connection: AsyncClient,
    #     address: Pubkey,
    #     commitment: typing.Optional[Commitment] = None,
    #     program_id: Pubkey = PROGRAM_ID,
    # ) -> typing.Optional["AnchorpyAccount"]:
    #     pass

    # @classmethod
    # @abstractmethod
    # async def fetch_multiple(
    #     cls,
    #     conn: AsyncClient,
    #     addresses: list[Pubkey],
    #     commitment: typing.Optional[Commitment] = None,
    #     program_id: Pubkey = PROGRAM_ID,
    # ) -> typing.List[typing.Optional["AnchorpyAccount"]]:
    #     pass

    @classmethod
    @abstractmethod
    def decode(cls, data: bytes) -> "AnchorpyAccount":
        pass


from httpx import AsyncClient
from .pricing import Pricing, PricingJSON
from .greeks import Greeks, GreeksJSON
from .market_indexes import MarketIndexes, MarketIndexesJSON
from .open_orders_map import OpenOrdersMap, OpenOrdersMapJSON
from .cross_open_orders_map import CrossOpenOrdersMap, CrossOpenOrdersMapJSON
from .state import State, StateJSON
from .underlying import Underlying, UnderlyingJSON
from .settlement_account import SettlementAccount, SettlementAccountJSON
from .perp_sync_queue import PerpSyncQueue, PerpSyncQueueJSON
from .zeta_group import ZetaGroup, ZetaGroupJSON
from .market_node import MarketNode, MarketNodeJSON
from .spread_account import SpreadAccount, SpreadAccountJSON
from .cross_margin_account_manager import (
    CrossMarginAccountManager,
    CrossMarginAccountManagerJSON,
)
from .cross_margin_account import CrossMarginAccount, CrossMarginAccountJSON
from .margin_account import MarginAccount, MarginAccountJSON
from .socialized_loss_account import SocializedLossAccount, SocializedLossAccountJSON
from .whitelist_deposit_account import (
    WhitelistDepositAccount,
    WhitelistDepositAccountJSON,
)
from .whitelist_insurance_account import (
    WhitelistInsuranceAccount,
    WhitelistInsuranceAccountJSON,
)
from .insurance_deposit_account import (
    InsuranceDepositAccount,
    InsuranceDepositAccountJSON,
)
from .whitelist_trading_fees_account import (
    WhitelistTradingFeesAccount,
    WhitelistTradingFeesAccountJSON,
)
from .referrer_account import ReferrerAccount, ReferrerAccountJSON
from .referral_account import ReferralAccount, ReferralAccountJSON
from .referrer_alias import ReferrerAlias, ReferrerAliasJSON
