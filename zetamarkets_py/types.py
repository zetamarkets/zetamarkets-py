from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Optional

from solders.hash import Hash
from solders.pubkey import Pubkey

from zetamarkets_py.zeta_client.types import asset, order_type, side


class Asset(Enum):
    """Enum class for different types of assets."""

    SOL = "SOL"
    BTC = "BTC"
    ETH = "ETH"
    APT = "APT"
    ARB = "ARB"
    BNB = "BNB"
    PYTH = "PYTH"
    TIA = "TIA"
    JTO = "JTO"
    ONEMBONK = "ONEMBONK"
    SEI = "SEI"
    JUP = "JUP"
    DYM = "DYM"

    def to_index(self):
        """Converts the asset to its corresponding index."""
        members = list(self.__class__.__members__.values())
        return members.index(self)

    @classmethod
    def from_index(cls, index: int):
        """Returns the asset corresponding to the given index."""
        members = list(Asset)
        return members[index]

    def to_program_type(self):
        """Converts the asset to its corresponding program type."""
        return asset.from_decoded({self.name: self.to_index()})

    @staticmethod
    def all():
        """Returns a list of all assets."""
        return list(Asset)

    def __str__(self) -> str:
        """Returns the name of the asset."""
        return self.name


class Network(Enum):
    """Enum class for different types of networks."""

    DEVNET = "devnet"
    TESTNET = "testnet"
    MAINNET = "mainnet_beta"

    def __str__(self) -> str:
        """Returns the name of the network."""
        return self.name


class OrderType(IntEnum):
    """Enum class for different types of orders."""

    Limit = 0
    PostOnly = 1
    FillOrKill = 2
    ImmediateOrCancel = 3
    PostOnlySlide = 4

    def to_program_type(self):
        """Converts the order type to its corresponding program type."""
        return order_type.from_decoded({self.name: self.value})

    @classmethod
    def from_index(cls, index: int):
        """Returns the order type corresponding to the given index."""
        members = list(OrderType)
        return members[index]

    def __str__(self) -> str:
        """Returns the name of the order type."""
        return self.name


class Side(Enum):
    """Enum class for different sides of the orderbook to trade."""

    Uninitialized = 0
    Bid = 1
    Ask = 2

    def to_program_type(self) -> side.SideKind:
        """Converts the side to its corresponding program type."""
        return side.from_decoded({self.name: self.value})

    @classmethod
    def from_index(cls, index: int):
        """Returns the side corresponding to the given index."""
        members = list(Side)
        return members[index]

    def __str__(self) -> str:
        """Returns the name of the side."""
        return self.name


class SelfTradeBehavior(Enum):
    """Enum class for different types of self trade behaviors."""

    DecrementTake = 0
    CancelProvide = 1
    AbortTransaction = 2

    def __str__(self) -> str:
        """Returns the name of the self trade behavior."""
        return self.name


class OrderCompleteType(Enum):
    """Enum class for different types of order completion statuses."""

    Cancel = 0
    Fill = 1
    Booted = 2

    @classmethod
    def from_index(cls, index: int):
        """Returns the order completion status corresponding to the given index."""
        members = list(OrderCompleteType)
        return members[index]

    def __str__(self) -> str:
        """Returns the name of the order completion status."""
        return self.name


@dataclass
class TIFOptions:
    """Data class for Time in Force options."""

    expiry_offset: Optional[int] = None
    expiry_ts: Optional[int] = None


@dataclass
class OrderOptions:
    """Data class for order options."""

    expiry_ts: Optional[int] = None
    client_order_id: Optional[int] = None
    blockhash: Optional[Hash] = None
    order_type: OrderType = OrderType.Limit
    tag: str = "SDK"


@dataclass
class OrderInfo:
    """Data class for order information."""

    price: float
    size: float


@dataclass
class Order:
    """Data class for order details."""

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
    """Data class for filled order details."""

    order_id: int
    side: Side
    price: float
    size: float
    fee_cost: int


@dataclass
class OrderArgs:
    """Data class for order arguments."""

    price: float
    size: float
    side: Side
    order_opts: OrderOptions = field(default_factory=OrderOptions)
