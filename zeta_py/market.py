from __future__ import annotations
import asyncio

from typing import Any, Callable, List, Set, Type, TypeVar
from zeta_py.assets import asset_to_index
from zeta_py.constants import Asset
from zeta_py.events import EventType

from zeta_py import constants, types
from solders.pubkey import Pubkey
from solana.rpc.types import TxOpts


# TODO: update to custom serum market
from pyserum.market import AsyncMarket as SerumMarket

from zeta_py.utils import convert_native_lot_size_to_decimal


class Market:
    """
    Wrapper class for a zeta market on serum.
    """

    def __init__(
        self,
        asset: Asset,
        market_index: int,
        address: Pubkey,
        zeta_group: Pubkey,
        quote_vault: Pubkey,
        base_vault: Pubkey,
        serum_market: SerumMarket,
    ):
        """
        :param asset: The underlying asset this set of markets belong to.
        :param market_index: The market index corresponding to the zeta group account.
        :param address: The serum market address.
        :param zeta_group: The zeta group this market belongs to. TODO currently there exists only one zeta group.
        :param quote_vault: The zeta vault for the quote mint.
        :param base_vault: The zeta vault for the base mint.
        :param serum_market: The serum Market object from @project-serum/ts
        """
        self._market_index = market_index
        self._asset = asset
        self._address = address
        self._zeta_group = zeta_group
        self._quote_vault = quote_vault
        self._base_vault = base_vault
        self._serum_market = serum_market
        self._bids = None
        self._asks = None
        self._orderbook = {"bids": [], "asks": []}
        self._exchange = None

    @property
    def market_index(self) -> int:
        return self._market_index

    @property
    def asset(self) -> Asset:
        return self._asset

    @property
    def exchange(self) -> Exchange:
        return self.zeta_group.sub_exchange.exchange

    @property
    def address(self) -> Pubkey:
        return self._address

    @property
    def zeta_group(self) -> Pubkey:
        return self._zeta_group

    @property
    def quote_vault(self) -> Pubkey:
        return self._quote_vault

    @property
    def base_vault(self) -> Pubkey:
        return self._base_vault

    @property
    def serum_market(self) -> SerumMarket:
        return self._serum_market

    @property
    def bids(self) -> Orderbook:
        return self._bids

    @bids.setter
    def bids(self, bids: Orderbook):
        self._bids = bids

    @property
    def asks(self) -> Orderbook:
        return self._asks

    @asks.setter
    def asks(self, asks: Orderbook):
        self._asks = asks

    @property
    def orderbook(self) -> types.DepthOrderbook:
        return self._orderbook

    @orderbook.setter
    def orderbook(self, orderbook: types.DepthOrderbook):
        self._orderbook = orderbook

    # TODO: May need to think here about fetching all orderbooks at once as a batch using getMultipleAccountsInfo
    async def load(self):
        # update_slot = 0
        self._bids, self._asks = await asyncio.gather(
            *[
                self.serum_market.load_bids(self.exchange.provider.connection),
                self.serum_market.load_asks(self.exchange.provider.connection),
            ]
        )
        # update_slot = loaded_orderbooks.slot

        for orderbook_side in [self._bids, self._asks]:
            descending = True if orderbook_side.is_bids else False
            levels = []  # (price, size, tifOffset)
            for key, quantity, tif_offset in orderbook_side.slab.items(descending):
                seq_num = get_seq_num_from_serum_order_key(key, orderbook_side.is_bids)
                if is_order_expired(
                    tif_offset.to_number(),
                    seq_num,
                    self._serum_market.epoch_start_ts.to_number(),
                    self._serum_market.start_epoch_seq_num,
                ):
                    continue

                price = get_price_from_serum_order_key(key)
                if levels.length > 0 and levels[levels.length - 1][0].eq(price):
                    levels[levels.length - 1][1].iadd(quantity)
                else:
                    # TODO: handle bignum
                    levels.append([price, quantity.to_number()])

            self._orderbook["bids" if orderbook_side.is_bids else "asks"] = levels.map(
                lambda price_lots, size_lots: {
                    "price": self._serum_market.price_lots_to_number(price_lots),
                    "size": convert_native_lot_size_to_decimal(
                        self._serum_market.base_size_lots_to_number(size_lots)
                    ),
                }
            )

        # return update_slot

    # TODO: should this not be loaded same way as other parent classes?
    # async def update_orderbook(self) -> int:
    #     # if not load_serum, we assume that this._bids and this._asks was set elsewhere manually beforehand
    #     update_slot = 0
    #     if load_serum:
    #         loaded_orderbooks = await self.serum_market.load_bids_and_asks(
    #             Exchange.provider.connection
    #         )
    #         self._bids, self._asks = loaded_orderbooks.bids, loaded_orderbooks.asks
    #         update_slot = loaded_orderbooks.slot

    #     for orderbook_side in [self._bids, self._asks]:
    #         descending = True if orderbook_side.is_bids else False
    #         levels = []  # (price, size, tifOffset)
    #         for key, quantity, tif_offset in orderbook_side.slab.items(descending):
    #             seq_num = get_seq_num_from_serum_order_key(key, orderbook_side.is_bids)
    #             if is_order_expired(
    #                 tif_offset.to_number(),
    #                 seq_num,
    #                 self._serum_market.epoch_start_ts.to_number(),
    #                 self._serum_market.start_epoch_seq_num,
    #             ):
    #                 continue

    #             price = get_price_from_serum_order_key(key)
    #             if levels.length > 0 and levels[levels.length - 1][0].eq(price):
    #                 levels[levels.length - 1][1].iadd(quantity)
    #             else:
    #                 # TODO: handle bignum
    #                 levels.append([price, quantity.to_number()])

    #         self._orderbook["bids" if orderbook_side.is_bids else "asks"] = levels.map(
    #             lambda price_lots, size_lots: {
    #                 "price": self._serum_market.price_lots_to_number(price_lots),
    #                 "size": convert_native_lot_size_to_decimal(
    #                     self._serum_market.base_size_lots_to_number(size_lots)
    #                 ),
    #             }
    #         )

    #     return update_slot

    def get_top_level(self) -> types.TopLevel:
        top_level: types.TopLevel = {"bid": None, "ask": None}
        if len(self.orderbook.bids) != 0:
            top_level["bid"] = self.orderbook.bids[0]
        if len(self.orderbook.asks) != 0:
            top_level["ask"] = self.orderbook.asks[0]
        return top_level

    @staticmethod
    def convert_order(market: Market, order: dict) -> types.Order:
        return types.Order(
            market_index=market.market_index,
            market=market.address,
            price=order["price"],
            size=convert_native_lot_size_to_decimal(order["size"]),
            side=types.Side.BID if order["side"] == "buy" else types.Side.ASK,
            order_id=order["orderId"],
            owner=order["openOrdersAddress"],
            client_order_id=order["clientId"],
            tif_offset=order["tifOffset"],
            asset=market.asset,
        )

    def get_orders_for_account(self, open_orders_address: Pubkey) -> List[Order]:
        orders = [
            order
            for order in self._bids + self._asks
            if order.open_orders_address == open_orders_address
        ]
        return [Market._convert_order(self, order) for order in orders]

    def get_market_orders(self):
        return [self.convert_order(order) for order in self._bids + self._asks]

    def get_bid_orders(self):
        return [self.convert_order(order) for order in self._bids]

    def get_ask_orders(self):
        return [self.convert_order(order) for order in self._asks]

    async def cancel_all_orders_halted(self):
        Exchange.get_sub_exchange(self.asset).assert_halted()

        await self.update_orderbook()
        orders = self.get_market_orders()
        ixs = await get_cancel_all_ixs(self.asset, orders, False)
        txs = split_ixs_into_tx(ixs, constants.MAX_CANCELS_PER_TX)
        for tx in txs:
            await process_transaction(Exchange.provider, tx)


