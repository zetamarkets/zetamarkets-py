from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import BorshPubkey
from construct import BitsSwapped, BitStruct, Container, Flag, Padding
from solders.pubkey import Pubkey

from zetamarkets_py.serum_client import types


@dataclass
class EventFlags:
    layout: typing.ClassVar = BitsSwapped(
        BitStruct(
            "fill" / Flag,
            "out" / Flag,
            "bid" / Flag,
            "maker" / Flag,
            Padding(4),
        )
    )
    fill: bool
    out: bool
    bid: bool
    maker: bool

    @classmethod
    def from_decoded(cls, obj: Container) -> "EventFlags":
        return cls(
            fill=obj.fill,
            out=obj.out,
            bid=obj.bid,
            maker=obj.maker,
        )


@dataclass
class Event:
    layout: typing.ClassVar = borsh.CStruct(
        "event_flags" / EventFlags.layout,
        "open_order_slot" / borsh.U8,
        "fee_tier" / borsh.U8,
        "padding" / borsh.U8[5],
        "native_quantity_released" / borsh.U64,
        "native_quantity_paid" / borsh.U64,
        "native_fee_or_rebate" / borsh.U64,
        "order_id" / borsh.U128,
        "public_key" / BorshPubkey,
        "client_order_id" / borsh.U64,
    )
    event_flags: EventFlags
    open_order_slot: int
    fee_tier: int
    native_quantity_released: int
    native_quantity_paid: int
    native_fee_or_rebate: int
    order_id: int
    public_key: Pubkey
    client_order_id: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "Event":
        return cls(
            event_flags=EventFlags.from_decoded(obj.event_flags),
            open_order_slot=obj.open_order_slot,
            fee_tier=obj.fee_tier,
            native_quantity_released=obj.native_quantity_released,
            native_quantity_paid=obj.native_quantity_paid,
            native_fee_or_rebate=obj.native_fee_or_rebate,
            order_id=obj.order_id,
            public_key=obj.public_key,
            client_order_id=obj.client_order_id,
        )


@dataclass
class QueueHeader:
    layout: typing.ClassVar = borsh.CStruct(
        "padding_1" / borsh.U8[5],
        "account_flags" / types.account_flags.AccountFlags.layout,
        "head" / borsh.U32,
        "padding_2" / borsh.U8[4],
        "count" / borsh.U32,
        "padding_3" / borsh.U8[4],
        "next_seq_num" / borsh.U32,
        "padding_4" / borsh.U8[4],
    )
    account_flags: types.account_flags.AccountFlags
    head: int
    count: int
    next_seq_num: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "QueueHeader":
        return cls(
            account_flags=types.account_flags.AccountFlags.from_decoded(obj.account_flags),
            head=obj.head,
            count=obj.count,
            next_seq_num=obj.next_seq_num,
        )
