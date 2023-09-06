import logging
from dataclasses import dataclass

from anchorpy import Provider, Wallet
from solana.rpc.async_api import AsyncClient
from solana.rpc.core import RPCException
from solana.rpc.types import TxOpts
from solders.instruction import Instruction
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.sysvar import RENT
from solders.transaction import VersionedTransaction
from spl.token.constants import TOKEN_PROGRAM_ID

from zeta_py import constants, pda, utils
from zeta_py.accounts import Account
from zeta_py.exchange import Exchange
from zeta_py.pyserum.market.types import Order
from zeta_py.types import Asset, Network, OrderOptions, Position, Side
from zeta_py.zeta_client.accounts.cross_margin_account import CrossMarginAccount
from zeta_py.zeta_client.accounts.cross_margin_account_manager import (
    CrossMarginAccountManager,
)
from zeta_py.zeta_client.errors import from_tx_error
from zeta_py.zeta_client.instructions import (
    cancel_all_market_orders,
    cancel_order,
    deposit_v2,
    initialize_cross_margin_account,
    initialize_cross_margin_account_manager,
    initialize_open_orders_v3,
    place_perp_order_v3,
)

# TODO: simplify to just client, no exchange?
# TODO: simplify and remove generic programAccount classes and handle bare minimum bids,asks,slots
# TODO: refactor markets to get rid of cancerous pyserum shit and standardise
# TODO: make client and markets stateless (don't hold self.data) - i.e. callback driven model
# TODO: remove timescaledb stuff - make client as lightweight as possible and leave this to external MMs to define
# TODO: simplify client args e.g. preflight commitment etc
# TODO: add trade and liq subscriptions

