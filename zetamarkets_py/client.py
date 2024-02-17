import json
import logging
import time
import traceback
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Union, cast

import anchorpy
import based58
import websockets
import websockets.exceptions  # force eager imports
import websockets.legacy.client  # force eager imports
from anchorpy import Event, Provider, Wallet
from anchorpy.provider import DEFAULT_OPTIONS
from construct import Container
from jsonrpcclient import request
from solana.blockhash import BlockhashCache
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment, Confirmed
from solana.rpc.core import RPCException
from solana.rpc.types import TxOpts
from solana.rpc.websocket_api import connect
from solders.compute_budget import set_compute_unit_price
from solders.instruction import Instruction
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.rpc.config import RpcTransactionLogsFilterMentions
from solders.transaction import VersionedTransaction

from zetamarkets_py import constants, pda, utils
from zetamarkets_py.events import (
    ApplyFundingEvent,
    CancelOrderEvent,
    EventMeta,
    LiquidationEvent,
    OrderCompleteEvent,
    PlaceOrderEvent,
    PlaceOrderEventWithArgs,
    TradeEvent,
    ZetaEnrichedEvent,
    ZetaEvent,
)
from zetamarkets_py.exchange import Exchange
from zetamarkets_py.orderbook import Orderbook
from zetamarkets_py.risk import AccountRiskSummary, Position
from zetamarkets_py.serum_client.accounts.orderbook import OrderbookAccount
from zetamarkets_py.solana_client.accounts.clock import CLOCK, Clock
from zetamarkets_py.types import (
    Asset,
    Network,
    OrderArgs,
    OrderCompleteType,
    OrderOptions,
    Side,
)
from zetamarkets_py.zeta_client.accounts.cross_margin_account import CrossMarginAccount
from zetamarkets_py.zeta_client.accounts.pricing import Pricing
from zetamarkets_py.zeta_client.errors import from_tx_error
from zetamarkets_py.zeta_client.instructions import (
    cancel_all_market_orders,
    cancel_order,
    deposit_v2,
    initialize_cross_margin_account,
    initialize_cross_margin_account_manager,
    initialize_open_orders_v3,
    place_perp_order_v4,
)

# TODO: add docstrings for most methods
# TODO: implement withdraw and liquidation
# TODO: implement priority fees to exchange


