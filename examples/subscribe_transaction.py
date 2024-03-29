import asyncio
import os

import anchorpy
from solana.rpc.commitment import Confirmed

from zetamarkets_py.client import Client
from zetamarkets_py.events import (
    CancelOrderEvent,
    LiquidationEvent,
    PlaceOrderEventWithArgs,
    TradeEvent,
)


async def main():
    # Get local filesystem keypair wallet, defaults to ~/.config/solana/id.json
    wallet = anchorpy.Wallet.local()
    commitment = Confirmed
    endpoint = os.getenv("ENDPOINT", "https://api.mainnet-beta.solana.com")
    # Note: Needs to be a Triton websocket endpoint to support transactionSubscribe
    # https://docs.triton.one/project-yellowstone/whirligig-websockets#transactionsubscribe
    ws_endpoint = os.getenv("WS_ENDPOINT", "wss://api.mainnet-beta.solana.com")

    # Load in client without any markets
    client = await Client.load(
        endpoint=endpoint,
        ws_endpoint=ws_endpoint,
        commitment=commitment,
        wallet=wallet,
        assets=[],
    )

    # Subscribe to margin account transactions
    print(f"Listening for transactions on margin account: {client._margin_account_address}")
    async for tx_events, _ in client.subscribe_transactions(
        # Listen to all transactions across Zeta by setting the following arguments:
        # ignore_truncation=True, ignore_third_party_transactions=False
    ):
        # Loop over the events in each tx
        for event in tx_events:
            # Event can be PlaceOrder, Trade, OrderComplete or Liquidate
            if isinstance(event, PlaceOrderEventWithArgs):
                print("Place order event: ", event)
            elif isinstance(event, TradeEvent):
                print("Trade event: ", event)
            elif isinstance(event, CancelOrderEvent):
                print("Cancel order event: ", event)
            elif isinstance(event, LiquidationEvent):
                print("Liquidation event: ", event)


asyncio.run(main())
