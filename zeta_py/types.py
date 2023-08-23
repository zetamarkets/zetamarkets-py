from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import NamedTuple, Optional
from solders.hash import Hash


class Asset(Enum):
    SOL = 0
    BTC = 1
    ETH = 2
    APT = 3
    ARB = 4
    UNDEFINED = 5

    def to_index(self):
        return self.value

    def to_string(self):
        return self.name

    @staticmethod
    def all():
        return [a for a in Asset if a != Asset.UNDEFINED]

    def __str__(self) -> str:
        return self.name


class Network(Enum):
    LOCALNET = "localnet"
    DEVNET = "devnet"
    TESTNET = "testnet"
    MAINNET = "mainnet_beta"

    def __str__(self) -> str:
        return self.name


class OrderType(IntEnum):
    LIMIT = 0
    POSTONLY = 1
    FILLORKILL = 2
    IMMEDIATEORCANCEL = 3
    POSTONLYSLIDE = 4


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
    tif_options: TIFOptions = field(default_factory=TIFOptions)
    order_type: Optional[OrderType] = OrderType.LIMIT
    client_order_id: Optional[int] = 0
    tag: Optional[str] = "SDK"
    blockhash: Optional[Hash] = None
