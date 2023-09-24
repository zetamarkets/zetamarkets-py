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


class MarketStateJSON(typing.TypedDict):
    account_flags: types.account_flags.AccountFlagsJSON
    own_address: str
    vault_signer_nonce: int
    base_mint: str
    quote_mint: str
    base_vault: str
    base_deposits_total: int
    base_fees_accrued: int
    quote_vault: str
    quote_deposits_total: int
    quote_fees_accrued: int
    quote_dust_threshold: int
    request_queue: str
    event_queue: str
    bids: str
    asks: str
    base_lot_size: int
    quote_lot_size: int
    fee_rate_bps: int
    referrer_rebate_accrued: int
    open_orders_authority: str
    prune_authority: str
    consume_events_authority: str
    epoch_length: int
    epoch_start_ts: int
    start_epoch_seq_num: int


@dataclass
class MarketState:
    discriminator: typing.ClassVar = b"\x73\x65\x72\x75\x6D"
    layout: typing.ClassVar = borsh.CStruct(
        "account_flags" / types.account_flags.AccountFlags.layout,
        "own_address" / BorshPubkey,
        "vault_signer_nonce" / borsh.U64,
        "base_mint" / BorshPubkey,
        "quote_mint" / BorshPubkey,
        "base_vault" / BorshPubkey,
        "base_deposits_total" / borsh.U64,
        "base_fees_accrued" / borsh.U64,
        "quote_vault" / BorshPubkey,
        "quote_deposits_total" / borsh.U64,
        "quote_fees_accrued" / borsh.U64,
        "quote_dust_threshold" / borsh.U64,
        "request_queue" / BorshPubkey,
        "event_queue" / BorshPubkey,
        "bids" / BorshPubkey,
        "asks" / BorshPubkey,
        "base_lot_size" / borsh.U64,
        "quote_lot_size" / borsh.U64,
        "fee_rate_bps" / borsh.U64,
        "referrer_rebate_accrued" / borsh.U64,
        "open_orders_authority" / BorshPubkey,
        "prune_authority" / BorshPubkey,
        "consume_events_authority" / BorshPubkey,
        "epoch_length" / borsh.U16,
        "epoch_start_ts" / borsh.U64,
        "start_epoch_seq_num" / borsh.U64,
        "padding" / borsh.U8[981],  # padding
    )
    account_flags: types.account_flags.AccountFlags
    own_address: Pubkey
    vault_signer_nonce: int
    base_mint: Pubkey
    quote_mint: Pubkey
    base_vault: Pubkey
    base_deposits_total: int
    base_fees_accrued: int
    quote_vault: Pubkey
    quote_deposits_total: int
    quote_fees_accrued: int
    quote_dust_threshold: int
    request_queue: Pubkey
    event_queue: Pubkey
    bids: Pubkey
    asks: Pubkey
    base_lot_size: int
    quote_lot_size: int
    fee_rate_bps: int
    referrer_rebate_accrued: int
    open_orders_authority: Pubkey
    prune_authority: Pubkey
    consume_events_authority: Pubkey
    epoch_length: int
    epoch_start_ts: int
    start_epoch_seq_num: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["MarketState"]:
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
    ) -> typing.List[typing.Optional["MarketState"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["MarketState"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "MarketState":
        if data[: len(cls.discriminator)] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = MarketState.layout.parse(data[len(cls.discriminator) :])
        return cls(
            account_flags=types.account_flags.AccountFlags.from_decoded(dec.account_flags),
            own_address=dec.own_address,
            vault_signer_nonce=dec.vault_signer_nonce,
            base_mint=dec.base_mint,
            quote_mint=dec.quote_mint,
            base_vault=dec.base_vault,
            base_deposits_total=dec.base_deposits_total,
            base_fees_accrued=dec.base_fees_accrued,
            quote_vault=dec.quote_vault,
            quote_deposits_total=dec.quote_deposits_total,
            quote_fees_accrued=dec.quote_fees_accrued,
            quote_dust_threshold=dec.quote_dust_threshold,
            request_queue=dec.request_queue,
            event_queue=dec.event_queue,
            bids=dec.bids,
            asks=dec.asks,
            base_lot_size=dec.base_lot_size,
            quote_lot_size=dec.quote_lot_size,
            fee_rate_bps=dec.fee_rate_bps,
            referrer_rebate_accrued=dec.referrer_rebate_accrued,
            open_orders_authority=dec.open_orders_authority,
            prune_authority=dec.prune_authority,
            consume_events_authority=dec.consume_events_authority,
            epoch_length=dec.epoch_length,
            epoch_start_ts=dec.epoch_start_ts,
            start_epoch_seq_num=dec.start_epoch_seq_num,
        )
