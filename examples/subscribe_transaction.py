import asyncio
import json
import os

import anchorpy
import websockets
from jsonrpcclient import request
from solana.rpc.commitment import Confirmed

from zetamarkets_py.client import Client


async def main():
    # get local filesystem keypair wallet, defaults to ~/.config/solana/id.json
    wallet = anchorpy.Wallet.local()
    commitment = Confirmed

    # NOTE: NEEDS TO BE A TRITON URL TO SUPPORT transactionSubscribe RPC METHOD
    endpoint = os.getenv("ENDPOINT", "https://api.mainnet-beta.solana.com")
    ws_endpoint = os.getenv("WS_ENDPOINT", "wss://api.mainnet-beta.solana.com")

    # load in client without any markets
    client = await Client.load(endpoint=endpoint, wallet=wallet, assets=[])

    # open up a websocket subscription
    async with websockets.connect(ws_endpoint + "/whirligig") as ws:
        # subscribe to only transactions that mention our margin account
        transaction_subscribe = request(
            "transactionSubscribe",
            params=[
                {
                    "mentions": [str(client._margin_account_address)],
                    "failed": False,
                    "vote": False,
                },
                {
                    "commitment": str(commitment),
                },
            ],
        )

        await ws.send(json.dumps(transaction_subscribe))
        first_resp = await ws.recv()
        first_resp

        print(f"Listening for transactions for margin account: {client._margin_account_address}")
        async for msg in ws:
            await client.parse_transaction_payload(msg)


asyncio.run(main())