@dataclass
class Client:
    """
    Cross margin client
    """

    provider: Provider
    network: Network
    connection: AsyncClient
    exchange: Exchange
    margin_account: Account[CrossMarginAccount]
    balance: int
    positions: dict[Asset, Position]
    open_orders: list[Asset, list[Order]]

    _open_orders_addresses: dict[Asset, Pubkey]
    _margin_account_manager_address: Pubkey
    _combined_vault_address: Pubkey
    _combined_socialized_loss_address: Pubkey
    _user_usdc_address: Pubkey
    _logger: logging.Logger

    @classmethod
    async def load(
        cls,
        network: Network,
        connection: AsyncClient,
        wallet: Wallet,
        assets: list[Asset] = Asset.all(),
        tx_opts: TxOpts = None,
        subscribe: bool = False,
    ):
        """
        Create a new client
        """
        tx_opts = tx_opts or TxOpts(
            {"skip_preflight": False, "preflight_commitment": connection.commitment, "skip_confirmation": False}
        )
        provider = Provider(
            connection,
            wallet,
            tx_opts,
        )
        exchange = await Exchange.load(
            network=network,
            connection=connection,
            assets=assets,
            tx_opts=tx_opts,
            subscribe=subscribe,
        )
        # TODO: ideally batch these fetches
        margin_account_address = pda.get_margin_account_address(exchange.program_id, wallet.public_key, 0)
        margin_account = await Account[CrossMarginAccount].load(margin_account_address, connection, CrossMarginAccount)

        balance = utils.convert_fixed_int_to_decimal(margin_account.account.balance)

        positions = {}
        open_orders = {}
        _open_orders_addresses = {}
        for asset in assets:
            # positions per market
            positions[asset] = Position(
                utils.convert_fixed_lot_to_decimal(
                    margin_account.account.product_ledgers[asset.to_index()].position.size
                ),
                utils.convert_fixed_int_to_decimal(
                    margin_account.account.product_ledgers[asset.to_index()].position.cost_of_trades
                ),
            )

            # open orders per market
            open_orders_address = pda.get_open_orders_address(
                exchange.program_id,
                constants.DEX_PID[network],
                exchange.markets[asset].address,
                margin_account.address,
            )
            _open_orders_addresses[asset] = open_orders_address
            # TODO: figure out open order subscription
            open_orders[asset] = await exchange.markets[asset]._serum_market.load_orders_for_owner(open_orders_address)

        # additional addresses to cache
        _margin_account_manager_address = pda.get_cross_margin_account_manager_address(
            exchange.program_id, provider.wallet.public_key
        )
        _combined_vault_address = pda.get_combined_vault_address(exchange.program_id)
        _combined_socialized_loss_address = pda.get_combined_socialized_loss_address(exchange.program_id)
        _user_usdc_address = pda.get_associated_token_address(provider.wallet.public_key, constants.USDC_MINT[network])

        logger = logging.getLogger(f"{__name__}.{cls.__name__}")

        return cls(
            provider,
            network,
            connection,
            exchange,
            margin_account,
            balance,
            positions,
            open_orders,
            _open_orders_addresses,
            _margin_account_manager_address,
            _combined_vault_address,
            _combined_socialized_loss_address,
            _user_usdc_address,
            logger,
        )

    async def _check_user_usdc_account_exists(self):
        if not hasattr(self, "_user_usdc_account"):
            # If they don't have USDC wallet this will be null
            resp = await self.connection.get_account_info_json_parsed(self._user_usdc_address)
            self._user_usdc_account = resp.value
        return self._user_usdc_account is not None

    async def _check_margin_account_manager_exists(self):
        if not hasattr(self, "_margin_account_manager"):
            # If they don't have margin account manager this will be null
            self._margin_account_manager = await Account[CrossMarginAccountManager].load(
                self._margin_account_manager_address, self.connection, CrossMarginAccountManager
            )  # None if no manager exists
        return self._margin_account_manager._is_initialized

    async def fetch_open_orders(self, asset: Asset):
        oo = await self.exchange.markets[asset]._serum_market.load_orders_for_owner(self._open_orders_addresses[asset])
        self.open_orders[asset] = oo
        return oo

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
        if not self.margin_account._is_initialized:
            self._logger.info("User has no cross-margin account manager, creating one...")
            ixs.append(
                initialize_cross_margin_account(
                    {"subaccount_index": subaccount_index},
                    {
                        "cross_margin_account": self.margin_account.address,
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
                        "margin_account": self.margin_account.address,
                        "vault": self._combined_vault_address,
                        "user_token_account": self._user_usdc_address,
                        "socialized_loss_account": self._combined_socialized_loss_address,
                        "authority": self.provider.wallet.public_key,
                        "state": self.exchange.state.address,
                        "pricing": self.exchange.pricing.address,
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
        ixs = self._place_order_ixs(asset, price, size, side, order_opts)
        self._logger.info(f"Placed {size}x {asset}-PERP {side.name} @ ${price}")
        return await self._send_versioned_transaction(ixs)

    def _place_order_ixs(
        self, asset: Asset, price: float, size: float, side: Side, order_opts: OrderOptions = OrderOptions
    ) -> list[Instruction]:
        if asset not in self.open_orders:
            raise Exception(f"Asset {asset.name} not loaded into client, cannot place order")
        ixs = []
        if self.open_orders[asset] is None:
            self._logger.info("User has no open orders account, creating one...")
            ixs.append(
                initialize_open_orders_v3(
                    {"asset": asset.to_program_type()},
                    {
                        "state": self.exchange.state.address,
                        "dex_program": constants.DEX_PID[self.network],
                        "system_program": SYS_PROGRAM_ID,
                        "open_orders": self._open_orders_addresses[asset],
                        "cross_margin_account": self.margin_account.address,
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
        tif_offset = (
            utils.get_tif_offset(
                order_opts.expiry_ts,
                self.exchange.markets[asset]._serum_market.state.epoch_length(),
                self.exchange.clock.account.unix_timestamp,
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
                    "state": self.exchange.state.address,
                    "pricing": self.exchange.pricing.address,
                    "margin_account": self.margin_account.address,
                    "authority": self.provider.wallet.public_key,
                    "dex_program": constants.DEX_PID[self.network],
                    "token_program": TOKEN_PROGRAM_ID,
                    "serum_authority": self.exchange._serum_authority_address,
                    "open_orders": self._open_orders_addresses[asset],
                    "rent": RENT,
                    "market_accounts": {
                        "market": self.exchange.markets[asset].address,
                        "request_queue": self.exchange.markets[asset]._serum_market.state.request_queue(),
                        "event_queue": self.exchange.markets[asset]._serum_market.state.event_queue(),
                        "bids": self.exchange.markets[asset]._serum_market.state.bids(),
                        "asks": self.exchange.markets[asset]._serum_market.state.asks(),
                        "coin_vault": self.exchange.markets[asset]._serum_market.state.base_vault(),
                        "pc_vault": self.exchange.markets[asset]._serum_market.state.quote_vault(),
                        "order_payer_token_account": self.exchange.markets[asset]._quote_zeta_vault_address
                        if side == Side.Bid
                        else self.exchange.markets[asset]._base_zeta_vault_address,
                        "coin_wallet": self.exchange.markets[asset]._base_zeta_vault_address,
                        "pc_wallet": self.exchange.markets[asset]._quote_zeta_vault_address,
                    },
                    "oracle": self.exchange.pricing.account.oracles[asset.to_index()],
                    "oracle_backup_feed": self.exchange.pricing.account.oracle_backup_feeds[asset.to_index()],
                    "oracle_backup_program": constants.CHAINLINK_PID,
                    "market_mint": self.exchange.markets[asset]._serum_market.state.quote_mint()
                    if side == Side.Bid
                    else self.exchange.markets[asset]._serum_market.state.base_mint(),
                    "mint_authority": self.exchange._mint_authority_address,
                    "perp_sync_queue": self.exchange.pricing.account.perp_sync_queues[asset.to_index()],
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
                        "state": self.exchange.state.address,
                        "margin_account": self.margin_account.address,
                        "dex_program": constants.DEX_PID[self.network],
                        "serum_authority": self.exchange._serum_authority_address,
                        "open_orders": self._open_orders_addresses[asset],
                        "market": self.exchange.markets[asset].address,
                        "bids": self.exchange.markets[asset]._serum_market.state.bids(),
                        "asks": self.exchange.markets[asset]._serum_market.state.asks(),
                        "event_queue": self.exchange.markets[asset]._serum_market.state.event_queue(),
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
                        "state": self.exchange.state.address,
                        "margin_account": self.margin_account.address,
                        "dex_program": constants.DEX_PID[self.network],
                        "serum_authority": self.exchange._serum_authority_address,
                        "open_orders": self._open_orders_addresses[asset],
                        "market": self.exchange.markets[asset].address,
                        "bids": self.exchange.markets[asset]._serum_market.state.bids(),
                        "asks": self.exchange.markets[asset]._serum_market.state.asks(),
                        "event_queue": self.exchange.markets[asset]._serum_market.state.event_queue(),
                    },
                },
            )
        )
        return ixs

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
        bid_place_ixs = self._place_order_ixs(asset, bid_price, bid_size, Side.Bid, order_opts)
        ask_place_ixs = self._place_order_ixs(asset, ask_price, ask_size, Side.Ask, order_opts)
        ixs = cancel_ixs + bid_place_ixs + ask_place_ixs
        self._logger.info(
            f"Replacing {asset} orders: \
                {bid_size}x {Side.Bid.name} @ ${bid_price}, {ask_size}x {Side.Ask.name} @ ${ask_price}"
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
