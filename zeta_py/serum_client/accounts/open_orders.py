import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import BorshPubkey
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


@dataclass
class OpenOrders:
    discriminator: typing.ClassVar = b"\x73\x65\x72\x75\x6D"
    layout: typing.ClassVar = borsh.CStruct(
        "account_flags" / types.account_flags.AccountFlags.layout,
        "market" / BorshPubkey,
        "owner" / BorshPubkey,
        "base_token_free" / borsh.U64,
        "base_token_total" / borsh.U64,
        "quote_token_free" / borsh.U64,
        "quote_token_total" / borsh.U64,
        "free_slot_bits" / borsh.U128,
        "is_bid_bits" / borsh.U128,
        "orders" / borsh.U128[128],
        "client_ids" / borsh.U64[128],
        "referrer_rebate_accrued" / borsh.U64,
        "padding" / borsh.U8[7],
    )
    account_flags: types.account_flags.AccountFlags
    market: Pubkey
    owner: Pubkey
    base_token_free: int
    base_token_total: int
    quote_token_free: int
    quote_token_total: int
    free_slot_bits: int
    is_bid_bits: int
    orders: list[int]
    client_ids: list[int]
    referrer_rebate_accrued: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["OpenOrders"]:
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
    ) -> typing.List[typing.Optional["OpenOrders"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["OpenOrders"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "OpenOrders":
        if data[: len(cls.discriminator)] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = OpenOrders.layout.parse(data[len(cls.discriminator) :])
        return cls(
            account_flags=types.account_flags.AccountFlags.from_decoded(dec.account_flags),
            market=dec.market,
            owner=dec.owner,
            base_token_free=dec.base_token_free,
            base_token_total=dec.base_token_total,
            quote_token_free=dec.quote_token_free,
            quote_token_total=dec.quote_token_total,
            free_slot_bits=dec.free_slot_bits,
            is_bid_bits=dec.is_bid_bits,
            orders=dec.orders,
            client_ids=dec.client_ids,
            referrer_rebate_accrued=dec.referrer_rebate_accrued,
        )
