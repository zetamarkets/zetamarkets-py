import asyncio
import os

import anchorpy
from solana.rpc.commitment import Confirmed
from solana.rpc.websocket_api import connect
from solders.rpc.config import RpcTransactionLogsFilterMentions

from zetamarkets_py.client import Client


async def main():
    # get local filesystem keypair wallet, defaults to ~/.config/solana/id.json
    wallet = anchorpy.Wallet.local()
    commitment = Confirmed
    endpoint = os.getenv("ENDPOINT", "https://api.mainnet-beta.solana.com")
    ws_endpoint = os.getenv("WS_ENDPOINT", "wss://api.mainnet-beta.solana.com")

    # load in client without any markets
    client = await Client.load(endpoint=endpoint, wallet=wallet, assets=[])

    # open up a websocket subscription
    async with connect(ws_endpoint) as ws:
        # subscribe to only logs/events that mention our margin account
        await ws.logs_subscribe(
            commitment=commitment, filter_=RpcTransactionLogsFilterMentions(client._margin_account_address)
        )
        first_resp = await ws.recv()
        first_resp[0].result
        print(f"Listening for events for margin account: {client._margin_account_address}")
        async for msg in ws:
            events = client.parse_event_payload(msg)
            print(events)


asyncio.run(main())
