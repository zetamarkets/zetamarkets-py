from dataclasses import dataclass
from typing import List, Mapping

from anchorpy import Wallet
from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts

from zeta_py import constants, pda, utils
from zeta_py.accounts import Account
from zeta_py.exchange import Exchange
from zeta_py.pyserum.market.types import Order
from zeta_py.types import Asset, Network, Position
from zeta_py.zeta_client.accounts.cross_margin_account import CrossMarginAccount


@dataclass
class Client:
    """
    Cross margin client
    """

    network: Network
    connection: AsyncClient
    wallet: Wallet
    # assets: List[Asset]
    exchange: Exchange
    margin_account: Account[CrossMarginAccount]
    balance: int
    positions: Mapping[Asset, Position]
    open_orders: Mapping[Asset, List[Order]]

    @classmethod
    async def create(
        cls,
        network: Network,
        connection: AsyncClient,
        wallet: Wallet,
        assets: List[Asset] = Asset.all(),
        tx_opts: TxOpts = constants.DEFAULT_TX_OPTS,
        subscribe: bool = False,
    ):
        """
        Create a new client
        """
        exchange = await Exchange.create(
            network=network,
            connection=connection,
            assets=assets,
            tx_opts=tx_opts,
            subscribe=subscribe,
            wallet=wallet,
        )
        margin_account_address, _ = pda.get_margin_account_address(exchange.program.program_id, wallet.public_key, 0)
        margin_account = await Account[CrossMarginAccount].create(
            margin_account_address, connection, CrossMarginAccount
        )
        balance = utils.convert_fixed_int_to_decimal(margin_account.account.balance)

        positions = {}
        open_orders = {}
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
            open_orders_address, _ = pda.get_open_orders_address(
                exchange.program.program_id,
                constants.DEX_PID[network],
                exchange.markets[asset].address,
                margin_account.address,
            )
            open_orders[asset] = await exchange.markets[asset]._serum_market.load_orders_for_owner(
                margin_account.address, open_orders_address
            )

        # deposit

        # withdraw

        # placeorder

        # cancelorder

        # cancelorderbyclientorderid

        # cancelallorders

        return cls(network, connection, wallet, exchange, margin_account, balance, positions, open_orders)
