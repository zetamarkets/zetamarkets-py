import asyncio
import os

from solana.rpc.commitment import Confirmed
from solana.rpc.websocket_api import connect

from zetamarkets_py.client import Client
from zetamarkets_py.orderbook import Orderbook
from zetamarkets_py.serum_client.accounts.orderbook import OrderbookAccount
from zetamarkets_py.types import Asset, Side


async def main():
    asset = Asset.SOL
    commitment = Confirmed
    endpoint = os.getenv("ENDPOINT", "https://api.mainnet-beta.solana.com")
    ws_endpoint = os.getenv("WS_ENDPOINT", "wss://api.mainnet-beta.solana.com")

    # load in client, we're simply using this to fetch the orderbook bids address
    client = await Client.load(endpoint=endpoint, assets=[asset])
    address = client.exchange.markets[asset]._market_state.bids

    # open up a websocket subscription to the bids account
    async with connect(ws_endpoint) as ws:
        await ws.account_subscribe(
            address,
            commitment=commitment,
            encoding="base64+zstd",
        )
        first_resp = await ws.recv()
        first_resp[0].result
        async for msg in ws:
            # decode the bytes received over the websocket based on the account data layout
            account = OrderbookAccount.decode(msg[0].result.value.data)
            # create an orderbook object from the account data that contains useful helper methods
            orderbook = Orderbook(Side.Bid, account, client.exchange.markets[asset]._market_state)
            print("=" * 20 + "Bids" + "=" * 20)
            for level in orderbook._get_l2(5):
                print(level)


asyncio.run(main())
