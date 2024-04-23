import asyncio
import os

import anchorpy

from zetamarkets_py.client import Client
from zetamarkets_py.types import Asset, Decimal


async def main():
    # get local filesystem keypair wallet, defaults to ~/.config/solana/id.json
    wallet = anchorpy.Wallet.local()
    asset = Asset.SOL
    endpoint = os.getenv("ENDPOINT", "https://api.mainnet-beta.solana.com")

    # load in client with just solana market, by default loads in all markets
    client = await Client.load(endpoint=endpoint, wallet=wallet, assets=[asset])

    # get the latest funding rate and convert from rust_decimal on-chain representation to float
    funding = client.exchange.pricing.latest_funding_rates[asset.to_index()]
    print(f"{asset} funding rate: {Decimal.from_anchor_decimal(funding).to_float()}")


asyncio.run(main())
