import argparse
import asyncio
import time
from datetime import datetime, timedelta
from typing import List

import anchorpy
import httpx
from binance import AsyncClient, BinanceSocketManager  # type: ignore
from solana.exceptions import SolanaRpcException
from solana.rpc.commitment import Commitment, Confirmed
from solana.rpc.types import TxOpts

from zetamarkets_py import utils
from zetamarkets_py.client import Client
from zetamarkets_py.constants import MIN_LOT_SIZE
from zetamarkets_py.orderbook import Orderbook
from zetamarkets_py.types import (
    Asset,
    Network,
    Order,
    OrderArgs,
    OrderOptions,
    OrderType,
    Side,
)


class MarketMaker:
    def __init__(
        self, client: Client, asset: Asset, size: float, edge: float, offset: float, current_open_orders: List[Order]
    ) -> None:
        self.client = client
        self.asset = asset
        self._is_quoting = False
        self.fair_price = None

        # feel free to play around with these params
        self.edge_bps = edge
        self.offset_bps = offset
        self.quote_size = size

        self.EDGE_REQUOTE_THRESHOLD = 0.25  # only requote if the fair price moves more than 25% of the edge
        self.TIF_DURATION = 120  # 2 minutes, can do lower at the expense of quotes expiring when volatility is low

        self._ratelimit_until_ts = 0  # timestamp for when we can retry after being rate limited

        # get the best bid in the open orders
        self.bid_price = max([o.info.price for o in current_open_orders if o.side == Side.Bid], default=None)
        self.ask_price = min([o.info.price for o in current_open_orders if o.side == Side.Ask], default=None)

    @classmethod
    async def load(
        cls,
        endpoint: str,
        wallet: anchorpy.Wallet,
        asset: Asset,
        size=0.001,
        edge=20,
        offset=0,
        network=Network.MAINNET,
        commitment=Confirmed,
    ):
        tx_opts = TxOpts(
            skip_preflight=True, skip_confirmation=False, preflight_commitment=commitment
        )  # skip preflight to save time
        client = await Client.load(
            endpoint=endpoint,
            commitment=commitment,
            wallet=wallet,
            assets=[asset],
            tx_opts=tx_opts,
            network=network,
            log_level="INFO",
        )
        open_orders = await client.fetch_open_orders(asset)
        return cls(client, asset, size, edge, offset, open_orders)

    async def subscribe_fair_price(self, max_retries=3):
        client = await AsyncClient.create()
        bm = BinanceSocketManager(client)
        retry_count = 0
        while retry_count < max_retries:
            try:
                # get the latest bid/ask price from Binance USD-M futures
                ts = bm.symbol_ticker_futures_socket(self.asset.to_string().upper() + "USDT")
                async with ts as tscm:
                    while True:
                        response = await tscm.recv()
                        if "e" in response and response["e"] == "error":
                            # close and restart the socket
                            print(f"Binance websocket error: {response['m']}")
                            retry_count += 1
                            break
                        ticker = response["data"]
                        # volume weighted average price based on BBO
                        binance_vwap = (
                            float(ticker["b"]) * float(ticker["B"]) + float(ticker["a"]) * float(ticker["A"])
                        ) / (float(ticker["B"]) + float(ticker["A"]))
                        self.fair_price = binance_vwap
                        try:
                            # Use asyncio.create_task to run update_quotes concurrently as to not block the websocket
                            asyncio.create_task(self.update_quotes())
                        except Exception as e:
                            print(f"Exception in update_quotes: {e}")
                            retry_count += 1
                            break
            except asyncio.CancelledError:
                print("Gracefully exiting...")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                retry_count += 1
            finally:
                await client.close_connection()

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
            # print("Already quoting")
            return
        if time.time() < self._ratelimit_until_ts:
            print(f"Rate limited by RPC. Retrying in {self._ratelimit_until_ts - time.time():.1f} seconds")
            return
        if self.fair_price is None:
            print("No fair price yet")
            return
        # Skip requote if the fair price is within the edge
        fair_price = self.fair_price * (1 + self.offset_bps / 10000)
        if self.bid_price is not None and self.ask_price is not None:
            # Get the latest mark price and calculate bid/ask prices
            current_mid_price = (self.bid_price + self.ask_price) / 2
            edge = current_mid_price * (self.edge_bps / 10000)

            divergence = abs(fair_price - current_mid_price)
            print(f"Divergence/edge = {divergence/edge:.2%}")
            # If the fair price is within the edge, don't update the quotes
            if divergence < edge * self.EDGE_REQUOTE_THRESHOLD:
                return

        print(f"External price: {self.fair_price}")
        print(f"Internal price: {fair_price}")

        # Requote
        bid_price = fair_price * (1 - self.edge_bps / 10000)
        ask_price = fair_price * (1 + self.edge_bps / 10000)

        # Set order options
        # Orders are sent as post-only to ensure that we don't take liquidity
        # We use time-in-force to ensure that the order is cancelled after a certain time and not left hanging
        if self.client.network == Network.MAINNET:
            expiry_ts = int((datetime.now() + timedelta(seconds=self.TIF_DURATION)).timestamp())
        else:
            # TIF doesn't work in devnet for some assets afaik
            expiry_ts = None
        # Use PostOnly to avoid taker fills, use Limit if you want to take
        order_opts = OrderOptions(expiry_ts=expiry_ts, order_type=OrderType.PostOnly, client_order_id=1337)
        bid_order = OrderArgs(bid_price, self.quote_size, Side.Bid, order_opts)
        ask_order = OrderArgs(ask_price, self.quote_size, Side.Ask, order_opts)

        # Execute quote!
        self._is_quoting = True
        try:
            print(f"Quoting {self.asset}: ${bid_order.price:.4f}@${ask_order.price:.4f} x {self.quote_size}")
            await self.client.replace_orders_for_market(self.asset, [bid_order, ask_order])
            # (Re)set the state now that we know we've succesfully quoted
            self.bid_price = bid_price
            self.ask_price = ask_price
        except SolanaRpcException as e:
            original_exception = e.__cause__
            if (
                isinstance(original_exception, httpx.HTTPStatusError)
                and original_exception.response.status_code == 429  # HTTP status code for Too Many Requests
            ):
                retry_after = int(original_exception.response.headers.get("Retry-After", 10))
                print(f"Rate limited. Retrying after {retry_after} seconds...")
                self._ratelimit_until_ts = time.time() + retry_after  # Retry after x seconds
            else:
                print(f"An RPC error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
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
    parser = argparse.ArgumentParser(description="Process some blockchain parameters.")

    parser.add_argument(
        "-n",
        "--network",
        type=Network,
        choices=list(Network),
        default=Network.MAINNET,
        help="The network to use. Defaults to %(default)s.",
    )

    parser.add_argument(
        "-u",
        "--url",
        type=str,
        help="The endpoint URL (optional).",
    )

    parser.add_argument(
        "-c",
        "--commitment",
        type=Commitment,
        default=Confirmed,
        help="The commitment level. Defaults to %(default)s.",
    )

    parser.add_argument(
        "-a",
        "--asset",
        type=Asset,
        choices=list(Asset),
        default=Asset.SOL,
        help="The asset identifier. Defaults to %(default)s.",
    )

    parser.add_argument(
        "-s",
        "--size",
        type=float,
        default=MIN_LOT_SIZE,
        help="The quote edge in bps. Defaults to %(default)s lots.",
    )

    parser.add_argument(
        "-e",
        "--edge",
        type=float,
        default=20,
        help="The quote edge in bps. Defaults to %(default)s bps.",
    )

    parser.add_argument(
        "-o",
        "--offset",
        type=float,
        default=0,
        help="The quote offset in bps. Defaults to %(default)s bps.",
    )

    args = parser.parse_args()

    # If endpoint is not specified, get it from the network argument
    endpoint = args.url if args.url else utils.cluster_endpoint(args.network)

    print(f"Network: {args.network.value}")
    print(f"Endpoint: {endpoint}")
    print(f"Commitment: {args.commitment}")
    print(f"Asset: {args.asset}")
    print(f"Size: {args.size} lots")
    print(f"Edge: {args.edge} bps")
    print(f"Offset: {args.offset} bps")

    wallet = anchorpy.Wallet.local()  # get local filesystem keypair wallet
    mm = await MarketMaker.load(
        endpoint, wallet, args.asset, args.size, args.edge, args.offset, args.network, args.commitment
    )

    await mm.run()


asyncio.run(main())
