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

    @classmethod
    def from_index(cls, index: int):
        members = list(Asset)
        return members[index]

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

    @classmethod
    def from_index(cls, index: int):
        members = list(OrderType)
        return members[index]

    def __str__(self) -> str:
        return self.name


class Side(Enum):
    """Side of the orderbook to trade."""

    Uninitialized = 0
    """"""
    Bid = 1
    """"""
    Ask = 2
    """"""

    def to_program_type(self) -> side.SideKind:
        return side.from_decoded({self.name: self.value})

    @classmethod
    def from_index(cls, index: int):
        members = list(Side)
        return members[index]

    def __str__(self) -> str:
        return self.name


class SelfTradeBehavior(Enum):
    DecrementTake = 0
    CancelProvide = 1
    AbortTransaction = 2

    def __str__(self) -> str:
        return self.name


class OrderCompleteType(Enum):
    Cancel = 0
    Fill = 1
    Booted = 2

    @classmethod
    def from_index(cls, index: int):
        members = list(OrderCompleteType)
        return members[index]

    def __str__(self) -> str:
        return self.name


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
