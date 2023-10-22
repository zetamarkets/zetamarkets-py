import logging
import re

import colorlog
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


def http_to_ws(endpoint: str) -> str:
    return re.sub(r"^http", "ws", endpoint)


def cluster_endpoint(network: Network, tls: bool = True, ws: bool = False) -> str:
    """Retrieve the RPC API URL for the specified cluster.

    :param cluster: The name of the cluster to use.
    :param tls: If True, use https. Defaults to True.
    """
    endpoint = cluster_api_url(network.value, tls=tls)  # type: ignore
    if ws:
        ws_endpoint = http_to_ws(endpoint)
        return ws_endpoint
    else:
        return endpoint


def get_tif_offset(expiry_ts: int, epoch_length: int, current_ts: int) -> int:
    if expiry_ts < current_ts:
        raise Exception(f"Cannot place expired order, current_ts: {current_ts}, expiry_ts: {expiry_ts}")
    epoch_start = current_ts - (current_ts % epoch_length)

    tif_offset = expiry_ts - epoch_start
    return min(tif_offset, epoch_length)


def create_logger(name: str, log_level: int = logging.CRITICAL, file_name: str = None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    formatter = colorlog.ColoredFormatter("%(log_color)s%(levelname)s:%(name)s:%(message)s")

    # Create console handler and set level to same as the logger
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if file_name:
        fh = logging.FileHandler(file_name)
        fh.setLevel(log_level)
        file_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
        fh.setFormatter(file_formatter)
        logger.addHandler(fh)
    return logger
