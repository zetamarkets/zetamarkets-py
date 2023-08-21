from enum import Enum
from typing import List, NamedTuple, TypedDict
from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solana.utils.cluster import Cluster


class Side(Enum):
    BID = 0
    ASK = 1


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


class LoadExchangeConfig(NamedTuple):
    network: Cluster
    connection: AsyncClient
    assets: List[Asset]
    opts: TxOpts
    load_from_store: bool
