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


class SocializedLossAccountJSON(typing.TypedDict):
    nonce: int
    overbankrupt_amount: int


@dataclass
class SocializedLossAccount:
    discriminator: typing.ClassVar = b"A\xfe\x8d\xeb<Th\x89"
    layout: typing.ClassVar = borsh.CStruct("nonce" / borsh.U8, "overbankrupt_amount" / borsh.U64)
    nonce: int
    overbankrupt_amount: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["SocializedLossAccount"]:
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
    ) -> typing.List[typing.Optional["SocializedLossAccount"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["SocializedLossAccount"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "SocializedLossAccount":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = SocializedLossAccount.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            nonce=dec.nonce,
            overbankrupt_amount=dec.overbankrupt_amount,
        )

    def to_json(self) -> SocializedLossAccountJSON:
        return {
            "nonce": self.nonce,
            "overbankrupt_amount": self.overbankrupt_amount,
        }

    @classmethod
    def from_json(cls, obj: SocializedLossAccountJSON) -> "SocializedLossAccount":
        return cls(
            nonce=obj["nonce"],
            overbankrupt_amount=obj["overbankrupt_amount"],
        )
