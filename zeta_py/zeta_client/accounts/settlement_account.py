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


class SettlementAccountJSON(typing.TypedDict):
    settlement_price: int
    strikes: list[int]


@dataclass
class SettlementAccount:
    discriminator: typing.ClassVar = b"Q*ho{Y\x92\xb4"
    layout: typing.ClassVar = borsh.CStruct("settlement_price" / borsh.U64, "strikes" / borsh.U64[23])
    settlement_price: int
    strikes: list[int]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["SettlementAccount"]:
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
    ) -> typing.List[typing.Optional["SettlementAccount"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["SettlementAccount"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "SettlementAccount":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = SettlementAccount.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            settlement_price=dec.settlement_price,
            strikes=dec.strikes,
        )

    def to_json(self) -> SettlementAccountJSON:
        return {
            "settlement_price": self.settlement_price,
            "strikes": self.strikes,
        }

    @classmethod
    def from_json(cls, obj: SettlementAccountJSON) -> "SettlementAccount":
        return cls(
            settlement_price=obj["settlement_price"],
            strikes=obj["strikes"],
        )
