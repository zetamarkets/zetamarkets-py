import typing
from dataclasses import dataclass

import borsh_construct as borsh
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solders.sysvar import CLOCK


@dataclass
class Clock:
    layout: typing.ClassVar = borsh.CStruct(
        "slot" / borsh.U64,
        "epoch_start_timestamp" / borsh.I64,
        "epoch" / borsh.U64,
        "leader_schedule_epoch" / borsh.U64,
        "unix_timestamp" / borsh.I64,
    )
    slot: int
    epoch_start_timestamp: int
    epoch: int
    leader_schedule_epoch: int
    unix_timestamp: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.Optional["Clock"]:
        resp = await conn.get_account_info(CLOCK, commitment=commitment)
        info = resp.value
        if info is None:
            return None
        bytes_data = info.data
        return cls.decode(bytes_data)

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
