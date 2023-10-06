import asyncio
import os

import anchorpy

from zetamarkets_py.client import Client
from zetamarkets_py.types import Asset, OrderArgs, OrderOptions, Side


async def main():
    # get local filesystem keypair wallet, defaults to ~/.config/solana/id.json
    wallet = anchorpy.Wallet.local()
    asset = Asset.SOL
    endpoint = os.getenv("ENDPOINT", "https://api.mainnet-beta.solana.com")

    # load in client with just solana market, by default loads in all markets
    client = await Client.load(endpoint=endpoint, wallet=wallet, assets=[asset])

    # deposit 0.1 USDC into margin account
    await client.deposit(0.1)

    # check balance on-chain
    balance = await client.fetch_balance()
    print(f"Balance: {balance}")

    # (optional) order options
    # here you can specify TIF order expiry, client order id, order type (limit, post-only, ...) etc.
    order_opts = OrderOptions(client_order_id=1337)

    # place order
    side = Side.Bid
    order = OrderArgs(price=0.1, size=0.001, side=side, order_opts=order_opts)
    await client.place_orders_for_market(asset=asset, orders=[order])

    # check open orders
    open_orders = await client.fetch_open_orders(Asset.SOL)
    print("Open Orders:")
    for order in open_orders:
        print(f"{order.side.name} {order.info.size}x ${order.info.price}")

    # cancel order
    await client.cancel_order(Asset.SOL, order_id=open_orders[0].order_id, side=side)


asyncio.run(main())
