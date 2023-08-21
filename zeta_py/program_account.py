import asyncio
from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solana.rpc.websocket_api import connect
from solders.pubkey import Pubkey

from zeta_py import utils
from zeta_py.types import Network
from zeta_py.zeta_client.accounts import AnchorpyAccount

AnchorpyAccountType = TypeVar("AnchorpyAccountType", bound=AnchorpyAccount)


@dataclass
class Account(Generic[AnchorpyAccountType]):
    address: Pubkey
    decode_class: Type[AnchorpyAccountType]
    account: AnchorpyAccountType = None
    last_update_slot: int = None
    _subscription_task: asyncio.Task = None
    _TIMEOUT = 60

    @classmethod
    async def create(
        cls, address: Pubkey, connection: AsyncClient, decode_class: AnchorpyAccountType
    ) -> "Account[AnchorpyAccountType]":
        instance = cls(address, decode_class)
        instance.account, instance.last_update_slot = await instance.fetch(connection, address)
        print(f"Loaded account: {instance.account.__class__.__name__}")
        return instance

    @property
    def _is_initialized(self) -> bool:
        return self.account is not None

    @property
    def _is_subscribed(self) -> bool:
        return self._subscription_task is not None

    async def fetch(self, conn: AsyncClient, address: Pubkey) -> None:
        resp = await conn.get_account_info(address, commitment=conn.commitment)
        info = resp.value
        if info is None:
            return None
        fetch_slot = resp.context.slot
        bytes_data = info.data
        account = self.decode(bytes_data)
        return account, fetch_slot

    def decode(self, data: bytes) -> AnchorpyAccountType:
        return self.decode_class.decode(data)

    async def update(self, conn: AsyncClient) -> None:
        self.account = await self.fetch(conn, self.address)

    async def _subscribe(self, network: Network, commitment: Commitment) -> None:
        ws_endpoint = utils.cluster_endpoint(network, ws=True)
        try:
            async with connect(ws_endpoint) as ws:
                await ws.account_subscribe(
                    self.address,
                    commitment=commitment,
                    encoding="base64",
                )
                first_resp = await asyncio.wait_for(ws.recv(), timeout=self._TIMEOUT)
                first_resp[0].result
                while True:
                    msg = await asyncio.wait_for(ws.recv(), timeout=self._TIMEOUT)
                    account = self.decode(msg[0].result.value.data)
                    self.account = account
                    self.last_update_slot = msg[0].result.context.slot
        finally:
            self._subscription_task = None

    def subscribe(self, network: Network, commitment: Commitment) -> None:
        if self._is_subscribed:
            print("Already subscribed")
            return
        # Run the subscription in the background
        # TODO: worth threading this??
        self._subscription_task = asyncio.create_task(self._subscribe(network, commitment))
        print(f"Subscribed to {self.account.__class__.__name__}")

    def unsubscribe(self) -> None:
        if not self._is_subscribed:
            print("Not subscribed")
            return
        self._subscription_task.cancel()
        self._subscription_task = None
        print(f"Unsubscribed to {self.account.__class__.__name__}")
