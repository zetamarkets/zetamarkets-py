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


class ReferrerIdAccountJSON(typing.TypedDict):
    referrer_id: list[int]
    referrer_pubkey: str


@dataclass
class ReferrerIdAccount:
    discriminator: typing.ClassVar = b"\xcf\xc2N\x8a\x9eJ\xba\x7f"
    layout: typing.ClassVar = borsh.CStruct("referrer_id" / borsh.U8[6], "referrer_pubkey" / BorshPubkey)
    referrer_id: list[int]
    referrer_pubkey: Pubkey

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["ReferrerIdAccount"]:
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
    ) -> typing.List[typing.Optional["ReferrerIdAccount"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["ReferrerIdAccount"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "ReferrerIdAccount":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = ReferrerIdAccount.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            referrer_id=dec.referrer_id,
            referrer_pubkey=dec.referrer_pubkey,
        )

    def to_json(self) -> ReferrerIdAccountJSON:
        return {
            "referrer_id": self.referrer_id,
            "referrer_pubkey": str(self.referrer_pubkey),
        }

    @classmethod
    def from_json(cls, obj: ReferrerIdAccountJSON) -> "ReferrerIdAccount":
        return cls(
            referrer_id=obj["referrer_id"],
            referrer_pubkey=Pubkey.from_string(obj["referrer_pubkey"]),
        )
