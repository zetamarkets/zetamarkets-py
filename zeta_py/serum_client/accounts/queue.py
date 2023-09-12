import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.utils.rpc import get_multiple_accounts
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


@dataclass
class EventQueue:
    layout: typing.ClassVar = borsh.CStruct(
        "header" / types.queue.QueueHeader.layout,
        "nodes" / types.queue.Event.layout[lambda this: this.header.count],
    )
    header: types.queue.QueueHeader
    nodes: list[types.queue.Event]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["EventQueue"]:
        resp = await conn.get_account_info(address, commitment=commitment)
        info = resp.value
        if info is None:
            return None
        if info.owner != program_id:
            raise ValueError("Account does not belong to this program")
        bytes_data = info.data
        return cls.decode(bytes_data)

    @classmethod
    async def fetch_multiple(
        cls,
        conn: AsyncClient,
        addresses: list[Pubkey],
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.List[typing.Optional["EventQueue"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["EventQueue"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "EventQueue":
        dec = EventQueue.layout.parse(data)
        return cls(
            header=types.queue.QueueHeader.from_decoded(dec.header),
            nodes=list(
                map(
                    lambda item: types.queue.Event.from_decoded(item),
                    dec.nodes,
                )
            ),
        )
