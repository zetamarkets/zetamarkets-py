import asyncio
import os

import anchorpy

from zetamarkets_py.client import Client
from zetamarkets_py.types import Asset, MultiOrderArgs, OrderType

from solders.compute_budget import set_compute_unit_limit
async def main():
    # get local filesystem keypair wallet, defaults to ~/.config/solana/id.json
    wallet = anchorpy.Wallet.local()
    asset = Asset.SOL
    endpoint = os.getenv("ENDPOINT", "insert_endpoint")

    # load in client with just solana market, by default loads in all markets
    client = await Client.load(endpoint=endpoint, double_down_endpoints=other_endpooints, wallet=wallet, assets=[asset])


    # check balance on-chain
    balance, positions = await client.fetch_margin_state()
    print(f"Balance: ${balance}")

    bid_orders = [
        MultiOrderArgs(10.5, 0.1),
        MultiOrderArgs(10.4, 0.1),
        MultiOrderArgs(10.3, 0.1),
        MultiOrderArgs(10.2, 0.1),
    ]

    ask_orders = [
        MultiOrderArgs(220, 0.1),
        MultiOrderArgs(220.1, 0.1),
        MultiOrderArgs(220.2, 0.1),
        MultiOrderArgs(220.3, 0.1),
    ]

    await client.place_multi_orders_for_market(asset, bid_orders, ask_orders, OrderType.PostOnly, pre_instructions=[set_compute_unit_limit(500_000)])



asyncio.run(main())
