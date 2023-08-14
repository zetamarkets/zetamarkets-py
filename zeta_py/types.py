from typing import NamedTuple, TypedDict
from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solana.utils.cluster import Cluster


class LoadExchangeConfig(NamedTuple):
    network: Cluster
    connection: AsyncClient
    opts: TxOpts
    throttle_ms: int
    load_from_store: bool
