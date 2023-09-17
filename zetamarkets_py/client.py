import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Optional, TypeVar

from anchorpy import Event, EventParser, Provider, Wallet
from anchorpy.provider import DEFAULT_OPTIONS
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment, Confirmed
from solana.rpc.core import RPCException
from solana.rpc.types import TxOpts
from solana.rpc.websocket_api import connect
from solders.instruction import Instruction
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.rpc.config import RpcTransactionLogsFilterMentions
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.sysvar import RENT
from solders.transaction import VersionedTransaction
from spl.token.constants import TOKEN_PROGRAM_ID

from zetamarkets_py import constants, pda, utils
from zetamarkets_py.events import (
    LiquidationEvent,
    OrderCompleteEvent,
    TradeEventV3,
    TransactionEventType,
)
from zetamarkets_py.exchange import Exchange
from zetamarkets_py.orderbook import Orderbook
from zetamarkets_py.serum_client.accounts.orderbook import OrderbookAccount
from zetamarkets_py.types import Asset, Network, OrderOptions, Position, Side
from zetamarkets_py.zeta_client.accounts.cross_margin_account import CrossMarginAccount
from zetamarkets_py.zeta_client.errors import from_tx_error
from zetamarkets_py.zeta_client.instructions import (
    cancel_all_market_orders,
    cancel_order,
    deposit_v2,
    initialize_cross_margin_account,
    initialize_cross_margin_account_manager,
    initialize_open_orders_v3,
    place_perp_order_v3,
)


