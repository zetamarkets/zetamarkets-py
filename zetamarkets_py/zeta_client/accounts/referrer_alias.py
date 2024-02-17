import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import BorshPubkey
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class ReferrerAliasJSON(typing.TypedDict):
    nonce: int
    alias: list[int]
    referrer: str


@dataclass
class ReferrerAlias:
    discriminator: typing.ClassVar = b"\x87e\x9e\xdc&\x97\xbe:"
    layout: typing.ClassVar = borsh.CStruct("nonce" / borsh.U8, "alias" / borsh.U8[15], "referrer" / BorshPubkey)
    nonce: int
    alias: list[int]
    referrer: Pubkey

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["ReferrerAlias"]:
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
    ) -> typing.List[typing.Optional["ReferrerAlias"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["ReferrerAlias"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "ReferrerAlias":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = ReferrerAlias.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            nonce=dec.nonce,
            alias=dec.alias,
            referrer=dec.referrer,
        )

    def to_json(self) -> ReferrerAliasJSON:
        return {
            "nonce": self.nonce,
            "alias": self.alias,
            "referrer": str(self.referrer),
        }

    @classmethod
    def from_json(cls, obj: ReferrerAliasJSON) -> "ReferrerAlias":
        return cls(
            nonce=obj["nonce"],
            alias=obj["alias"],
            referrer=Pubkey.from_string(obj["referrer"]),
        )
