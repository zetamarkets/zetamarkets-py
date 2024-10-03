import asyncio
import os

import anchorpy

from zetamarkets_py.client import Client
from zetamarkets_py.types import Asset, OrderArgs, OrderOptions, Side, SelfTradeBehaviorZeta


async def main():
    # get local filesystem keypair wallet, defaults to ~/.config/solana/id.json
    wallet = anchorpy.Wallet.local()
    asset = Asset.SOL
    endpoint = os.getenv("ENDPOINT", "https://zeta-zeta-61e4.mainnet.rpcpool.com/269b8dcb-fea0-4b60-a317-2a7281381fdb")

    # load in client with just solana market, by default loads in all markets
    client = await Client.load(endpoint=endpoint, wallet=wallet, assets=[asset])

    # deposit 0.1 USDC into margin account
    # print("Depositing 0.1 USDC into margin account")
    # await client.deposit(0.1)

    # check balance on-chain
    balance, positions = await client.fetch_margin_state()
    print(f"Balance: ${balance}")

    # (optional) order options
    # here you can specify TIF order expiry, client order id, order type (limit, post-only, ...) etc.
    order_opts = OrderOptions(client_order_id=1337, self_trade_behavior=SelfTradeBehaviorZeta.AbortTransaction)

    # place order
    side = Side.Bid
    order = OrderArgs(price=130, size=0.1, side=side, order_opts=order_opts)
    print(f"Placing {order.side} order: {order.size}x {str(asset)}-PERP @ ${order.price}")
    await client.place_orders_for_market(asset=asset, orders=[order], priority_fee=10)

    # check open orders
    open_orders = await client.fetch_open_orders(Asset.SOL)
    print("Current open orders:")
    for order in open_orders:
        print(f"- {order.side.name} {order.info.size}x {str(asset)}-PERP @ ${order.info.price}")

    # cancel order
    print(f"Cancelling order with id: {open_orders[0].order_id}")
    # await client.cancel_order(Asset.SOL, order_id=open_orders[0].order_id, side=side)
    await client.cancel_order_by_client_order_id(Asset.SOL, client_order_id=1337, priority_fee=10)


asyncio.run(main())
