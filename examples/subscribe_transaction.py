import asyncio
import json
import os

import anchorpy
import based58
import websockets
from anchorpy import Event, EventParser
from jsonrpcclient import request
from solana.rpc.commitment import Confirmed

from zetamarkets_py import constants
from zetamarkets_py.client import Client
from zetamarkets_py.events import (
    OrderCompleteEvent,
    PlaceOrderEvent,
    PlaceOrderEventWithArgs,
    TradeEvent,
    TradeEventWithPlacePerpOrderArgs,
)


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
            parser = EventParser(client.exchange.program_id, client.exchange.program.coder)

            jsonMsg = json.loads(msg)
            txValue = jsonMsg["params"]["result"]["value"]

            logMessages = txValue["meta"]["logMessages"]

            message = txValue["transaction"]["message"]
            if isinstance(message[0], int) or "instructions" not in message[0]:
                messageIndexed = message[1]
            else:
                messageIndexed = message[0]

            ixs = messageIndexed["instructions"][1:]
            ixArgs = []
            ixNames = []

            for ix in ixs:
                accKeysRaw = messageIndexed["accountKeys"][1:]
                accountKeys = [str(based58.b58encode(bytes(a)), encoding="utf-8") for a in accKeysRaw]

                loadedAddresses = txValue["meta"]["loadedAddresses"]
                loadedAddressesList = accountKeys + loadedAddresses["writable"] + loadedAddresses["readonly"]
                ownerAddress = loadedAddressesList[ix["programIdIndex"]]
                if ownerAddress != str(constants.ZETA_PID[client.network]):
                    ixArgs.append(None)
                    ixNames.append(None)
                    continue
                data = client.exchange.program.coder.instruction.parse(bytes(ix["data"][1:]))
                ixArgs.append(data.data)
                ixNames.append(data.name)

            # Split logMessages every time we see "invoke [1]"
            splitLogMessages = []
            splitIndices = []
            for i in range(len(logMessages)):
                if logMessages[i] == "Log truncated":
                    raise Exception("Logs truncated, missing event data")
                if logMessages[i].endswith("invoke [1]"):
                    splitIndices.append(i)

            splitLogMessages = [logMessages[i:j] for i, j in zip([0] + splitIndices, splitIndices + [None])]
            if len(splitLogMessages) > 0:
                splitLogMessages = splitLogMessages[1:]

            if len(ixArgs) != len(splitLogMessages) or len(ixNames) != len(splitLogMessages):
                raise Exception("Mismatched transation info lengths")

            # For each individual instruction, find the ix name and the events
            for i in range(len(splitLogMessages)):
                # # First log line will always be "...invoke [1]", second will be "Program log: Instruction: <ix_name>"
                ixName = ixNames[i]
                ixArg = ixArgs[i]

                if ixName is None or ixArg is None:
                    continue

                chunk = splitLogMessages[i]
                events: list[Event] = []
                parser.parse_logs(chunk, lambda evt: events.append(evt))

                # Depending on the instruction and event we can get different data from the args
                for event in events:
                    # Skip event that aren't for our account but mention our account
                    # eg if we do a taker trade, we want to skip the maker crank events
                    if str(event.data.margin_account) != str(client._margin_account_address):
                        continue

                    if ixName.startswith("place_perp_order"):
                        if event.name.startswith(TradeEvent.__name__):
                            print(TradeEventWithPlacePerpOrderArgs.from_event_and_args(event, ixArg))
                        elif event.name.startswith(PlaceOrderEvent.__name__):
                            print(PlaceOrderEventWithArgs.from_event_and_args(event, ixArg))
                        elif event.name.startswith(OrderCompleteEvent.__name__):
                            print(OrderCompleteEvent.from_event(event))

                    elif ixName.startswith("crank_event_queue"):
                        if event.name.startswith(TradeEvent.__name__):
                            print(TradeEvent.from_event(event))
                        elif event.name.startswith(OrderCompleteEvent.__name__):
                            print(OrderCompleteEvent.from_event(event))

                    elif ixName.startswith("cancel_"):
                        if event.name.startswith(OrderCompleteEvent.__name__):
                            print(OrderCompleteEvent.from_event(event))


asyncio.run(main())
