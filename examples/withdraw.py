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

    print("Withdrawing 0.1 USDC from margin account")
    await client.withdraw(0.1, priority_fee=10)

asyncio.run(main())