@dataclass
class Client:
    """
    Cross margin client
    """

    provider: Provider
    network: Network
    connection: AsyncClient
    endpoint: str
    ws_endpoint: str
    exchange: Exchange
    margin_account: CrossMarginAccount

    _margin_account_address: Optional[Pubkey]
    _open_orders_addresses: Optional[dict[Asset, Pubkey]]
    _margin_account_manager_address: Optional[Pubkey]
    _user_usdc_address: Optional[Pubkey]
    _combined_vault_address: Pubkey
    _combined_socialized_loss_address: Pubkey
    _logger: logging.Logger

    @classmethod
    async def load(
        cls,
        endpoint: str,
        ws_endpoint: str = None,
        commitment: Commitment = Confirmed,
        wallet: Wallet = None,
        assets: list[Asset] = Asset.all(),
        tx_opts: TxOpts = DEFAULT_OPTIONS,
        network: Network = Network.MAINNET,
    ):
        """
        Create a new client
        """
        logger = logging.getLogger(f"{__name__}.{cls.__name__}")
        connection = AsyncClient(endpoint=endpoint, commitment=commitment, blockhash_cache=False)
        exchange = await Exchange.load(
            network=network,
            connection=connection,
            assets=assets,
        )
        if wallet is None:
            wallet = Wallet.dummy()
            logger.warning("Client in read-only mode, pass in `wallet` to enable transactions")
            _margin_account_manager_address = None
            _user_usdc_address = None
            _margin_account_address = None
            margin_account = None
            _open_orders_addresses = None
        else:
            _margin_account_manager_address = pda.get_cross_margin_account_manager_address(
                exchange.program_id, wallet.public_key
            )
            _user_usdc_address = pda.get_associated_token_address(wallet.public_key, constants.USDC_MINT[network])
            _margin_account_address = pda.get_margin_account_address(exchange.program_id, wallet.public_key, 0)
            margin_account = await CrossMarginAccount.fetch(connection, _margin_account_address, connection.commitment)
            _open_orders_addresses = {}
            for asset in assets:
                open_orders_address = pda.get_open_orders_address(
                    exchange.program_id,
                    constants.DEX_PID[network],
                    exchange.markets[asset].address,
                    _margin_account_address,
                )
                _open_orders_addresses[asset] = open_orders_address
        if ws_endpoint is None:
            ws_endpoint = utils.cluster_endpoint(network, ws=True, whirligig=False)
        provider = Provider(
            connection,
            wallet,
            tx_opts,
        )

        # additional addresses to cache
        _combined_vault_address = pda.get_combined_vault_address(exchange.program_id)
        _combined_socialized_loss_address = pda.get_combined_socialized_loss_address(exchange.program_id)

        return cls(
            provider,
            network,
            connection,
            endpoint,
            ws_endpoint,
            exchange,
            margin_account,
            _margin_account_address,
            _open_orders_addresses,
            _margin_account_manager_address,
            _user_usdc_address,
            _combined_vault_address,
            _combined_socialized_loss_address,
            logger,
        )

    async def _check_user_usdc_account_exists(self):
        if not hasattr(self, "_user_usdc_account_exists"):
            # If they don't have USDC wallet this will be null
            resp = await self.connection.get_account_info(self._user_usdc_address)
            self._user_usdc_account_exists = resp.value is not None
        return self._user_usdc_account_exists

    async def _check_margin_account_manager_exists(self):
        if not hasattr(self, "_margin_account_manager_exists"):
            # If they don't have margin account manager this will be null
            resp = await self.connection.get_account_info(self._margin_account_manager_address)
            self._margin_account_manager_exists = resp.value is not None
        return self._margin_account_manager_exists

    async def _check_margin_account_exists(self):
        if not hasattr(self, "_margin_account_exists"):
            # If they don't have margin account this will be null
            resp = await self.connection.get_account_info(self._margin_account_address)
            self._margin_account_exists = resp.value is not None
        return self._margin_account_exists

    async def _check_open_orders_account_exists(self, asset: Asset):
        if not hasattr(self, "_open_orders_account_exists"):
            self._open_orders_account_exists = {}
        if asset not in self._open_orders_account_exists:
            resp = await self.connection.get_account_info(self._open_orders_addresses[asset])
            self._open_orders_account_exists[asset] = resp.value is not None
        return self._open_orders_account_exists[asset]

    async def fetch_balance(self):
        margin_account = await self.margin_account.fetch(
            self.connection, self._margin_account_address, self.connection.commitment
        )
        balance = utils.convert_fixed_int_to_decimal(margin_account.balance)
        return balance

    async def fetch_position(self, asset: Asset):
        margin_account = await self.margin_account.fetch(
            self.connection, self._margin_account_address, self.connection.commitment
        )
        position = Position(
            utils.convert_fixed_lot_to_decimal(margin_account.product_ledgers[asset.to_index()].position.size),
            utils.convert_fixed_int_to_decimal(
                margin_account.product_ledgers[asset.to_index()].position.cost_of_trades
            ),
        )
        return position

    async def fetch_open_orders(self, asset: Asset):
        oo = await self.exchange.markets[asset].load_orders_for_owner(self._open_orders_addresses[asset])
        # TODO: caching layer
        # self.open_orders[asset] = oo
        return oo

    AccountType = TypeVar("AccountType")

    async def _account_subscribe(
        self,
        address: Pubkey,
        ws_endpoint: str,
        commitment: Commitment,
        callback: Callable[[AccountType], Any],
        max_retries: int = 3,
        encoding: str = "base64+zstd",
    ) -> None:
        retries = max_retries
        while True:
            async with connect(ws_endpoint) as ws:
                try:
                    await ws.account_subscribe(
                        address,
                        commitment=commitment,
                        encoding=encoding,
                    )
                    first_resp = await ws.recv()
                    subscription_id = first_resp[0].result
                    async for msg in ws:
                        await callback(msg[0].result.value.data)
                    await ws.account_unsubscribe(subscription_id)
                except asyncio.CancelledError:
                    self._logger.info("WebSocket subscription task cancelled.")
                    break
                # solana_py.SubscriptionError?
                except Exception as e:
                    self._logger.error(f"Error subscribing to {self.__class__.__name__}: {e}")
                    retries -= 1
                    await asyncio.sleep(2)  # Pause for a while before retrying
                finally:
                    # self._subscription_task = None
                    pass

    async def subscribe_orderbook(self, asset: Asset, side: Side, callback: Callable[[Orderbook], Awaitable[Any]]):
        ws_endpoint = utils.cluster_endpoint(self.network, ws=True, whirligig=False)
        address = (
            self.exchange.markets[asset]._market_state.bids
            if side == Side.Bid
            else self.exchange.markets[asset]._market_state.asks
        )

        # Wrap callback in order to parse account data correctly
        async def _callback(data: bytes):
            account = OrderbookAccount.decode(data)
            orderbook = Orderbook(side, account, self.exchange.markets[asset]._market_state)
            return await callback(orderbook)

        self._logger.info(f"Subscribing to Orderbook:{side}.")
        await self._account_subscribe(
            address,
            ws_endpoint,
            self.connection.commitment,
            _callback,
        )

    # TODO: add retry logic
    # TODO: decode and format event data
    async def subscribe_transaction(
        self,
        order_complete_callback: Callable[[OrderCompleteEvent], Awaitable[Any]],
        trade_callback: Callable[[TradeEventV3], Awaitable[Any]],
        liquidation_callback: Callable[[LiquidationEvent], Awaitable[Any]],
    ):
        async with connect(self.ws_endpoint) as ws:
            await ws.logs_subscribe(
                commitment=self.connection.commitment,
                filter_=RpcTransactionLogsFilterMentions(self.exchange.program_id),
            )
            first_resp = await ws.recv()
            first_resp[0].result
            async for msg in ws:
                logs = msg[0].result.value.logs
                parser = EventParser(self.exchange.program_id, self.exchange.program.coder)
                parsed: list[Event] = []
                parser.parse_logs(logs, lambda evt: parsed.append(evt))
                for event in parsed:
                    if event.name == TransactionEventType.ORDERCOMPLETE.value:
                        if event.data.margin_account == self._margin_account_address:
                            await order_complete_callback(event)
                    elif event.name == TransactionEventType.TRADE.value:
                        if event.data.margin_account == self._margin_account_address:
                            await trade_callback(event)
                    elif event.name == TransactionEventType.LIQUIDATION.value:
                        if event.data.margin_account == self._margin_account_address:
                            await liquidation_callback(event)
                    else:
                        pass

    # Instructions

    async def deposit(self, amount: float, subaccount_index: int = 0):
        ixs = await self._deposit_ixs(amount, subaccount_index)
        self._logger.info(f"Depositing {amount} USDC to margin account")
        return await self._send_versioned_transaction(ixs)

    async def _deposit_ixs(self, amount: float, subaccount_index: int = 0) -> list[Instruction]:
        ixs = []
        if not await self._check_margin_account_manager_exists():
            self._logger.info("User has no cross-margin account manager, creating one...")
            ixs.append(
                initialize_cross_margin_account_manager(
                    {
                        "cross_margin_account_manager": self._margin_account_manager_address,
                        "authority": self.provider.wallet.public_key,
                        "payer": self.provider.wallet.public_key,
                        "zeta_program": self.exchange.program_id,
                    }
                )
            )
        # Create margin account if user doesn't have one
        if not await self._check_margin_account_exists():
            self._logger.info("User has no cross-margin account manager, creating one...")
            ixs.append(
                initialize_cross_margin_account(
                    {"subaccount_index": subaccount_index},
                    {
                        "cross_margin_account": self._margin_account_address,
                        "cross_margin_account_manager": self._margin_account_manager_address,
                        "authority": self.provider.wallet.public_key,
                        "payer": self.provider.wallet.public_key,
                        "zeta_program": self.exchange.program_id,
                    },
                )
            )
        # Check they have an existing USDC account
        if await self._check_user_usdc_account_exists():
            ixs.append(
                deposit_v2(
                    {"amount": utils.convert_decimal_to_fixed_int(amount)},
                    {
                        "margin_account": self._margin_account_address,
                        "vault": self._combined_vault_address,
                        "user_token_account": self._user_usdc_address,
                        "socialized_loss_account": self._combined_socialized_loss_address,
                        "authority": self.provider.wallet.public_key,
                        "state": self.exchange._state_address,
                        "pricing": self.exchange._pricing_address,
                    },
                )
            )
        else:
            raise Exception("User has no USDC, cannot deposit to margin account")

        return ixs

    # TODO: withdraw (and optionally close)
    async def withdraw(self):
        raise NotImplementedError

    async def place_order(
        self, asset: Asset, price: float, size: float, side: Side, order_opts: OrderOptions = OrderOptions
    ):
        ixs = await self._place_order_ixs(asset, price, size, side, order_opts)
        self._logger.info(f"Placed {size}x {asset}-PERP {side.name} @ ${price}")
        return await self._send_versioned_transaction(ixs)

    async def _place_order_ixs(
        self, asset: Asset, price: float, size: float, side: Side, order_opts: OrderOptions = OrderOptions
    ) -> list[Instruction]:
        if asset not in self.exchange.assets:
            raise Exception(f"Asset {asset.name} not loaded into client, cannot place order")
        ixs = []
        if not await self._check_open_orders_account_exists(asset):
            self._logger.info("User has no open orders account, creating one...")
            ixs.append(
                initialize_open_orders_v3(
                    {"asset": asset.to_program_type()},
                    {
                        "state": self.exchange._state_address,
                        "dex_program": constants.DEX_PID[self.network],
                        "system_program": SYS_PROGRAM_ID,
                        "open_orders": self._open_orders_addresses[asset],
                        "cross_margin_account": self._margin_account_address,
                        "authority": self.provider.wallet.public_key,
                        "payer": self.provider.wallet.public_key,
                        "market": self.exchange.markets[asset].address,
                        "serum_authority": self.exchange._serum_authority_address,
                        "open_orders_map": pda.get_open_orders_map_address(
                            self.exchange.program_id, self._open_orders_addresses[asset]
                        ),
                        "rent": RENT,
                    },
                )
            )
        unix_timestamp = int(time.time())
        tif_offset = (
            utils.get_tif_offset(
                order_opts.expiry_ts,
                self.exchange.markets[asset]._market_state.epoch_length,
                unix_timestamp,  # self.exchange.clock.account.unix_timestamp,
            )
            if order_opts.expiry_ts
            else None
        )
        ixs.append(
            place_perp_order_v3(
                {
                    "price": utils.convert_decimal_to_fixed_int(price),
                    "size": utils.convert_decimal_to_fixed_lot(size),
                    "side": side.to_program_type(),
                    "order_type": order_opts.order_type.to_program_type(),
                    "client_order_id": order_opts.client_order_id,
                    "tif_offset": tif_offset,
                    "tag": order_opts.tag,
                    "asset": asset.to_program_type(),
                },
                {
                    "state": self.exchange._state_address,
                    "pricing": self.exchange._pricing_address,
                    "margin_account": self._margin_account_address,
                    "authority": self.provider.wallet.public_key,
                    "dex_program": constants.DEX_PID[self.network],
                    "token_program": TOKEN_PROGRAM_ID,
                    "serum_authority": self.exchange._serum_authority_address,
                    "open_orders": self._open_orders_addresses[asset],
                    "rent": RENT,
                    "market_accounts": {
                        "market": self.exchange.markets[asset].address,
                        "request_queue": self.exchange.markets[asset]._market_state.request_queue,
                        "event_queue": self.exchange.markets[asset]._market_state.event_queue,
                        "bids": self.exchange.markets[asset]._market_state.bids,
                        "asks": self.exchange.markets[asset]._market_state.asks,
                        "coin_vault": self.exchange.markets[asset]._market_state.base_vault,
                        "pc_vault": self.exchange.markets[asset]._market_state.quote_vault,
                        "order_payer_token_account": self.exchange.markets[asset]._quote_zeta_vault_address
                        if side == Side.Bid
                        else self.exchange.markets[asset]._base_zeta_vault_address,
                        "coin_wallet": self.exchange.markets[asset]._base_zeta_vault_address,
                        "pc_wallet": self.exchange.markets[asset]._quote_zeta_vault_address,
                    },
                    "oracle": self.exchange.pricing.oracles[asset.to_index()],
                    "oracle_backup_feed": self.exchange.pricing.oracle_backup_feeds[asset.to_index()],
                    "oracle_backup_program": constants.CHAINLINK_PID,
                    "market_mint": self.exchange.markets[asset]._market_state.quote_mint
                    if side == Side.Bid
                    else self.exchange.markets[asset]._market_state.base_mint,
                    "mint_authority": self.exchange._mint_authority_address,
                    "perp_sync_queue": self.exchange.pricing.perp_sync_queues[asset.to_index()],
                },
            )
        )
        return ixs

    async def cancel_order(self, asset: Asset, order_id: int, side: Side):
        ixs = self._cancel_order_ixs(asset, order_id, side)
        self._logger.info(f"Cancelling order {order_id} for {asset}")
        return await self._send_versioned_transaction(ixs)

    def _cancel_order_ixs(self, asset: Asset, order_id: int, side: Side) -> list[Instruction]:
        ixs = []
        ixs.append(
            cancel_order(
                {"side": side.to_program_type(), "order_id": order_id, "asset": asset.to_program_type()},
                {
                    "authority": self.provider.wallet.public_key,
                    "cancel_accounts": {
                        "state": self.exchange._state_address,
                        "margin_account": self._margin_account_address,
                        "dex_program": constants.DEX_PID[self.network],
                        "serum_authority": self.exchange._serum_authority_address,
                        "open_orders": self._open_orders_addresses[asset],
                        "market": self.exchange.markets[asset].address,
                        "bids": self.exchange.markets[asset]._market_state.bids,
                        "asks": self.exchange.markets[asset]._market_state.asks,
                        "event_queue": self.exchange.markets[asset]._market_state.event_queue,
                    },
                },
            )
        )
        return ixs

    # TODO: cancelorderbyclientorderid

    def _cancel_orders_for_market_ixs(self, asset: Asset):
        ixs = []
        ixs.append(
            cancel_all_market_orders(
                {"asset": asset.to_program_type()},
                {
                    "authority": self.provider.wallet.public_key,
                    "cancel_accounts": {
                        "state": self.exchange._state_address,
                        "margin_account": self._margin_account_address,
                        "dex_program": constants.DEX_PID[self.network],
                        "serum_authority": self.exchange._serum_authority_address,
                        "open_orders": self._open_orders_addresses[asset],
                        "market": self.exchange.markets[asset].address,
                        "bids": self.exchange.markets[asset]._market_state.bids,
                        "asks": self.exchange.markets[asset]._market_state.asks,
                        "event_queue": self.exchange.markets[asset]._market_state.event_queue,
                    },
                },
            )
        )
        return ixs

    async def cancel_orders_for_market(self, asset: Asset):
        ixs = self._cancel_orders_for_market_ixs(asset)
        self._logger.info(f"Cancelling all orders for {asset}")
        return await self._send_versioned_transaction(ixs)

    async def replace_quote(
        self,
        asset: Asset,
        bid_price: float,
        bid_size: float,
        ask_price: float,
        ask_size: float,
        order_opts: OrderOptions = OrderOptions,
    ):
        cancel_ixs = self._cancel_orders_for_market_ixs(asset)
        bid_place_ixs = await self._place_order_ixs(asset, bid_price, bid_size, Side.Bid, order_opts)
        ask_place_ixs = await self._place_order_ixs(asset, ask_price, ask_size, Side.Ask, order_opts)
        ixs = cancel_ixs + bid_place_ixs + ask_place_ixs
        self._logger.info(
            f"Replacing {asset} orders: {bid_size}x {Side.Bid.name} @ ${bid_price}, {ask_size}x {Side.Ask.name} @ ${ask_price}"
        )
        return await self._send_versioned_transaction(ixs)

    # TODO: liquidate
    async def liquidate(self):
        raise NotImplementedError

    async def _send_versioned_transaction(self, ixs):
        # TODO: prefetch blockhash (look into blockhash cache)
        recent_blockhash = (
            self.connection.blockhash_cache.get()
            if self.connection.blockhash_cache
            else (await self.connection.get_latest_blockhash(constants.BLOCKHASH_COMMITMENT)).value.blockhash
        )
        msg = MessageV0.try_compile(
            self.provider.wallet.public_key, ixs, [constants.ZETA_LUT[self.network]], recent_blockhash
        )
        tx = VersionedTransaction(msg, [self.provider.wallet.payer])
        try:
            signature = await self.provider.send(tx)
        except RPCException as exc:
            # This won't work on zDEX errors
            parsed = from_tx_error(exc)
            self._logger.error(parsed)
            if parsed is not None:
                raise parsed from exc
            raise exc
        return signature
