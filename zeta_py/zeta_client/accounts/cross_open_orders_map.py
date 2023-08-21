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


class CrossOpenOrdersMapJSON(typing.TypedDict):
    user_key: str
    subaccount_index: int


@dataclass
class CrossOpenOrdersMap:
    discriminator: typing.ClassVar = b"\xc5\x18R\tR\x0e0\x9a"
    layout: typing.ClassVar = borsh.CStruct("user_key" / BorshPubkey, "subaccount_index" / borsh.U8)
    user_key: Pubkey
    subaccount_index: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["CrossOpenOrdersMap"]:
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
    ) -> typing.List[typing.Optional["CrossOpenOrdersMap"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["CrossOpenOrdersMap"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "CrossOpenOrdersMap":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = CrossOpenOrdersMap.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            user_key=dec.user_key,
            subaccount_index=dec.subaccount_index,
        )

    def to_json(self) -> CrossOpenOrdersMapJSON:
        return {
            "user_key": str(self.user_key),
            "subaccount_index": self.subaccount_index,
        }

    @classmethod
    def from_json(cls, obj: CrossOpenOrdersMapJSON) -> "CrossOpenOrdersMap":
        return cls(
            user_key=Pubkey.from_string(obj["user_key"]),
            subaccount_index=obj["subaccount_index"],
        )