class ZetaGroupMarkets:
    @property
    def asset(self) -> Asset:
        return self._asset

    @property
    def sub_exchange(self) -> SubExchange:
        return self._sub_exchange

    @property
    def exchange(self) -> Exchange:
        return self.sub_exchange.exchange

    @property
    def perp_market(self) -> Market:
        return self._perp_market

    @property
    def poll_interval(self) -> int:
        return self._poll_interval

    @poll_interval.setter
    def poll_interval(self, interval: int) -> None:
        if interval < 0:
            raise ValueError("Invalid poll interval")
        self._poll_interval = interval

    @property
    def subscribed_perp(self) -> bool:
        return self._subscribed_perp

    def __init__(self, asset: Asset, sub_exchange: SubExchange):
        self._asset: Asset = asset
        self._sub_exchange: SubExchange = sub_exchange
        self._perp_market: Market = None
        self._subscribed_market_indexes: Set = set()
        self._last_poll_timestamp: int = 0
        self._subscribed_perp: bool = False

        base_vault_addr, _ = get_zeta_vault(
            self.exchange.program_id, serum_market.base_mint_address
        )
        quote_vault_addr, _ = get_zeta_vault(
            self.exchange.program_id, serum_market.quote_mint_address
        )

        # TODO: need to figure out the cached stuff, otherwise fetch
        market_addr = self.exchange.pricing.products[asset_to_index(self.asset)].market
        serum_market = None
        self._perp_market = Market(
            asset,
            constants.PERP_INDEX,  # not in use but technically sits at the end of the list of Products in the ZetaGroup
            market_addr,
            self.sub_exchange.zeta_group_address,
            quote_vault_addr,
            base_vault_addr,
            serum_market,
        )

    # TODO: when is this enabled??
    def subscribe_perp(self):
        self._subscribed_perp = True

    def unsubscribe_perp(self):
        self._subscribed_perp = False

    async def handle_polling(
        self, callback: Callable[[Asset, EventType, Any], None] = None
    ) -> None:
        if (
            self.exchange.clock_timestamp
            > self._last_poll_timestamp + self._poll_interval
        ):
            self._last_poll_timestamp = self.exchange.clock_timestamp

            if self._subscribed_perp:
                try:
                    await self._perp_market.update_orderbook()
                except Exception as e:
                    print(f"Orderbook poll failed: {e}")
                if callback is not None:
                    data: OrderbookEvent = {"market_index": constants.PERP_INDEX}
                    callback(self.asset, EventType.ORDERBOOK, data)

    async def load(
        self,
        opts: TxOpts,
        load_from_store: bool = False,
    ):
        # instance = ZetaGroupMarkets(asset)

        # Perps product/market is separate
        market_addr = self.exchange.pricing.products[asset_to_index(self.asset)].market
        if load_from_store:
            decoded = get_decoded_market(
                self.exchange.network, self.asset, constants.PERP_INDEX
            )
            # TODO: update to custom serum market
            serum_market = SerumMarket.load_from_decoded(
                decoded,
                {
                    "commitment": opts.commitment,
                    "skip_preflight": opts.skip_preflight,
                },
                constants.DEX_PID[self.exchange.network],
            )
        else:
            # serum_market = SerumMarket.load(
            #     self.exchange.connection,
            #     market_addr,
            #     {
            #         "commitment": opts.commitment,
            #         "skip_preflight": opts.skip_preflight,
            #     },
            #     constants.DEX_PID[self.exchange.network],
            # )
            serum_market = SerumMarket.load(
                self.exchange.connection,
                market_addr,
                constants.DEX_PID[self.exchange.network],
            )

        # base_vault_addr, _base_vault_nonce = get_zeta_vault(
        #     self.exchange.program_id, serum_market.base_mint_address
        # )
        # quote_vault_addr, _quote_vault_nonce = get_zeta_vault(
        #     self.exchange.program_id, serum_market.quote_mint_address
        # )

        # self._perp_market = Market(
        #     asset,
        #     constants.PERP_INDEX,  # not in use but technically sits at the end of the list of Products in the ZetaGroup
        #     market_addr,
        #     self.sub_exchange.zeta_group_address,
        #     quote_vault_addr,
        #     base_vault_addr,
        #     serum_market,
        # )

    # Factory method
    @classmethod
    async def create(
        cls,
        asset: Asset,
        market_index: int,
        address: Pubkey,
        zeta_group: Pubkey,
        quote_vault: Pubkey,
        base_vault: Pubkey,
        serum_market: SerumMarket,
        sub_exchange: SubExchange,
        opts: TxOpts,
        load_from_store: bool = False,
    ) -> "ZetaGroupMarkets":
        obj = cls(
            asset,
            market_index,
            address,
            zeta_group,
            quote_vault,
            base_vault,
            serum_market,
            sub_exchange,
        )
        await obj.load(
            opts,
            load_from_store,
        )

    def get_market(self, market: Pubkey) -> Market:
        index = self.get_market_index(market)
        return (
            self._perp_market if index == constants.PERP_INDEX else self._markets[index]
        )

    def get_market_index(self, market: Pubkey) -> int:
        if market == self.sub_exchange.markets.perp_market.address:
            return constants.PERP_INDEX
        else:
            raise Exception(
                "Cannot get market index of non perp market on perp only market!"
            )