@dataclass
class Client:
    """
    This class represents the Zeta Client. It contains all the necessary attributes and methods
    for interacting with the Zeta Exchange from the user side, including loading the client, fetching state and pricing,
    and handling various market assets.

    Note:
        Loading the client is asynchronous, so it is recommended to use :func:`load` to
        initialize the client.
    """

    provider: Provider
    """The network and wallet context to send transactions paid for and signed by the provider."""
    network: Network
    """The Solana network identifier (i.e. mainnet_beta, devnet etc.)."""
    connection: AsyncClient
    """The connection to the Solana network."""
    endpoint: str
    "The http(s) RPC endpoint."
    ws_endpoint: str
    """The websocket RPC endpoint."""
    exchange: Exchange
    """The Zeta Exchange object."""

    margin_account: Optional[CrossMarginAccount]
    """The margin account of the Zeta program."""

    _margin_account_address: Optional[Pubkey]
    _open_orders_addresses: Optional[dict[Asset, Pubkey]]
    _margin_account_manager_address: Optional[Pubkey]
    _user_usdc_address: Optional[Pubkey]
    _combined_vault_address: Pubkey
    _combined_socialized_loss_address: Pubkey
    _logger: logging.Logger
    _account_exists_cache: dict[Pubkey, bool] = field(default_factory=dict)

    @classmethod
    async def load(
        cls,
        endpoint: Optional[str] = None,
        ws_endpoint: Optional[str] = None,
        commitment: Commitment = Confirmed,
        wallet: Optional[Wallet] = None,
        assets: list[Asset] = Asset.all(),
        tx_opts: TxOpts = DEFAULT_OPTIONS,
        network: Network = Network.MAINNET,
        log_level: int = logging.WARNING,
        blockhash_cache: Union[BlockhashCache, bool] = False,
        delegator_pubkey: Optional[Pubkey] = None,
    ):
        """
        Asynchronously load the Zeta Client.

        Args:
            endpoint (str, optional): The http(s) RPC endpoint. Defaults to None.
            ws_endpoint (str, optional): The websocket RPC endpoint. Defaults to None.
            commitment (Commitment, optional): The commitment level of the Solana network. Defaults to Confirmed.
            wallet (Wallet, optional): The wallet used for transactions. Defaults to None.
            assets (list[Asset], optional): The list of assets to be used. Defaults to all available assets.
            tx_opts (TxOpts, optional): Transaction options. Defaults to DEFAULT_OPTIONS.
            network (Network, optional): The network of the Zeta program. Defaults to Network.MAINNET.
            log_level (int, optional): The level of logging. Defaults to logging.CRITICAL.
            blockhash_cache (Union[BlockhashCache, bool], optional): The blockhash cache. Disabled by default.
            delegator_pubkey (Pubkey, optional): If passing in a delegated wallet in the 'wallet' param, this
            is the delegator account itself so you can load positions/orders/balance/etc

        Returns:
            Client: An instance of the Client class.
        """
        logger = utils.create_logger(f"{__name__}.{cls.__name__}", log_level)

        if endpoint is None:
            endpoint = utils.cluster_endpoint(network)
        if ws_endpoint is None:
            ws_endpoint = utils.http_to_ws(endpoint)
        connection = AsyncClient(endpoint=endpoint, commitment=commitment, blockhash_cache=blockhash_cache)
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
            key = wallet.public_key if delegator_pubkey is None else delegator_pubkey

            _margin_account_manager_address = pda.get_cross_margin_account_manager_address(exchange.program_id, key)
            _user_usdc_address = pda.get_associated_token_address(key, constants.USDC_MINT[network])
            _margin_account_address = pda.get_margin_account_address(exchange.program_id, key, 0)
            margin_account = await CrossMarginAccount.fetch(
                connection, _margin_account_address, connection.commitment, exchange.program_id
            )
            _open_orders_addresses = {}
            for asset in assets:
                open_orders_address = pda.get_open_orders_address(
                    exchange.program_id,
                    constants.MATCHING_ENGINE_PID[network],
                    exchange.markets[asset].address,
                    _margin_account_address,
                )
                _open_orders_addresses[asset] = open_orders_address
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
        """
        Check if the user's USDC account exists.

        Returns:
            bool: True if the account exists, False otherwise.
        """
        if self._user_usdc_address in self._account_exists_cache:
            return self._account_exists_cache[self._user_usdc_address]
        resp = await self.connection.get_account_info(self._user_usdc_address)
        exists = resp.value is not None
        if exists:
            self._account_exists_cache[self._user_usdc_address] = exists
        return exists

    async def _check_margin_account_manager_exists(self):
        """
        Check if the margin account manager exists.

        Returns:
            bool: True if the account manager exists, False otherwise.
        """
        if self._margin_account_manager_address in self._account_exists_cache:
            return self._account_exists_cache[self._margin_account_manager_address]
        resp = await self.connection.get_account_info(self._margin_account_address)
        exists = resp.value is not None
        if exists:
            self._account_exists_cache[self._margin_account_manager_address] = exists
        return exists

    async def _check_margin_account_exists(self):
        """
        Check if the margin account exists.

        Returns:
            bool: True if the account exists, False otherwise.
        """
        if self._margin_account_address in self._account_exists_cache:
            return self._account_exists_cache[self._margin_account_address]
        account = await CrossMarginAccount.fetch(self.connection, self._margin_account_address)
        exists = account is not None
        if exists:
            self._account_exists_cache[self._margin_account_address] = exists
            self.margin_account = account
        return exists

    async def _check_open_orders_account_exists(self, asset: Asset):
        """
        Check if the open orders account for a specific asset exists.

        Args:
            asset (Asset): The asset for which to check the open orders account.

        Raises:
            Exception: If the open orders accounts are not loaded.

        Returns:
            bool: True if the open orders account exists, False otherwise.
        """
        if self._open_orders_addresses is None:
            raise Exception("Open orders accounts not loaded, cannot check if account exists")
        open_orders_address = self._open_orders_addresses[asset]
        if open_orders_address in self._account_exists_cache:
            return self._account_exists_cache[open_orders_address]
        resp = await self.connection.get_account_info(open_orders_address)
        exists = resp.value is not None
        if exists:
            self._account_exists_cache[open_orders_address] = exists
        return exists

    async def fetch_margin_state(self):
        """
        Fetch the state of the margin account.

        Raises:
            Exception: If the margin account is not loaded or not found.

        Returns:
            Tuple[Decimal, Dict[Asset, zetamarkets_py.types.Position]]: The balance and positions of the margin account.
        """
        if self.margin_account is None or self._margin_account_address is None:
            raise Exception("Margin account not loaded, cannot fetch margin account state")
        margin_account = await self.margin_account.fetch(
            self.connection, self._margin_account_address, program_id=self.exchange.program_id
        )
        if margin_account is None:
            raise Exception("Margin account not found, cannot fetch margin state")
        balance = utils.convert_fixed_int_to_decimal(margin_account.balance)
        positions = {
            Asset.from_index(i): Position.from_margin_account(margin_account, i)
            for i in range(len(self.exchange.assets))
        }
        return balance, positions

    async def get_account_risk_summary(self):
        """
        Get the risk summary of the account.

        This method fetches the margin state of the account, calculates the equity, margin parameters, margin usage,
        and leverage, and returns an AccountRiskSummary object.

        Returns:
            AccountRiskSummary: The risk summary of the account.
        """
        # Batched RPC call to margin acc and prices
        account_infos = await anchorpy.utils.rpc.get_multiple_accounts(
            self.connection, [self._margin_account_address, self.exchange._pricing_address]
        )
        margin_account = CrossMarginAccount.decode(account_infos[0].account.data)
        pricing_account = Pricing.decode(account_infos[1].account.data)
        return AccountRiskSummary.from_margin_and_pricing_accounts(margin_account, pricing_account)

    async def fetch_open_orders(self, asset: Asset):
        """
        Fetch the open orders for a specific asset.

        Args:
            asset (Asset): The asset for which to fetch the open orders.

        Raises:
            Exception: If the open orders accounts are not loaded.

        Returns:
            List[Order]: The open orders for the asset.
        """
        if self._open_orders_addresses is None:
            raise Exception("Open orders accounts not loaded, cannot fetch open orders")
        oo = await self.exchange.markets[asset].load_orders_for_owner(self._open_orders_addresses[asset])
        return oo

    async def fetch_clock(self):
        """
        Fetch the Solana clock.

        Raises:
            Exception: If the clock is not found.

        Returns:
            Clock: The clock.
        """
        clock = await Clock.fetch(self.connection)
        if clock is None:
            raise Exception("Clock not found, cannot fetch clock")
        return clock

    async def _account_subscribe(
        self,
        address: Pubkey,
        commitment: Commitment,
        encoding: str = "base64+zstd",
    ) -> AsyncIterator[Tuple[bytes, int]]:
        """
        Subscribe to an account and yield account data and slot.

        Args:
            address (Pubkey): The public key of the account to subscribe to.
            commitment (Commitment): The commitment level to use for the subscription.
            encoding (str, optional): The encoding to use for the subscription. Defaults to "base64+zstd".

        Yields:
            AsyncIterator[Tuple[bytes, int]]: An async iterator that yields tuples of account data and slot.
        """
        async for ws in connect(self.ws_endpoint):
            try:
                await ws.account_subscribe(  # type: ignore
                    address,
                    commitment=commitment,
                    encoding=encoding,
                )
                first_resp = await ws.recv()
                subscription_id = cast(int, first_resp[0].result)  # type: ignore
                async for msg in ws:
                    try:
                        slot = int(msg[0].result.context.slot)  # type: ignore
                        account_bytes = cast(bytes, msg[0].result.value.data)  # type: ignore
                        yield account_bytes, slot
                    except Exception:
                        self._logger.error(f"Error processing account data: {traceback.format_exc()}")
                        break
                await ws.account_unsubscribe(subscription_id)  # type: ignore
            except websockets.exceptions.ConnectionClosed:
                self._logger.warning("Websocket closed, reconnecting...")
                continue

    async def subscribe_orderbook(
        self, asset: Asset, side: Side, commitment: Optional[Commitment] = None
    ) -> AsyncIterator[Tuple[Orderbook, int]]:
        """
        Subscribe to an orderbook and yield orderbook data and slot.

        Args:
            asset (Asset): The asset for which to subscribe to the orderbook.
            side (Side): The side of the orderbook to subscribe to.
            commitment (Commitment, optional): The commitment level to use for the subscription. Defaults to None.

        Yields:
            AsyncIterator[Tuple[Orderbook, int]]: An async iterator that yields tuples of orderbook data and slot.
        """
        commitment = commitment or self.connection.commitment
        address = (
            self.exchange.markets[asset]._market_state.bids
            if side == Side.Bid
            else self.exchange.markets[asset]._market_state.asks
        )

        self._logger.info(f"Subscribing to Orderbook:{side}.")
        async for account_bytes, slot in self._account_subscribe(address, commitment):
            account = OrderbookAccount.decode(account_bytes)
            orderbook = Orderbook(side, account, self.exchange.markets[asset]._market_state)
            yield orderbook, slot

    async def subscribe_clock(self, commitment: Optional[Commitment] = None) -> AsyncIterator[Tuple[Clock, int]]:
        """
        Subscribe to a clock and yield clock data and slot.

        Args:
            commitment (Commitment, optional): The commitment level to use for the subscription. Defaults to None.

        Yields:
            AsyncIterator[Tuple[Clock, int]]: An async iterator that yields tuples of clock data and slot.
        """
        commitment = commitment or self.connection.commitment

        self._logger.info("Subscribing to Clock")
        async for account_bytes, slot in self._account_subscribe(CLOCK, commitment):
            clock = Clock.decode(account_bytes)
            yield clock, slot

    # TODO: maybe at some point support subscribing to all exchange events, not just margin account
    async def subscribe_events(
        self,
        commitment: Optional[Commitment] = None,
    ) -> AsyncIterator[Tuple[List[ZetaEvent], EventMeta]]:
        """
        Subscribe to events and yield event data and slot.

        Args:
            commitment (Commitment, optional): The commitment level to use for the subscription. Defaults to None.

        Yields:
            AsyncIterator[Tuple[List[ZetaEvent], int]]: An async iterator that yields tuples of event data and slot.
        """
        if self._margin_account_address is None:
            raise Exception("Margin account not loaded, cannot subscribe to events")
        commitment = commitment or self.connection.commitment
        async for ws in connect(self.ws_endpoint):
            try:
                # Subscribe to logs that mention the margin account
                await ws.logs_subscribe(  # type: ignore
                    commitment=commitment,
                    filter_=RpcTransactionLogsFilterMentions(self._margin_account_address),
                )
                first_resp = await ws.recv()
                subscription_id = cast(int, first_resp[0].result)  # type: ignore
                async for msg in ws:
                    try:
                        events, meta = self._parse_event_payload(msg)
                        if len(events) > 0 or not meta.is_successful:
                            yield events, meta

                    except Exception:
                        self._logger.error(f"Error processing event data: {traceback.format_exc()}")
                        break
                await ws.logs_unsubscribe(subscription_id)  # type: ignore
            except websockets.exceptions.ConnectionClosed:
                self._logger.warning("Websocket closed, reconnecting...")
                continue

    def _parse_event_payload(self, msg) -> Tuple[List[ZetaEvent], EventMeta]:
        """
        Parse the event payload from the message.

        Args:
            msg: The message received from the websocket.

        Returns:
            Tuple[List[ZetaEvent], int]: A tuple containing a list of ZetaEvents and the slot number.
        """
        slot = int(msg[0].result.context.slot)
        logs = cast(list[str], msg[0].result.value.logs)  # type: ignore
        error = msg[0].result.value.err
        meta = EventMeta(slot, error)
        if error is not None:
            return [], meta

        parsed: list[Event] = []
        self.exchange._event_parser.parse_logs(logs, lambda evt: parsed.append(evt))
        events = []
        for event in parsed:
            if event.name.startswith(PlaceOrderEvent.__name__):
                place_order_event = PlaceOrderEvent.from_event(event)
                if place_order_event.margin_account == self._margin_account_address:
                    events.append(place_order_event)
            elif event.name.startswith(OrderCompleteEvent.__name__):
                order_complete_event = OrderCompleteEvent.from_event(event)
                # Ignore fills
                if (
                    order_complete_event.order_complete_type == OrderCompleteType.Cancel
                    or order_complete_event.order_complete_type == OrderCompleteType.Booted
                ):
                    cancel_event = CancelOrderEvent.from_order_complete_event(order_complete_event)
                    if cancel_event.margin_account == self._margin_account_address:
                        events.append(cancel_event)
            elif event.name.startswith(TradeEvent.__name__):
                trade_event = TradeEvent.from_event(event)
                if trade_event.margin_account == self._margin_account_address:
                    events.append(trade_event)
            elif event.name.startswith(LiquidationEvent.__name__):
                liquidation_event = LiquidationEvent.from_event(event)
                if liquidation_event.liquidatee_margin_account == self._margin_account_address:
                    events.append(liquidation_event)
            elif event.name.startswith(ApplyFundingEvent.__name__):
                funding_event = ApplyFundingEvent.from_event(event)
                if funding_event.margin_account == self._margin_account_address:
                    events.append(funding_event)
            else:
                pass

        return events, meta

    async def subscribe_transactions(
        self, commitment: Optional[Commitment] = None, ignore_truncation: bool = False
    ) -> AsyncIterator[Tuple[List[ZetaEnrichedEvent], EventMeta]]:
        """
        This method is used to subscribe to transactions.

        Args:
            commitment (Optional[Commitment], optional): The commitment level to use for the subscription.
                Defaults to None.
            ignore_truncation(bool): Bool to ignore the "Logs truncated, missing event data" warning.
                Defaults to False.

        Yields:
            List[ZetaEvent]: A list of ZetaEvents that are yielded as they are received.

        Warning:
            This method is experimental and requires a Triton RPC node.
        """

        if "rpcpool.com" not in self.ws_endpoint:
            self._logger.warning(
                'Provided ws_endpoint does not contain "rpcpool.com". This method is experimental and'
                " requires a Triton RPC node for transactionSubscribe"
            )

        commitment = commitment or self.connection.commitment
        # TODO: upgrade to websockets 12.0
        # TODO: modify solanapy websocket stuff and make it support txs + types and subclassing
        # (so we dont have to handle json)
        async for ws in websockets.legacy.client.connect(self.ws_endpoint + "/whirligig"):
            try:
                transaction_subscribe = request(
                    "transactionSubscribe",
                    params=[
                        {
                            "mentions": [str(self._margin_account_address)],
                            # "failed": False,
                            "vote": False,
                        },
                        {
                            "commitment": str(commitment),
                        },
                    ],
                )
                await ws.send(json.dumps(transaction_subscribe))

                first_resp = await ws.recv()
                subscription_id = cast(int, first_resp)

                async for msg in ws:
                    try:
                        events, meta = self._parse_transaction_payload(msg, ignore_truncation)
                        if len(events) > 0 or not meta.is_successful:
                            yield events, meta
                    except Exception:
                        self._logger.error(f"Error processing transaction data: {traceback.format_exc()}")
                        break

                transaction_unsubscribe = request(
                    "transactionUnsubscribe",
                    params=[subscription_id],
                )
                await ws.send(json.dumps(transaction_unsubscribe))
            except websockets.exceptions.ConnectionClosed:
                self._logger.warning("Websocket closed, reconnecting...")
                continue

    def _parse_transaction_payload(
        self, msg, ignore_truncation: bool = False
    ) -> Tuple[List[ZetaEnrichedEvent], EventMeta]:
        """
        Parse the transaction payload from the message.

        Args:
            msg: The message received from the websocket.
            ignore_truncation: Bool to ignore the "Logs truncated, missing event data" warning. Defaults to False.

        Returns:
            Tuple[List[ZetaEvent], int]: A tuple containing a list of ZetaEnrichedEvent and the slot number.
        """
        json_msg = json.loads(msg)
        slot = int(json_msg["params"]["result"]["context"]["slot"])
        tx_value = json_msg["params"]["result"]["value"]
        log_messages = tx_value["meta"]["logMessages"]
        message = tx_value["transaction"]["message"]
        error = tx_value["meta"]["err"]
        meta = EventMeta(slot, error)
        if error is not None:
            return [], meta

        if isinstance(message[0], int) or "instructions" not in message[0]:
            message_indexed = message[1]
        else:
            message_indexed = message[0]

        ixs = message_indexed["instructions"][1:]
        ix_args: list[Optional[Container]] = []
        ix_names: list[Optional[str]] = []
        events_to_return = []

        for ix in ixs:
            acc_keys_raw = message_indexed["accountKeys"][1:]
            account_keys = [str(based58.b58encode(bytes(a)), encoding="utf-8") for a in acc_keys_raw]
            loaded_addresses = tx_value["meta"]["loadedAddresses"]
            loaded_addresses_list = account_keys + loaded_addresses["writable"] + loaded_addresses["readonly"]
            owner_address = loaded_addresses_list[ix["programIdIndex"]]

            if owner_address != str(constants.ZETA_PID[self.network]):
                ix_args.append(None)
                ix_names.append(None)
                continue
            data = self.exchange.program.coder.instruction.parse(bytes(ix["data"][1:]))
            ix_args.append(data.data)
            ix_names.append(data.name)

        # Split log_messages every time we see "invoke [1]"
        split_log_messages = []
        split_indices = []
        for i in range(len(log_messages)):
            if log_messages[i] == "Log truncated":
                if ignore_truncation:
                    break
                self._logger.warning("Logs truncated, missing event data")
            if log_messages[i].endswith("invoke [1]"):
                split_indices.append(i)

        split_log_messages = [log_messages[i:j] for i, j in zip([0] + split_indices, split_indices + [None])]
        if len(split_log_messages) > 0:
            split_log_messages = split_log_messages[1:]

        if not ignore_truncation and (
            len(ix_args) != len(split_log_messages) or len(ix_names) != len(split_log_messages)
        ):
            raise Exception("Mismatched transaction info lengths")

        # For each individual instruction, find the ix name and the events
        for i in range(len(split_log_messages)):
            # First log line will always be "...invoke [1]", second will be "Program log: Instruction: <ix_name>"
            ix_name = ix_names[i]
            ix_arg = ix_args[i]

            if ix_name is None or ix_arg is None:
                continue

            chunk = split_log_messages[i]
            events: list[Event] = []
            self.exchange._event_parser.parse_logs(chunk, lambda evt: events.append(evt))

            # Depending on the instruction and event we can get different data from the args
            for event in events:
                # Skip event that aren't for our account but mention our account
                # eg if we do a taker trade, we want to skip the maker crank events
                account_check = (
                    str(event.data.liquidatee_margin_account)
                    if ix_name.startswith("liquidation")
                    else str(event.data.margin_account)
                )
                if account_check != str(self._margin_account_address):
                    continue

                if ix_name.startswith("place_perp_order"):
                    if event.name.startswith(TradeEvent.__name__):
                        events_to_return.append(TradeEvent.from_event(event))  # Taker fill
                    elif event.name.startswith(PlaceOrderEvent.__name__):
                        events_to_return.append(PlaceOrderEventWithArgs.from_event_and_args(event, ix_arg))

                elif ix_name.startswith("crank_event_queue"):
                    if event.name.startswith(TradeEvent.__name__):
                        events_to_return.append(TradeEvent.from_event(event))  # Maker fill\
                    elif str(event.name).startswith(str(OrderCompleteEvent.__name__)):
                        order_complete_event = OrderCompleteEvent.from_event(event)
                        if order_complete_event.order_complete_type == OrderCompleteType.Booted:  # TIF expiry
                            events_to_return.append(CancelOrderEvent.from_order_complete_event(order_complete_event))

                elif ix_name.startswith("cancel_"):
                    if event.name.startswith(OrderCompleteEvent.__name__):
                        order_complete_event = OrderCompleteEvent.from_event(event)
                        if (
                            order_complete_event.order_complete_type == OrderCompleteType.Cancel
                            or order_complete_event.order_complete_type == OrderCompleteType.Booted
                        ):
                            events_to_return.append(CancelOrderEvent.from_order_complete_event(order_complete_event))

                elif ix_name.startswith("apply_perp_funding"):
                    if event.name.startswith(ApplyFundingEvent.__name__):
                        events_to_return.append(ApplyFundingEvent.from_event(event))

        return events_to_return, meta

    # Instructions

    async def deposit(self, amount: float, subaccount_index: int = 0):
        """
        This method is used to deposit a specified amount into the user's margin account.

        Args:
            amount (float): The amount to be deposited.
            subaccount_index (int, optional): The index of the subaccount. Defaults to 0.

        Raises:
            Exception: If the user does not have a USDC account.

        Returns:
            Transaction: The transaction object of the deposit operation.
        """
        ixs = []
        if not await self._check_margin_account_manager_exists():
            self._logger.info("User has no cross-margin account manager, creating one...")
            ixs.append(self._init_margin_account_manager_ix())
        # Create margin account if user doesn't have one
        if not await self._check_margin_account_exists():
            self._logger.info("User has no cross-margin account, creating one...")
            ixs.append(self._init_margin_account_ix(subaccount_index))
        # Check they have an existing USDC account
        if await self._check_user_usdc_account_exists():
            ixs.append(self._deposit_ix(amount))
        else:
            raise Exception("User has no USDC, cannot deposit to margin account")

        self._logger.info(f"Depositing {amount} USDC to margin account")
        return await self._send_versioned_transaction(ixs)

    def _init_margin_account_manager_ix(self) -> Instruction:
        """
        Initialize the margin account manager instruction.

        Raises:
            Exception: If the margin account manager address is not loaded.

        Returns:
            Instruction: The initialized cross margin account manager instruction.
        """
        if self._margin_account_manager_address is None:
            raise Exception("Margin account manager address not loaded, cannot deposit")
        return initialize_cross_margin_account_manager(
            {
                "cross_margin_account_manager": self._margin_account_manager_address,
                "authority": self.provider.wallet.public_key,
                "payer": self.provider.wallet.public_key,
                "zeta_program": self.exchange.program_id,
            },
            self.exchange.program_id,
        )

    def _init_margin_account_ix(self, subaccount_index: int = 0) -> Instruction:
        """
        Initialize the margin account instruction.

        Args:
            subaccount_index (int, optional): The index of the subaccount. Defaults to 0.

        Raises:
            Exception: If the margin account address is not loaded.

        Returns:
            Instruction: The initialized cross margin account instruction.
        """
        if self._margin_account_address is None or self._margin_account_manager_address is None:
            raise Exception("Margin account address not loaded, cannot deposit")
        return initialize_cross_margin_account(
            {"subaccount_index": subaccount_index},
            {
                "cross_margin_account": self._margin_account_address,
                "cross_margin_account_manager": self._margin_account_manager_address,
                "authority": self.provider.wallet.public_key,
                "payer": self.provider.wallet.public_key,
                "zeta_program": self.exchange.program_id,
            },
            self.exchange.program_id,
        )

    def _deposit_ix(self, amount: float) -> Instruction:
        """
        Deposit instruction.

        Args:
            amount (float): The amount to be deposited.

        Raises:
            Exception: If the user USDC address is not loaded.

        Returns:
            Instruction: The deposit instruction.
        """
        if self._user_usdc_address is None or self._margin_account_address is None:
            raise Exception("User USDC address not loaded, cannot deposit")
        return deposit_v2(
            {"amount": utils.convert_decimal_to_fixed_int(amount, constants.MIN_NATIVE_TICK_SIZE)},
            {
                "margin_account": self._margin_account_address,
                "vault": self._combined_vault_address,
                "user_token_account": self._user_usdc_address,
                "socialized_loss_account": self._combined_socialized_loss_address,
                "authority": self.provider.wallet.public_key,
                "state": self.exchange._state_address,
                "pricing": self.exchange._pricing_address,
            },
            self.exchange.program_id,
        )

    # TODO: withdraw (and optionally close)
    async def withdraw(self):
        """
        Withdraw method.

        Raises:
            NotImplementedError: This method is not implemented yet.
        """
        raise NotImplementedError

    def _init_open_orders_ix(self, asset: Asset) -> Instruction:
        """
        Initialize the open orders instruction.

        Args:
            asset (Asset): The asset for which to initialize the open orders.

        Raises:
            Exception: If the asset is not loaded into the client or if the open orders address is not loaded.

        Returns:
            Instruction: The initialized open orders instruction.
        """
        if asset not in self.exchange.assets:
            raise Exception(f"Asset {asset.name} not loaded into client, cannot initialize open orders")
        if self._open_orders_addresses is None or self._margin_account_address is None:
            raise Exception("Open orders address not loaded, cannot place order")
        return initialize_open_orders_v3(
            {"asset": asset.to_program_type()},
            {
                "state": self.exchange._state_address,
                "dex_program": constants.MATCHING_ENGINE_PID[self.network],
                "open_orders": self._open_orders_addresses[asset],
                "cross_margin_account": self._margin_account_address,
                "authority": self.provider.wallet.public_key,
                "payer": self.provider.wallet.public_key,
                "market": self.exchange.markets[asset].address,
                "serum_authority": self.exchange._serum_authority_address,
                "open_orders_map": pda.get_open_orders_map_address(
                    self.exchange.program_id, self._open_orders_addresses[asset]
                ),
            },
            self.exchange.program_id,
        )

    def _place_order_ix(
        self,
        asset: Asset,
        price: float,
        size: float,
        side: Side,
        order_opts: Optional[OrderOptions] = None,
        tif_buffer: int = 0,
    ) -> Instruction:
        """
        Build a PlaceOrder instruction.

        Args:
            asset (Asset): The asset for which to place the order.
            price (float): The price of the order.
            size (float): The size of the order.
            side (Side): The side of the order (bid or ask).
            order_opts (Optional[OrderOptions], optional): The options for the order. Defaults to None.

        Raises:
            Exception: If the asset is not loaded into the client, or if the margin account address or open orders
                addresses are not loaded.

        Returns:
            Instruction: The place order instruction.
        """
        if order_opts is None:
            order_opts = OrderOptions()

        unix_timestamp = int(time.time())
        tif_offset = (
            utils.get_tif_offset(
                order_opts.expiry_ts,
                self.exchange.markets[asset]._market_state.epoch_length,
                unix_timestamp,  # self.exchange.clock.account.unix_timestamp,
                tif_buffer,
            )
            if order_opts.expiry_ts
            else None
        )

        if asset not in self.exchange.assets:
            raise Exception(f"Asset {asset.name} not loaded into client, cannot place order")
        if self._margin_account_address is None:
            raise Exception("Margin account address not loaded, cannot place order")
        if self._open_orders_addresses is None:
            raise Exception("Open orders addresses not loaded, cannot place order")

        return place_perp_order_v4(
            {
                "price": utils.convert_decimal_to_fixed_int(
                    price, utils.get_fixed_tick_size(self.exchange.state, asset)
                ),
                "size": utils.convert_decimal_to_fixed_lot(
                    size, utils.get_fixed_min_lot_size(self.exchange.state, asset)
                ),
                "side": side.to_program_type(),
                "order_type": order_opts.order_type.to_program_type(),
                "reduce_only": False,
                "client_order_id": order_opts.client_order_id,
                "tif_offset": tif_offset,
                "tag": order_opts.tag,
                "asset": asset.to_program_type(),
            },
            {
                "authority": self.provider.wallet.public_key,
                "place_order_accounts": {
                    "state": self.exchange._state_address,
                    "pricing": self.exchange._pricing_address,
                    "margin_account": self._margin_account_address,
                    "dex_program": constants.MATCHING_ENGINE_PID[self.network],
                    "serum_authority": self.exchange._serum_authority_address,
                    "open_orders": self._open_orders_addresses[asset],
                    "market_accounts": {
                        "market": self.exchange.markets[asset].address,
                        "request_queue": self.exchange.markets[asset]._market_state.request_queue,
                        "event_queue": self.exchange.markets[asset]._market_state.event_queue,
                        "bids": self.exchange.markets[asset]._market_state.bids,
                        "asks": self.exchange.markets[asset]._market_state.asks,
                        "coin_vault": self.exchange.markets[asset]._market_state.base_vault,
                        "pc_vault": self.exchange.markets[asset]._market_state.quote_vault,
                        "order_payer_token_account": (
                            self.exchange.markets[asset]._quote_zeta_vault_address
                            if side == Side.Bid
                            else self.exchange.markets[asset]._base_zeta_vault_address
                        ),
                        "coin_wallet": self.exchange.markets[asset]._base_zeta_vault_address,
                        "pc_wallet": self.exchange.markets[asset]._quote_zeta_vault_address,
                    },
                    "oracle": self.exchange.pricing.oracles[asset.to_index()],
                    "oracle_backup_feed": self.exchange.pricing.oracle_backup_feeds[asset.to_index()],
                    "oracle_backup_program": constants.CHAINLINK_PID,
                    "market_mint": (
                        self.exchange.markets[asset]._market_state.quote_mint
                        if side == Side.Bid
                        else self.exchange.markets[asset]._market_state.base_mint
                    ),
                    "mint_authority": self.exchange._mint_authority_address,
                    "perp_sync_queue": self.exchange.pricing.perp_sync_queues[asset.to_index()],
                },
            },
            self.exchange.program_id,
        )

    async def cancel_order(self, asset: Asset, order_id: int, side: Side):
        """
        Cancel an order.

        Args:
            asset (Asset): The asset for which to cancel the order.
            order_id (int): The ID of the order to cancel.
            side (Side): The side of the order (buy or sell).

        Returns:
            Transaction: The transaction of the cancelled order.
        """
        ixs = [self._cancel_order_ix(asset, order_id, side)]
        self._logger.info(f"Cancelling order {order_id} for {asset}")
        return await self._send_versioned_transaction(ixs)

    def _cancel_order_ix(self, asset: Asset, order_id: int, side: Side) -> Instruction:
        """
        Build a CancelOrder instruction.

        Args:
            asset (Asset): The asset for which to cancel the order.
            order_id (int): The ID of the order to cancel.
            side (Side): The side of the order (bid or ask).

        Raises:
            Exception: If the margin account address or open orders addresses are not loaded.

        Returns:
            Instruction: The cancel order instruction.
        """
        if self._margin_account_address is None:
            raise Exception("Margin account address not loaded, cannot cancel order")
        if self._open_orders_addresses is None:
            raise Exception("Open orders addresses not loaded, cannot cancel order")
        return cancel_order(
            {"side": side.to_program_type(), "order_id": order_id, "asset": asset.to_program_type()},
            {
                "authority": self.provider.wallet.public_key,
                "cancel_accounts": {
                    "state": self.exchange._state_address,
                    "margin_account": self._margin_account_address,
                    "dex_program": constants.MATCHING_ENGINE_PID[self.network],
                    "serum_authority": self.exchange._serum_authority_address,
                    "open_orders": self._open_orders_addresses[asset],
                    "market": self.exchange.markets[asset].address,
                    "bids": self.exchange.markets[asset]._market_state.bids,
                    "asks": self.exchange.markets[asset]._market_state.asks,
                    "event_queue": self.exchange.markets[asset]._market_state.event_queue,
                },
            },
            self.exchange.program_id,
        )

    # TODO: cancelorderbyclientorderid

    def _cancel_orders_for_market_ix(self, asset: Asset) -> Instruction:
        """
        Build an instruction for cancelling all orders on a given market.

        Args:
            asset (Asset): The asset for which to cancel all orders.

        Raises:
            Exception: If the margin account address or open orders addresses are not loaded.

        Returns:
            Instruction: The cancel all orders for a market instruction.
        """
        if self._margin_account_address is None:
            raise Exception("Margin account address not loaded, cannot cancel orders")
        if self._open_orders_addresses is None:
            raise Exception("Open orders addresses not loaded, cannot cancel orders")
        return cancel_all_market_orders(
            {"asset": asset.to_program_type()},
            {
                "authority": self.provider.wallet.public_key,
                "cancel_accounts": {
                    "state": self.exchange._state_address,
                    "margin_account": self._margin_account_address,
                    "dex_program": constants.MATCHING_ENGINE_PID[self.network],
                    "serum_authority": self.exchange._serum_authority_address,
                    "open_orders": self._open_orders_addresses[asset],
                    "market": self.exchange.markets[asset].address,
                    "bids": self.exchange.markets[asset]._market_state.bids,
                    "asks": self.exchange.markets[asset]._market_state.asks,
                    "event_queue": self.exchange.markets[asset]._market_state.event_queue,
                },
            },
            self.exchange.program_id,
        )

    async def cancel_orders_for_market(
        self,
        asset: Asset,
        pre_instructions: Optional[list[Instruction]] = None,
        post_instructions: Optional[list[Instruction]] = None,
        priority_fee: int = 0,
    ):
        """
        Cancel all orders for a market.

        Args:
            asset (Asset): The asset for which to cancel all orders.
            pre_instructions (Optional[list[Instruction]], optional): The list of instructions to execute before
                cancelling the orders. Defaults to None.
            post_instructions (Optional[list[Instruction]], optional): The list of instructions to execute after
                cancelling the orders. Defaults to None.
            priority_fee (int): Additional priority fee, in microlamports per CU. Defaults to 0.

        Returns:
            Transaction: The transaction of the cancelled orders.
        """
        ixs = []
        if priority_fee > 0:
            ixs.extend([set_compute_unit_price(priority_fee)])
        if pre_instructions is not None:
            ixs.extend(pre_instructions)
        ixs.append(self._cancel_orders_for_market_ix(asset))
        if post_instructions is not None:
            ixs.extend(post_instructions)
        self._logger.info(f"Cancelling all orders for {asset}")
        return await self._send_versioned_transaction(ixs)

    async def place_orders_for_market(
        self,
        asset: Asset,
        orders: list[OrderArgs],
        pre_instructions: Optional[list[Instruction]] = None,
        post_instructions: Optional[list[Instruction]] = None,
        tif_buffer: int = 0,
        priority_fee: int = 0,
    ):
        """
        Place orders for a market.

        Args:
            asset (Asset): The asset for which to place the orders.
            orders (list[OrderArgs]): The list of orders to place.
            pre_instructions (Optional[list[Instruction]], optional): The list of instructions to execute before
                placing the orders. Defaults to None.
            post_instructions (Optional[list[Instruction]], optional): The list of instructions to execute after
                placing the orders. Defaults to None.
            tif_buffer (int): Extra value to add to tif_expiry at epoch rollover to aid a smooth transition.
                Defaults to 0.
            priority_fee (int): Additional priority fee, in microlamports per CU. Defaults to 0.

        Returns:
            Transaction: The transaction of the placed orders.
        """
        # TODO: warn about log truncation above 10 orders
        ixs = []
        if not await self._check_open_orders_account_exists(asset):
            self._logger.info("User has no open orders account, creating one...")
            ixs.append(self._init_open_orders_ix(asset))

        if priority_fee > 0:
            ixs.extend([set_compute_unit_price(priority_fee)])

        if pre_instructions is not None:
            ixs.extend(pre_instructions)
        for order in orders:
            ixs.append(self._place_order_ix(asset, order.price, order.size, order.side, order.order_opts, tif_buffer))
        if post_instructions is not None:
            ixs.extend(post_instructions)
        self._logger.info(f"Placing {len(orders)} orders for {asset}")
        return await self._send_versioned_transaction(ixs)

    async def replace_orders_for_market(self, asset: Asset, orders: list[OrderArgs], priority_fee: int = 0):
        """
        Replace orders for a market (atomically cancel all orders and replace them).

        Args:
            asset (Asset): The asset for which to replace the orders.
            orders (list[OrderArgs]): The list of new orders to place.
            priority_fee (int): Additional priority fee, in microlamports per CU. Defaults to 0.

        Returns:
            Transaction: The transaction of the replaced orders.
        """
        pre_ixs = []
        if priority_fee > 0:
            pre_ixs.extend([set_compute_unit_price(priority_fee)])
        pre_ixs.extend([self._cancel_orders_for_market_ix(asset)])
        return await self.place_orders_for_market(asset, orders, pre_instructions=pre_ixs)

    # TODO: liquidate
    async def liquidate(self):
        """
        Liquidate method.

        Raises:
            NotImplementedError: This method is not implemented yet.
        """
        raise NotImplementedError

    async def _send_versioned_transaction(self, ixs: list[Instruction]):
        """
        Send a versioned transaction.

        Args:
            ixs (list[Instruction]): The list of instructions to include in the transaction.

        Returns:
            str: The signature of the transaction.
        """
        # Prefetch blockhash, using cache if available
        if self.connection.blockhash_cache:
            try:
                recent_blockhash = self.connection.blockhash_cache.get()
                last_valid_block_height = None
                self._logger.debug(f"Blockhash cache hit, using cached blockhash: {recent_blockhash}")
            except ValueError:
                blockhash_resp = await self.connection.get_latest_blockhash(self.connection.commitment)
                recent_blockhash = self.connection._process_blockhash_resp(blockhash_resp, used_immediately=True)
                last_valid_block_height = blockhash_resp.value.last_valid_block_height
                self._logger.debug(f"Blockhash cache miss, fetched from RPC: {recent_blockhash}")
        else:
            blockhash_resp = await self.connection.get_latest_blockhash(self.connection.commitment)
            recent_blockhash = self.connection.parse_recent_blockhash(blockhash_resp)
            last_valid_block_height = blockhash_resp.value.last_valid_block_height
            self._logger.debug(f"Blockhash cache not enabled, fetched from RPC: {recent_blockhash}")

        msg = MessageV0.try_compile(
            self.provider.wallet.public_key, ixs, [constants.ZETA_LUT[self.network]], recent_blockhash
        )
        tx = VersionedTransaction(msg, [self.provider.wallet.payer])

        try:
            opts = self.provider.opts._replace(last_valid_block_height=last_valid_block_height)
            signature = await self.provider.send(tx, opts)
        except RPCException as exc:
            # This won't work on zDEX errors
            # TODO: add ZDEX error parsing
            parsed = from_tx_error(exc)
            self._logger.error(parsed)
            if parsed is not None:
                raise parsed from exc
            raise exc
        return signature
