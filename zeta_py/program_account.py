import asyncio
from solders.pubkey import Pubkey
from typing import TypeVar, Generic
from zeta_py import utils

from zeta_py.zeta_client.accounts.pricing import Pricing
from solana.rpc.websocket_api import connect
from solana.rpc.async_api import AsyncClient

ProgramAccountType = TypeVar("ProgramAccountType")


class ProgramAccount(Generic[ProgramAccountType]):
    @property
    def is_loaded(self) -> bool:
        return self._account is not None

    @property
    def address(self) -> Pubkey:
        return self._address

    @property
    def account(self) -> ProgramAccountType:
        if self.is_loaded:
            return self._account
        else:
            raise Exception("Account not loaded, please call .load() first")

    @account.setter
    def account(self, account: ProgramAccountType):
        self._account = account

    @property
    def is_subscribed(self) -> bool:
        return self._subscription_task is not None

    def __init__(
        self,
        address: Pubkey,
        account_class: ProgramAccountType,
    ):
        self._address = address
        self._account_class = account_class
        self._account = None
        self._subscription_task = None

    async def load(self, connection: AsyncClient):
        if self.is_loaded:
            print(self.is_loaded)
            raise Exception("Exchange already loaded")
        self._account: ProgramAccountType = await self._account_class.fetch(
            connection, self.address
        )

    async def _subscribe(self) -> None:
        ws_endpoint = utils.cluster_endpoint(self.network, ws=True)
        try:
            async with connect(ws_endpoint) as ws:
                await ws.account_subscribe(
                    self.accounts.pricing.address,
                    commitment="confirmed",
                    encoding="base64",
                )
                first_resp = await ws.recv()
                subscription_id = first_resp[0].result
                while True:
                    msg = await ws.recv()
                    price_account = Pricing.decode(msg[0].result.value.data)
                    self._accounts.pricing.account = price_account
        finally:
            await ws.account_unsubscribe(subscription_id)
            self._subscription_task = None

    def subscribe(self) -> None:
        if self.is_subscribed:
            raise Exception("Already subscribed")
        # Run the subscription in the background
        self._subscription_task = asyncio.create_task(self._subscribe())
        print(f"Subscribed to {self._account_class.__name__}")

    # Doesn't work I assume because of the async nature of the websocket
    async def unsubscribe(self) -> None:
        if not self.is_subscribed:
            raise Exception("Not subscribed")
        self._subscription_task.cancel()
        self._subscription_task = None
        print(f"Unsubscribed to {self._account_class.__name__}")
