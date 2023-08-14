import re
from typing import Optional, Tuple
from zeta_py import constants
from solders.pubkey import Pubkey
from solana.utils.cluster import Cluster, cluster_api_url

"""
Converts a native lot size where 1 unit = 0.001 lots to human readable decimal
@param amount
"""


def convert_native_lot_size_to_decimal(amount: int) -> float:
    return amount / 10**constants.POSITION_PRECISION


def cluster_endpoint(
    cluster: Optional[Cluster] = None, tls: bool = True, ws: bool = False
) -> str:
    """Retrieve the RPC API URL for the specified cluster.

    :param cluster: The name of the cluster to use.
    :param tls: If True, use https. Defaults to True.
    """
    endpoint = cluster_api_url(cluster, tls=tls)
    if ws:
        return re.sub(r"^http", "ws", endpoint)
    else:
        return endpoint
