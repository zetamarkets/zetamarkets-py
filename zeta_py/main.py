import asyncio
import logging
import os

from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solana.rpc.websocket_api import connect

from zeta_py import pda
from zeta_py.constants import Asset
from zeta_py.exchange import Exchange
from zeta_py.types import Network
from zeta_py.utils import cluster_endpoint
from zeta_py.zeta_client import accounts, program_id

logging.getLogger("zeta_py").setLevel(logging.DEBUG)


async def test_anchorpy(connection: AsyncClient):
    pricing_address = pda.get_pricing_address(program_id.PROGRAM_ID)
    print(pricing_address)
    pricing = await accounts.Pricing.fetch(connection, pricing_address)
    print([m for m in pricing.markets])


async def async_ws(network: Network):
    async with connect(cluster_endpoint(network, ws=True)) as websocket:
        await websocket.account_subscribe(
            pda.get_pricing_address(program_id.PROGRAM_ID)[0],
            commitment="confirmed",
            encoding="base64+zstd",
        )
        first_resp = await websocket.recv()
        print(first_resp)
        subscription_id = first_resp[0].result
        while True:
            msg = await websocket.recv()
            print(msg)
            print(accounts.Pricing.decode(msg[0].result.value.data).mark_prices)
        await websocket.account_subscribe(subscription_id)


async def setup_exchange(network: Network):
    commitment = Confirmed
    opts = {
        "preflight_commitment": commitment,
    }
    endpoint = os.environ.get("ENDPOINT", cluster_endpoint(network))
    print(endpoint)
    connection = AsyncClient(endpoint, commitment=commitment)
    await Exchange.load(network=network, connection=connection, assets=[Asset.SOL], tx_opts=opts, subscribe=True)
    for i in range(100000):
        # print(datetime.fromtimestamp(zeta.clock.account.unix_timestamp))
        # print(datetime.now() - datetime.fromtimestamp(zeta.clock.account.unix_timestamp))
        # print(zeta.clock.last_update_slot)
        # zeta.markets[Asset.SOL].print_orderbook()
        await asyncio.sleep(0.4)


def main():
    network = Network.MAINNET

    # asyncio.run(test_anchorpy(connection))
    # asyncio.run(async_ws(network))
    asyncio.run(setup_exchange(network))
