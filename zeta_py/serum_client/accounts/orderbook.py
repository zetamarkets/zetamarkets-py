import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


@dataclass
class OrderbookAccount:
    discriminator: typing.ClassVar = b"\x73\x65\x72\x75\x6D"
    layout: typing.ClassVar = borsh.CStruct(
        "account_flags" / types.account_flags.AccountFlags.layout,
        "slab" / types.slab.Slab.layout,
    )
    account_flags: types.account_flags.AccountFlags
    slab: types.slab.Slab

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["OrderbookAccount"]:
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
    ) -> typing.List[typing.Optional["OrderbookAccount"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["OrderbookAccount"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "OrderbookAccount":
        if data[: len(cls.discriminator)] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = OrderbookAccount.layout.parse(data[len(cls.discriminator) :])
        return cls(
            account_flags=types.account_flags.AccountFlags.from_decoded(dec.account_flags),
            slab=types.slab.Slab.from_decoded(dec.slab),
        )
