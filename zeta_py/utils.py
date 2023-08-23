import re

from solana.utils.cluster import cluster_api_url

from zeta_py import constants
from zeta_py.types import Network


def convert_fixed_int_to_decimal(amount: int) -> float:
    return amount / 10**constants.PLATFORM_PRECISION


def convert_decimal_to_fixed_int(amount: float) -> int:
    return int((amount * 10**constants.PLATFORM_PRECISION / constants.TICK_SIZE) * constants.TICK_SIZE)


def convert_fixed_lot_to_decimal(amount: int) -> float:
    return amount / 10**constants.POSITION_PRECISION


def convert_decimal_to_fixed_lot(amount: float) -> int:
    return int(amount * 10**constants.POSITION_PRECISION)


def cluster_endpoint(network: Network, tls: bool = True, ws: bool = False) -> str:
    """Retrieve the RPC API URL for the specified cluster.

    :param cluster: The name of the cluster to use.
    :param tls: If True, use https. Defaults to True.
    """
    endpoint = cluster_api_url(network.value, tls=tls)
    if ws:
        return re.sub(r"^http", "ws", endpoint)
    else:
        return endpoint
