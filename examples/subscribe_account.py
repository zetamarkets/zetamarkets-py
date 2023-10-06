import asyncio
import os

from solana.rpc.commitment import Confirmed

from zetamarkets_py.client import Client
from zetamarkets_py.types import Asset, Side


async def main():
    asset = Asset.SOL
    commitment = Confirmed
    endpoint = os.getenv("ENDPOINT", "https://api.mainnet-beta.solana.com")
    # optional: pass in your own websocket endpoint
    ws_endpoint = os.getenv("WS_ENDPOINT", "wss://api.mainnet-beta.solana.com")

    client = await Client.load(endpoint=endpoint, ws_endpoint=ws_endpoint, commitment=commitment, assets=[asset])

    # subscribe_orderbook yields Orderbook objects, which come with a bunch of helper methods
    async for orderbook in client.subscribe_orderbook(asset, Side.Bid):
        print("=" * 20 + "Bids" + "=" * 20)
        for level in orderbook._get_l2(5):
            print(level)


asyncio.run(main())
