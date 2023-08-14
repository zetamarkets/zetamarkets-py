import solana
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from solana.utils.cluster import Cluster, cluster_api_url, ENDPOINT

from zeta_py.exchange import Exchange


async def main():
    # pk = Pubkey.from_string("6ZMKN79tGXcyE467S9h1vVN3cBQnHNtxv4nw2MLfJBAE")
    # info = http_client.get_account_info_json_parsed(pk)
    # print(info)

    network = "devnet"
    connection = AsyncClient(cluster_api_url(network))
    opts = {
        "skip_preflight": False,
        "preflight_commitment": "confirmed",
    }
    config = {
        "network": network,
        "connection": connection,
        "opts": opts,
        "throttle_ms": 0,
        "load_from_store": False,
    }
    zeta = await Exchange.create(config)

    print(zeta.is_initialized)
    print(zeta.is_setup)
