import asyncio
import solana
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from solana.utils.cluster import Cluster, ENDPOINT
from solana.rpc.websocket_api import connect


from zeta_py.exchange import Exchange
from zeta_py import pda
from zeta_py.types import LoadExchangeConfig
from zeta_py.utils import cluster_endpoint
from zeta_py.constants import Asset
from zeta_py.zeta_client import accounts, program_id
from solders.sysvar import CLOCK


async def test_anchorpy(connection: AsyncClient):
    pricing_address, _ = pda.get_pricing(program_id.PROGRAM_ID)
    print(accounts.Pricing)
    pricing = await accounts.Pricing.fetch(connection, pricing_address)
    print(pricing)

    # clock = await connection.get_account_info_json_parsed(CLOCK)
    # print(clock.value.data.parsed["info"]["slot"])


async def async_ws(network: Cluster):
    async with connect(cluster_endpoint(network, ws=True)) as websocket:
        await websocket.account_subscribe(
            pda.get_pricing(program_id.PROGRAM_ID)[0],
            commitment="confirmed",
            encoding="base64",
        )
        first_resp = await websocket.recv()
        print(first_resp)
        subscription_id = first_resp[0].result
        while True:
            msg = await websocket.recv()
            print(msg)
            print(accounts.Pricing.decode(msg[0].result.value.data).mark_prices)
        await websocket.account_subscribe(subscription_id)


async def setup_exchange(network: Cluster):
    opts = {
        "skip_preflight": False,
        "preflight_commitment": "confirmed",
    }
    config = LoadExchangeConfig(
        **{
            "network": network,
            "connection": AsyncClient(cluster_endpoint(network)),
            "opts": opts,
            "throttle_ms": 0,
            "load_from_store": False,
        }
    )
    # zeta = await Exchange.create(config)
    zeta = Exchange(config)
    print(zeta.is_loaded)
    await zeta.load(config)
    print(zeta.is_loaded)
    for i in range(100):
        print(i)
        print("Mark Prices", zeta.accounts.pricing.account.mark_prices)
        print(
            "Perp Sync Queue Head",
            zeta.markets[Asset.SOL].accounts.perp_sync_queue.account.head,
        )
        await asyncio.sleep(1)
        if i == 50:
            await zeta.accounts.pricing.unsubscribe()


def main():
    # pk = Pubkey.from_string("6ZMKN79tGXcyE467S9h1vVN3cBQnHNtxv4nw2MLfJBAE")
    # info = http_client.get_account_info_json_parsed(pk)
    # print(info)

    network = "mainnet_beta"
    connection = AsyncClient(cluster_endpoint(network))

    # print(zeta.is_initialized)
    # print(zeta.is_setup)

    # asyncio.run(test_anchorpy(connection))
    # asyncio.run(async_ws(network))
    asyncio.run(setup_exchange(network))
