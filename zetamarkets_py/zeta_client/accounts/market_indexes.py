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


class MarketIndexesJSON(typing.TypedDict):
    nonce: int
    initialized: bool
    indexes: list[int]


@dataclass
class MarketIndexes:
    discriminator: typing.ClassVar = b"o\xcdi\x92\xdb\x89R\x17"
    layout: typing.ClassVar = borsh.CStruct("nonce" / borsh.U8, "initialized" / borsh.Bool, "indexes" / borsh.U8[138])
    nonce: int
    initialized: bool
    indexes: list[int]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["MarketIndexes"]:
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
    ) -> typing.List[typing.Optional["MarketIndexes"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["MarketIndexes"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "MarketIndexes":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = MarketIndexes.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            nonce=dec.nonce,
            initialized=dec.initialized,
            indexes=dec.indexes,
        )

    def to_json(self) -> MarketIndexesJSON:
        return {
            "nonce": self.nonce,
            "initialized": self.initialized,
            "indexes": self.indexes,
        }

    @classmethod
    def from_json(cls, obj: MarketIndexesJSON) -> "MarketIndexes":
        return cls(
            nonce=obj["nonce"],
            initialized=obj["initialized"],
            indexes=obj["indexes"],
        )
