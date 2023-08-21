from typing import List

from anchorpy import Wallet
from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts

from zeta_py import constants, pda
from zeta_py.exchange import Exchange
from zeta_py.program_account import Account
from zeta_py.types import Asset, Network
from zeta_py.zeta_client.accounts.cross_margin_account import CrossMarginAccount


class Client:
    """
    Cross margin client
    """

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
        margin_account_address = pda.get_margin_account(wallet.public_key(), exchange.program.program_id)
        await Account[CrossMarginAccount].create(margin_account_address, connection, CrossMarginAccount)
        return cls(connection, wallet)
