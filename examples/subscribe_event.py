import asyncio
import os

import anchorpy
from solana.rpc.commitment import Confirmed

from zetamarkets_py.client import Client
from zetamarkets_py.events import (
    ApplyFundingEvent,
    CancelOrderEvent,
    LiquidationEvent,
    PlaceOrderEvent,
    TradeEvent,
)


async def main():
    # Get local filesystem keypair wallet, defaults to ~/.config/solana/id.json
    wallet = anchorpy.Wallet.local()
    commitment = Confirmed
    endpoint = os.getenv("ENDPOINT", "https://api.mainnet-beta.solana.com")
    ws_endpoint = os.getenv("WS_ENDPOINT", "wss://api.mainnet-beta.solana.com")

    # Load in client without any markets
    client = await Client.load(
        endpoint=endpoint, ws_endpoint=ws_endpoint, commitment=commitment, wallet=wallet, assets=[]
    )

    # Subscribe to margin account events
    print(f"Listening for events on margin account: {client._margin_account_address} (authority: {wallet.public_key})")
    async for events, _ in client.subscribe_events(
        # Listen to all events across Zeta by setting the following argument:
        # ignore_third_party_events=False
    ):
        # Loop over the events in each tx
        for event in events:
            # Event can be PlaceOrder, Trade, OrderComplete or Liquidate
            if isinstance(event, PlaceOrderEvent):
                print("Place order event: ", event)
            elif isinstance(event, TradeEvent):
                print("Trade event: ", event)
            elif isinstance(event, CancelOrderEvent):
                print("Cancel order event: ", event)
            elif isinstance(event, LiquidationEvent):
                print("Liquidation event: ", event)
            elif isinstance(event, ApplyFundingEvent):
                print("Funding event: ", event)


asyncio.run(main())
