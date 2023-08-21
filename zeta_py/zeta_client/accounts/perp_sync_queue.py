import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class PerpSyncQueueJSON(typing.TypedDict):
    nonce: int
    head: int
    length: int
    queue: list[types.anchor_decimal.AnchorDecimalJSON]


@dataclass
class PerpSyncQueue:
    discriminator: typing.ClassVar = b"\\78\x9d\xe6\xb8\xabB"
    layout: typing.ClassVar = borsh.CStruct(
        "nonce" / borsh.U8,
        "head" / borsh.U16,
        "length" / borsh.U16,
        "queue" / types.anchor_decimal.AnchorDecimal.layout[600],
    )
    nonce: int
    head: int
    length: int
    queue: list[types.anchor_decimal.AnchorDecimal]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["PerpSyncQueue"]:
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
    ) -> typing.List[typing.Optional["PerpSyncQueue"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["PerpSyncQueue"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "PerpSyncQueue":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = PerpSyncQueue.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            nonce=dec.nonce,
            head=dec.head,
            length=dec.length,
            queue=list(
                map(
                    lambda item: types.anchor_decimal.AnchorDecimal.from_decoded(item),
                    dec.queue,
                )
            ),
        )

    def to_json(self) -> PerpSyncQueueJSON:
        return {
            "nonce": self.nonce,
            "head": self.head,
            "length": self.length,
            "queue": list(map(lambda item: item.to_json(), self.queue)),
        }

    @classmethod
    def from_json(cls, obj: PerpSyncQueueJSON) -> "PerpSyncQueue":
        return cls(
            nonce=obj["nonce"],
            head=obj["head"],
            length=obj["length"],
            queue=list(
                map(
                    lambda item: types.anchor_decimal.AnchorDecimal.from_json(item),
                    obj["queue"],
                )
            ),
        )
