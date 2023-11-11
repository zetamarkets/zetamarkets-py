import asyncio
import os

import anchorpy

from zetamarkets_py.client import Client
from zetamarkets_py.types import Asset


async def main():
    # get local filesystem keypair wallet, defaults to ~/.config/solana/id.json
    wallet = anchorpy.Wallet.local()
    asset = Asset.SOL
    endpoint = os.getenv("ENDPOINT", "https://api.mainnet-beta.solana.com")

    # load in client with just solana market, by default loads in all markets
    client = await Client.load(endpoint=endpoint, wallet=wallet, assets=[asset])

    summary = await client.get_account_risk_summary()
    print(f"Balance: ${summary.balance}")
    print(f"Unrealized PnL: ${summary.unrealized_pnl}")
    print(f"Equity: ${summary.equity}")
    print(f"Position Value: ${summary.position_value}")
    print(f"Initial Margin: ${summary.initial_margin}")
    print(f"Maintenance Margin: ${summary.maintenance_margin}")
    print(f"Margin Usage: {summary.margin_utilization:.2%}")
    print(f"Leverage: {summary.leverage}x")


asyncio.run(main())
