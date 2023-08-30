import asyncio
import logging
import typing
from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solana.rpc.websocket_api import connect
from solders.pubkey import Pubkey

from zeta_py import utils
from zeta_py._layouts.clock import SYSTEM_CLOCK_LAYOUT
from zeta_py.types import Network
from zeta_py.zeta_client.accounts import AnchorpyAccount

AnchorpyAccountType = TypeVar("AnchorpyAccountType", bound=AnchorpyAccount)


@dataclass
class Account(Generic[AnchorpyAccountType]):
    """Stateful wrapper for decodable accounts

    Args:
        Generic (_type_): _description_

    Returns:
        _type_: _description_
    """

    address: Pubkey
    decode_class: Type[AnchorpyAccountType]
    account: AnchorpyAccountType = None
    last_update_slot: int = None
    _subscription_task: asyncio.Task = None
    _TIMEOUT = 60
    _logger: logging.Logger = None

    @classmethod
    async def load(
        cls, address: Pubkey, connection: AsyncClient, decode_class: AnchorpyAccountType
    ) -> "Account[AnchorpyAccountType]":
        logger = logging.getLogger(f"{__name__}.{cls.__name__}")
        instance = cls(address, decode_class, _logger=logger)
        instance.account, instance.last_update_slot = await instance.fetch(connection, address)
        logger.info(f"Loaded account: {instance.account.__class__.__name__}")
        return instance

    @property
    def _is_initialized(self) -> bool:
        return self.account is not None

    @property
    def _is_subscribed(self) -> bool:
        return self._subscription_task is not None

    async def fetch(self, conn: AsyncClient, address: Pubkey) -> typing.Tuple[AnchorpyAccountType, int]:
        resp = await conn.get_account_info(address, commitment=conn.commitment)
        info = resp.value
        if info is None:
            return None, None
        fetch_slot = resp.context.slot
        bytes_data = info.data
        account = self.decode(bytes_data)
        return account, fetch_slot

    def decode(self, data: bytes) -> AnchorpyAccountType:
        return self.decode_class.decode(data)

    async def update(self, conn: AsyncClient) -> None:
        self.account = await self.fetch(conn, self.address)

    async def _subscribe(self, network: Network, commitment: Commitment) -> None:
        ws_endpoint = utils.cluster_endpoint(network, ws=True, whirligig=False)
        try:
            async with connect(ws_endpoint) as ws:
                await ws.account_subscribe(
                    self.address,
                    commitment=commitment,
                    encoding="base64",
                )
                first_resp = await ws.recv()
                first_resp[0].result
                while True:
                    msg = await ws.recv()
                    account = self.decode(msg[0].result.value.data)
                    self.account = account
                    self.last_update_slot = msg[0].result.context.slot
        except Exception as e:
            self._logger.error(f"Error subscribing to {self.account.__class__.__name__}: {e}")
        finally:
            self._subscription_task = None

    def subscribe(self, network: Network, commitment: Commitment) -> None:
        if self._is_subscribed:
            self._logger.warn(f"Already subscribed to {self.account.__class__.__name__}")
            return
        # Run the subscription in the background
        # TODO: worth threading this??
        self._subscription_task = asyncio.create_task(self._subscribe(network, commitment))
        self._logger.info(f"Subscribed to {self.account.__class__.__name__}")

    def unsubscribe(self) -> None:
        if not self._is_subscribed:
            self._logger.warn(f"Not subscribed to {self.account.__class__.__name__}")
            return
        self._subscription_task.cancel()
        self._subscription_task = None
        self._logger.info(f"Unsubscribed to {self.account.__class__.__name__}")


# Accounts layouts for those not automatically generated by AnchorPy


@dataclass
class Clock(AnchorpyAccount):
    layout: typing.ClassVar = SYSTEM_CLOCK_LAYOUT
    slot: int
    epoch_start_timestamp: int
    epoch: int
    leader_schedule_epoch: int
    unix_timestamp: int

    @classmethod
    def decode(cls, data: bytes) -> "Clock":
        dec = Clock.layout.parse(data)
        return cls(
            slot=dec.slot,
            epoch_start_timestamp=dec.epoch_start_timestamp,
            epoch=dec.epoch,
            leader_schedule_epoch=dec.leader_schedule_epoch,
            unix_timestamp=dec.unix_timestamp,
        )
