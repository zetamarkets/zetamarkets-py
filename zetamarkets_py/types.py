from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Optional

from solders.hash import Hash
from solders.pubkey import Pubkey

from zetamarkets_py.zeta_client.types import asset, order_type, side


class Asset(Enum):
    SOL = "SOL"
    BTC = "BTC"
    ETH = "ETH"
    APT = "APT"
    ARB = "ARB"

    def to_index(self):
        members = list(self.__class__.__members__.values())
        return members.index(self)

    def to_string(self):
        return self.name

    def to_program_type(self):
        return asset.from_decoded({self.name: self.to_index()})

    @staticmethod
    def all():
        return list(Asset)

    def __str__(self) -> str:
        return self.name


class Network(Enum):
    DEVNET = "devnet"
    TESTNET = "testnet"
    MAINNET = "mainnet_beta"

    def __str__(self) -> str:
        return self.name


class OrderType(IntEnum):
    Limit = 0
    PostOnly = 1
    FillOrKill = 2
    ImmediateOrCancel = 3
    PostOnlySlide = 4

    def to_program_type(self):
        return order_type.from_decoded({self.name: self.value})


class Side(Enum):
    """Side of the orderbook to trade."""

    Bid = 0
    """"""
    Ask = 1
    """"""

    def to_program_type(self) -> side.SideKind:
        return side.from_decoded({self.name.title(): self.value})


class SelfTradeBehavior(Enum):
    DecrementTake = 0
    CancelProvide = 1
    AbortTransaction = 2


@dataclass
class Position:
    size: float
    cost_of_trades: float


@dataclass
class TIFOptions:
    expiry_offset: Optional[int] = None
    expiry_ts: Optional[int] = None


@dataclass
class OrderOptions:
    expiry_ts: Optional[int] = None
    client_order_id: Optional[int] = None
    blockhash: Optional[Hash] = None
    order_type: OrderType = OrderType.Limit
    tag: str = "SDK"


@dataclass
class OrderInfo:
    price: float
    size: float


@dataclass
class Order:
    order_id: int
    client_id: int
    open_order_address: Pubkey
    open_order_slot: int
    fee_tier: int
    info: OrderInfo
    side: Side
    tif_offset: int


@dataclass
class FilledOrder:
    order_id: int
    side: Side
    price: float
    size: float
    fee_cost: int


@dataclass
class OrderArgs:
    price: float
    size: float
    side: Side
    order_opts: OrderOptions = field(default_factory=OrderOptions)
