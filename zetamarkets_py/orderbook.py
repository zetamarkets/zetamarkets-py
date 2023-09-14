import time
from typing import Iterable, Union

from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solders.pubkey import Pubkey

from zetamarkets_py import utils
from zetamarkets_py.serum_client.accounts.market_state import MarketState
from zetamarkets_py.serum_client.accounts.orderbook import OrderbookAccount
from zetamarkets_py.serum_client.types.slab import SlabInnerNode, SlabLeafNode
from zetamarkets_py.types import Order, OrderInfo, Side


class Orderbook:
    """Represents an order book."""

    def __init__(self, side: Side, orderbook: OrderbookAccount, market_state: MarketState) -> None:
        if not (orderbook.account_flags.initialized and orderbook.account_flags.bids ^ orderbook.account_flags.asks):
            raise Exception("Invalid order book, either not initialized or neither of bids or asks")
        self.side = side
        self._slab = orderbook.slab
        self._market_state = market_state

    @classmethod
    async def load(
        cls, conn: AsyncClient, address: Pubkey, commitment: Commitment, side: Side, market_state: MarketState
    ) -> "Orderbook":
        orderbook = await OrderbookAccount.fetch(conn, address, commitment)
        return cls(side, orderbook, market_state)

    @staticmethod
    def _get_price_from_slab(node: Union[SlabInnerNode, SlabLeafNode]) -> int:
        """Get price from a slab node key.

        The key is constructed as the (price << 64) + (seq_no if ask_order else !seq_no).
        """
        return node.key >> 64

    @staticmethod
    def _get_seq_num_from_slab(key: int, side: Side) -> int:
        """Get sequence number from a slab node key.

        The key is constructed as the (price << 64) + (seq_no if ask_order else !seq_no).
        """
        # TODO: bit length might be variable bc of python
        # if key.bit_length() != 128:
        #     print(key.bit_length())
        #     raise ValueError("Key should be 128 bits")
        # Mask off highest 64 bits
        UPPER_64_BITMASK = 0x0000000000000000FFFFFFFFFFFFFFFF
        lower = key & UPPER_64_BITMASK
        if side == Side.Bid:
            # Bitwise NOT (since python doesn't have unsigned ints)
            return (1 << 64) - 1 - lower
        else:
            return lower

    @staticmethod
    def _is_order_expired(
        clock_ts: int, tif_offset: int, epoch_start_ts: int, seq_num: int, epoch_start_seq_num: int
    ) -> int:
        """ """
        if tif_offset > 0:
            if epoch_start_ts + tif_offset < clock_ts or seq_num <= epoch_start_seq_num:
                return True
        return False

    def _get_l2(self, depth: int, filter_tif: bool = True) -> list[OrderInfo]:
        """Get the Level 2 market information."""
        descending = self.side == Side.Bid
        # The first element of the inner list is price, the second is quantity.
        levels: list[list[int]] = []
        for node in self._slab.items(descending):
            seq_num = self._get_seq_num_from_slab(node.key, self.side)
            # using local time as a hack as opposed to self.exchange.clock.account.unix_timestamp
            clock_ts = time.time()
            order_expired = self._is_order_expired(
                clock_ts,
                node.tif_offset,
                self._market_state.epoch_start_ts,
                seq_num,
                self._market_state.start_epoch_seq_num,
            )
            if filter_tif and order_expired:
                continue
            price = self._get_price_from_slab(node)
            if len(levels) > 0 and levels[len(levels) - 1][0] == price:
                levels[len(levels) - 1][1] += node.quantity
            elif len(levels) == depth:
                break
            else:
                levels.append([price, node.quantity])
        return [
            OrderInfo(
                price=utils.convert_fixed_int_to_decimal(price_lots),
                size=utils.convert_fixed_lot_to_decimal(size_lots),
            )
            for price_lots, size_lots in levels
        ]

    def __iter__(self) -> Iterable[Order]:
        return self.orders()

    def orders(self) -> Iterable[Order]:
        for node in self._slab.items():
            price = self._get_price_from_slab(node)
            open_orders_address = node.owner

            yield Order(
                order_id=node.key,
                client_id=node.client_order_id,
                open_order_address=open_orders_address,
                fee_tier=node.fee_tier,
                info=OrderInfo(
                    price=utils.convert_fixed_int_to_decimal(price),
                    size=utils.convert_fixed_lot_to_decimal(node.quantity),
                ),
                side=self.side,
                open_order_slot=node.owner_slot,
                tif_offset=node.tif_offset,
            )
