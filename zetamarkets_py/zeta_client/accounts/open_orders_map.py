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


class OpenOrdersMapJSON(typing.TypedDict):
    user_key: str


@dataclass
class OpenOrdersMap:
    discriminator: typing.ClassVar = b"\xfa~\xac\nv\x1e\x03\xa8"
    layout: typing.ClassVar = borsh.CStruct("user_key" / BorshPubkey)
    user_key: Pubkey

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["OpenOrdersMap"]:
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
    ) -> typing.List[typing.Optional["OpenOrdersMap"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["OpenOrdersMap"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "OpenOrdersMap":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = OpenOrdersMap.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            user_key=dec.user_key,
        )

    def to_json(self) -> OpenOrdersMapJSON:
        return {
            "user_key": str(self.user_key),
        }

    @classmethod
    def from_json(cls, obj: OpenOrdersMapJSON) -> "OpenOrdersMap":
        return cls(
            user_key=Pubkey.from_string(obj["user_key"]),
        )
