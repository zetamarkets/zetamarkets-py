import asyncio
import os
from datetime import datetime

from solana.rpc import commitment
from solana.rpc.async_api import AsyncClient
from solana.rpc.websocket_api import connect
from solana.utils.cluster import Cluster

from zeta_py import pda
from zeta_py.constants import Asset
from zeta_py.exchange import Exchange
from zeta_py.types import LoadExchangeConfig
from zeta_py.utils import cluster_endpoint
from zeta_py.zeta_client import accounts, program_id


async def test_anchorpy(connection: AsyncClient):
    pricing_address, _ = pda.get_pricing(program_id.PROGRAM_ID)
    print(pricing_address)
    pricing = await accounts.Pricing.fetch(connection, pricing_address)
    print([m for m in pricing.markets])

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
        "preflight_commitment": commitment.Confirmed,
    }
    endpoint = os.environ.get("ENDPOINT", cluster_endpoint(network))
    print(endpoint)
    config = LoadExchangeConfig(
        **{
            "network": network,
            "connection": AsyncClient(endpoint, commitment=opts.get("preflight_commitment")),
            "assets": [Asset.SOL],
            "opts": opts,
            "load_from_store": False,
        }
    )
    # zeta = await Exchange.create(config)
    zeta = await Exchange.create(config, subscribe=True)
    for i in range(100000):
        # if i == 15:
        #     await zeta.accounts.pricing.unsubscribe()
        print(datetime.fromtimestamp(zeta.clock.account.unix_timestamp))
        print(datetime.now() - datetime.fromtimestamp(zeta.clock.account.unix_timestamp))
        print(zeta.clock.last_update_slot)
        zeta.markets[Asset.SOL].print_orderbook()
        await asyncio.sleep(0.4)


def main():
    # pk = Pubkey.from_string("6ZMKN79tGXcyE467S9h1vVN3cBQnHNtxv4nw2MLfJBAE")
    # info = http_client.get_account_info_json_parsed(pk)
    # print(info)

    network = "mainnet_beta"
    AsyncClient(cluster_endpoint(network))
    # connection = AsyncClient("http://localhost:8899")

    # print(zeta.is_initialized)
    # print(zeta.is_setup)

    # asyncio.run(test_anchorpy(connection))
    # asyncio.run(async_ws(network))
    asyncio.run(setup_exchange(network))
