import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class MarketNodeJSON(typing.TypedDict):
    index: int
    nonce: int
    node_updates: list[int]
    interest_update: int


@dataclass
class MarketNode:
    discriminator: typing.ClassVar = b"\x1cR\x15;\x96\x8d<|"
    layout: typing.ClassVar = borsh.CStruct(
        "index" / borsh.U8,
        "nonce" / borsh.U8,
        "node_updates" / borsh.I64[5],
        "interest_update" / borsh.I64,
    )
    index: int
    nonce: int
    node_updates: list[int]
    interest_update: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["MarketNode"]:
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
    ) -> typing.List[typing.Optional["MarketNode"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["MarketNode"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "MarketNode":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = MarketNode.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            index=dec.index,
            nonce=dec.nonce,
            node_updates=dec.node_updates,
            interest_update=dec.interest_update,
        )

    def to_json(self) -> MarketNodeJSON:
        return {
            "index": self.index,
            "nonce": self.nonce,
            "node_updates": self.node_updates,
            "interest_update": self.interest_update,
        }

    @classmethod
    def from_json(cls, obj: MarketNodeJSON) -> "MarketNode":
        return cls(
            index=obj["index"],
            nonce=obj["nonce"],
            node_updates=obj["node_updates"],
            interest_update=obj["interest_update"],
        )
