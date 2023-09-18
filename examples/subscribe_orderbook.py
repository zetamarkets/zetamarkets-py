import asyncio
import os

from solana.rpc.commitment import Confirmed
from solana.rpc.websocket_api import connect

from zetamarkets_py.client import Client
from zetamarkets_py.orderbook import Orderbook
from zetamarkets_py.serum_client.accounts.orderbook import OrderbookAccount
from zetamarkets_py.types import Asset, Side

# This example shows how to subscribe to multiple accounts over the same websocket connection
# This is useful for subscribing to the full orderbook (bids and asks) for a given market on Zeta


async def main():
    asset = Asset.SOL
    commitment = Confirmed
    endpoint = os.getenv("ENDPOINT", "https://api.mainnet-beta.solana.com")
    ws_endpoint = os.getenv("WS_ENDPOINT", "wss://api.mainnet-beta.solana.com")

    # load in client, we're simply using this to fetch the orderbook bids address
    client = await Client.load(endpoint=endpoint, assets=[asset])
    bids_address = client.exchange.markets[asset]._market_state.bids
    asks_address = client.exchange.markets[asset]._market_state.asks

    # subscribe to both bids and asks over the same websocket connection
    async with connect(ws_endpoint) as ws:
        # Subscribe to the first address
        await ws.account_subscribe(
            bids_address,
            commitment=commitment,
            encoding="base64+zstd",
        )
        bids_subscription_id = (await ws.recv())[0].result
        print(bids_subscription_id)

        # Subscribe to the second address
        await ws.account_subscribe(
            asks_address,
            commitment=commitment,
            encoding="base64+zstd",
        )
        asks_subscription_id = (await ws.recv())[0].result
        print(asks_subscription_id)

        # Listen for messages related to both subscriptions
        async for msg in ws:
            # Decode the bytes received over the websocket based on the account data layout
            # Bids and asks have the same layout, so we can use the same decoder
            account = OrderbookAccount.decode(msg[0].result.value.data)
            # Process the account data
            side = Side.Bid if msg[0].subscription == bids_subscription_id else Side.Ask
            orderbook = Orderbook(side, account, client.exchange.markets[asset]._market_state)
            print("=" * 20 + side.name + "=" * 20)
            levels = orderbook._get_l2(5)
            if side == Side.Ask:
                levels = reversed(levels)
            for level in levels:
                print(level)


asyncio.run(main())
