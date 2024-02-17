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


class UnderlyingJSON(typing.TypedDict):
    mint: str


@dataclass
class Underlying:
    discriminator: typing.ClassVar = b"\xce\x80\x98Mp\xa4\r\x02"
    layout: typing.ClassVar = borsh.CStruct("mint" / BorshPubkey)
    mint: Pubkey

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["Underlying"]:
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
    ) -> typing.List[typing.Optional["Underlying"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["Underlying"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "Underlying":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = Underlying.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            mint=dec.mint,
        )

    def to_json(self) -> UnderlyingJSON:
        return {
            "mint": str(self.mint),
        }

    @classmethod
    def from_json(cls, obj: UnderlyingJSON) -> "Underlying":
        return cls(
            mint=Pubkey.from_string(obj["mint"]),
        )
