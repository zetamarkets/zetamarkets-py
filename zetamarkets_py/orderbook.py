import time
from typing import Iterable, Optional, Union

from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solders.pubkey import Pubkey

from zetamarkets_py import constants, utils
from zetamarkets_py.serum_client.accounts.market_state import MarketState
from zetamarkets_py.serum_client.accounts.orderbook import OrderbookAccount
from zetamarkets_py.serum_client.types.slab import SlabInnerNode, SlabLeafNode
from zetamarkets_py.types import Network, Order, OrderInfo, Side


class Orderbook:
    """Represents an order book.

    Attributes:
        side (Side): The side of the order book.
    """

    def __init__(self, side: Side, orderbook: OrderbookAccount, market_state: MarketState) -> None:
        """Initializes the Orderbook class.

        Args:
            side (Side): The side of the order book.
            orderbook (OrderbookAccount): The orderbook account.
            market_state (MarketState): The market state.

        Raises:
            Exception: If the order book is not initialized or neither of bids or asks.
        """
        if not (orderbook.account_flags.initialized and orderbook.account_flags.bids ^ orderbook.account_flags.asks):
            raise Exception("Invalid order book, either not initialized or neither of bids or asks")
        self.side = side
        self._slab = orderbook.slab
        self._market_state = market_state

    @classmethod
    async def load(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: Commitment,
        side: Side,
        market_state: MarketState,
        program_id: Pubkey = constants.MATCHING_ENGINE_PID[Network.MAINNET],
    ) -> Optional["Orderbook"]:
        """Loads the order book.

        Args:
            conn (AsyncClient): The connection.
            address (Pubkey): The address.
            commitment (Commitment): The commitment.
            side (Side): The side.
            market_state (MarketState): The market state.
            program_id (Pubkey, optional): The program ID. Defaults to constants.MATCHING_ENGINE_PID[Network.MAINNET].

        Returns:
            Optional[Orderbook]: The order book if it exists, None otherwise.
        """
        orderbook = await OrderbookAccount.fetch(conn, address, commitment, program_id)
        if orderbook is None:
            return None
        return cls(side, orderbook, market_state)

    @staticmethod
    def _get_price_from_slab(node: Union[SlabInnerNode, SlabLeafNode]) -> int:
        """Gets the price from a slab node key.

        Args:
            node (Union[SlabInnerNode, SlabLeafNode]): The slab node.

        Returns:
            int: The price.
        """
        return node.key >> 64

    @staticmethod
    def _get_seq_num_from_slab(key: int, side: Side) -> int:
        """Gets the sequence number from a slab node key.

        Args:
            key (int): The key.
            side (Side): The side.

        Returns:
            int: The sequence number.
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

    def _is_order_expired(
        self, clock_ts: int, tif_offset: int, epoch_length: int, seq_num: int, epoch_start_seq_num: int, tif_buffer: int
    ) -> int:
        """Checks if the order is expired.

        Args:
            clock_ts (int): The clock timestamp.
            tif_offset (int): The time in force offset.
            epoch_start_ts (int): The epoch start timestamp.
            seq_num (int): The sequence number.
            epoch_start_seq_num (int): The epoch start sequence number.

        Returns:
            int: 1 if the order is expired, 0 otherwise.
        """
        if tif_offset > 0:
            # Add TIF buffer here to get into the next epoch earlier
            epoch_start_ts = (clock_ts + tif_buffer) - (clock_ts + tif_buffer) % epoch_length

            # Add TIF buffer here to account for clock drift when not around the epoch crossover
            if epoch_start_ts + tif_offset + tif_buffer < clock_ts or seq_num <= epoch_start_seq_num:
                return True

        return False

    # using local time as a hack as opposed to self.exchange.clock.account.unix_timestamp
    def _get_l2(self, depth: int, clock_ts: int = int(time.time()), tif_buffer: int = 10) -> list[OrderInfo]:
        """Gets the Level 2 market information.

        Args:
            depth (int): The depth.
            clock_ts (int, optional): The clock timestamp. Defaults to int(time.time()).

        Returns:
            list[OrderInfo]: The Level 2 market information.
        """
        descending = self.side == Side.Bid
        # The first element of the inner list is price, the second is quantity.
        levels: list[list[int]] = []
        for node in self._slab.items(descending):
            seq_num = self._get_seq_num_from_slab(node.key, self.side)
            order_expired = self._is_order_expired(
                clock_ts,
                node.tif_offset,
                self._market_state.epoch_length,
                seq_num,
                self._market_state.start_epoch_seq_num,
                tif_buffer,
            )
            if order_expired:
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
        """Returns an iterator over the orders.

        Returns:
            Iterable[Order]: An iterator over the orders.
        """
        return self.orders()

    def orders(self) -> Iterable[Order]:
        """Yields the orders.

        Yields:
            Order: The order.
        """
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
