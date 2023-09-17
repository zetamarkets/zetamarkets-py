import asyncio
from datetime import datetime, timedelta
import json
import os
import time
from typing import List

import anchorpy
import websockets
from solana.rpc.commitment import Confirmed

from zetamarkets_py.client import Client
from zetamarkets_py.orderbook import Orderbook
from zetamarkets_py.types import Asset, Order, OrderOptions, OrderType, Side


class MarketMaker:
    def __init__(self, client: Client, asset: Asset, current_open_orders: List[Order]) -> None:
        self.client = client
        self.asset = asset
        self._is_quoting = False
        self.fair_price = None

        # feel free to play around with these params
        self.offset_bps = 0
        self.edge_bps = 20
        self.quote_size = 0.001

        self.EDGE_REQUOTE_THRESHOLD = 0.25  # only requote if the fair price moves more than 25% of the edge
        self.TIF_DURATION = 60  # 1 minute

        # get the best bid in the open orders
        self.bid_price = max([o.info.price for o in current_open_orders if o.side == Side.Bid], default=None)
        self.ask_price = min([o.info.price for o in current_open_orders if o.side == Side.Ask], default=None)

    @classmethod
    async def load(cls, endpoint, wallet, asset, commitment=Confirmed):
        client = await Client.load(endpoint=endpoint, commitment=commitment, wallet=wallet, assets=[asset])
        open_orders = await client.fetch_open_orders(asset)
        return cls(client, asset, open_orders)

    async def subscribe_fair_price(self):
        # Connect to Binance USDC-margined futures websocket
        stream = self.asset.to_string().lower() + "usdt@bookTicker"
        print("Subscribing to Binance stream: " + stream)
        async with websockets.connect("wss://fstream.binance.com/ws/" + stream) as ws:
            id = int(time.time() * 1000)
            await ws.send(json.dumps({"method": "SUBSCRIBE", "params": [stream], "id": id}))
            # Establish connection
            await ws.recv()
            async for msg in ws:
                try:
                    ticker = json.loads(msg)
                    if ticker.get("e") == "bookTicker":
                        # volume weighted average price based on BBO
                        vwap = (float(ticker["b"]) * int(ticker["B"]) + float(ticker["a"]) * int(ticker["A"])) / (
                            int(ticker["B"]) + int(ticker["A"])
                        )
                        self.fair_price = vwap
                        await self.update_quotes()
                except ValueError as e:
                    print(e)
                except Exception as e:
                    print(e)

    async def subscribe_zeta_price(self):
        async def on_bid_update(orderbook: Orderbook):
            print(f"Best bid: {orderbook._get_l2(1)}")
            pass

        async def on_ask_update(orderbook: Orderbook):
            print(f"Best ask: {orderbook._get_l2(1)}")
            pass

        await asyncio.gather(
            self.client.subscribe_orderbook(self.asset, Side.Bid, on_bid_update),
            self.client.subscribe_orderbook(self.asset, Side.Ask, on_ask_update),
        )

    async def update_quotes(self):
        if self._is_quoting:
            return
        if self.fair_price is None:
            return
        # Skip requote if the fair price is within the edge
        fair_price = self.fair_price * (1 + self.offset_bps / 10000)
        if self.bid_price is not None and self.ask_price is not None:
            # Get the latest mark price and calculate bid/ask prices
            current_mid_price = (self.bid_price + self.ask_price) / 2
            edge = current_mid_price * (self.edge_bps / 10000)

            # If the fair price is within the edge, don't update the quotes
            divergence = abs(fair_price - current_mid_price)
            if divergence < edge * self.EDGE_REQUOTE_THRESHOLD:
                # print(f"Skipping requote, divergence/edge = {divergence/edge:.2%}")
                return

        print(f"External price: {self.fair_price}")
        print(f"Internal price: {fair_price}")

        # Requote
        bid_price = fair_price * (1 - self.edge_bps / 10000)
        ask_price = fair_price * (1 + self.edge_bps / 10000)

        # Set order options
        # Orders are sent as post-only to ensure that we don't take liquidity
        # We use time-in-force to ensure that the order is cancelled after a certain time and not left hanging
        expiry_ts = int((datetime.now() + timedelta(seconds=self.TIF_DURATION)).timestamp())
        order_opts = OrderOptions(expiry_ts=expiry_ts, order_type=OrderType.PostOnly, client_order_id=1234)

        # Execute quote!
        self._is_quoting = True
        try:
            await self.client.replace_quote(
                self.asset, bid_price, self.quote_size, ask_price, self.quote_size, order_opts
            )
            self.bid_price = bid_price
            self.ask_price = ask_price
        except Exception as e:
            raise e
        finally:
            self._is_quoting = False

    async def run(self):
        try:
            zeta_subscription = asyncio.create_task(self.subscribe_zeta_price())
            binance_subscription = asyncio.create_task(self.subscribe_fair_price())
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            # Cancel all orders on exit
            await self.client.cancel_orders_for_market(self.asset)
            zeta_subscription.cancel()
            binance_subscription.cancel()


async def main():
    endpoint = os.getenv("ENDPOINT", "https://api.mainnet-beta.solana.com")
    wallet = anchorpy.Wallet.local()  # get local filesystem keypair wallet
    mm = await MarketMaker.load(endpoint, wallet, Asset.SOL)

    await mm.run()


asyncio.run(main())
