import re

from solana.utils.cluster import cluster_api_url

from zetamarkets_py import constants
from zetamarkets_py.types import Network


def convert_fixed_int_to_decimal(amount: int) -> float:
    return amount / 10**constants.PLATFORM_PRECISION


def convert_decimal_to_fixed_int(amount: float) -> int:
    return int((amount * 10**constants.PLATFORM_PRECISION / constants.TICK_SIZE)) * constants.TICK_SIZE


def convert_fixed_lot_to_decimal(amount: int) -> float:
    return amount / 10**constants.POSITION_PRECISION


def convert_decimal_to_fixed_lot(amount: float) -> int:
    return int(amount * 10**constants.POSITION_PRECISION)


def cluster_endpoint(network: Network, tls: bool = True, ws: bool = False, whirligig=False) -> str:
    """Retrieve the RPC API URL for the specified cluster.

    :param cluster: The name of the cluster to use.
    :param tls: If True, use https. Defaults to True.
    """
    endpoint = cluster_api_url(network.value, tls=tls)
    if ws:
        ws_endpoint = re.sub(r"^http", "ws", endpoint)
        if whirligig:
            return ws_endpoint + "/whirligig"
        return ws_endpoint
    else:
        return endpoint


def get_tif_offset(expiry_ts: int, epoch_length: int, current_ts: int) -> int:
    if expiry_ts < current_ts:
        raise Exception(f"Cannot place expired order, current_ts: {current_ts}, expiry_ts: {expiry_ts}")
    epoch_start = current_ts - (current_ts % epoch_length)

    tif_offset = expiry_ts - epoch_start
    return min(tif_offset, epoch_length)
