from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Optional

from solders.hash import Hash
from solders.pubkey import Pubkey

from zetamarkets_py.zeta_client.types import asset, order_type, side, self_trade_behavior_zeta


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
    STRK = "STRK"
    WIF = "WIF"
    RNDR = "RNDR"
    TNSR = "TNSR"
    POPCAT = "POPCAT"

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


class SelfTradeBehaviorZeta(IntEnum):
    """Enum class for different types of orders."""

    CancelProvide = 0
    AbortTransaction = 1

    def to_program_type(self):
        """Converts the order type to its corresponding program type."""
        return self_trade_behavior_zeta.from_decoded({self.name: self.value})

    @classmethod
    def from_index(cls, index: int):
        """Returns the order type corresponding to the given index."""
        members = list(SelfTradeBehaviorZeta)
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
    self_trade_behavior: Optional[SelfTradeBehaviorZeta] = None


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


@dataclass
class MultiOrderArgs:
    """Data class for multi order arguments."""

    price: float
    size: float
    client_order_id: Optional[int] = None
    expiry_ts: Optional[int] = None


class AnchorDecimal:
    flags: int
    hi: int
    lo: int
    mid: int


class Decimal:
    def __init__(self, flags: int, hi: int, lo: int, mid: int):
        self._flags = flags
        self._hi = hi
        self._lo = lo
        self._mid = mid
        self.SCALE_MASK = 0x00FF0000
        self.SCALE_SHIFT = 16
        self.SIGN_MASK = 0x80000000

    @classmethod
    def from_anchor_decimal(cls, decimal: AnchorDecimal):
        return cls(decimal.flags, decimal.hi, decimal.lo, decimal.mid)

    def scale(self) -> int:
        return (self._flags & self.SCALE_MASK) >> self.SCALE_SHIFT

    def is_sign_negative(self) -> bool:
        return (self._flags & self.SIGN_MASK) != 0

    def is_sign_positive(self) -> bool:
        return (self._flags & self.SIGN_MASK) == 0

    def to_float(self):

        scale = self.scale()
        if scale == 0:
            raise ValueError("Scale 0 is not handled.")

        bytes_ = bytes(
            [
                (self._hi >> 24) & 0xFF,
                (self._hi >> 16) & 0xFF,
                (self._hi >> 8) & 0xFF,
                self._hi & 0xFF,
                (self._mid >> 24) & 0xFF,
                (self._mid >> 16) & 0xFF,
                (self._mid >> 8) & 0xFF,
                self._mid & 0xFF,
                (self._lo >> 24) & 0xFF,
                (self._lo >> 16) & 0xFF,
                (self._lo >> 8) & 0xFF,
                self._lo & 0xFF,
            ]
        )

        return (-1 * int.from_bytes(bytes_, "big") if self.is_sign_negative() else int.from_bytes(bytes_, "big")) / (
            10**scale
        )

    def is_unset(self) -> bool:
        return self._hi == 0 and self._mid == 0 and self._lo == 0 and self._flags == 0
