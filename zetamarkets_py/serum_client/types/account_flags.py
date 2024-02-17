from __future__ import annotations

import typing
from dataclasses import dataclass

from construct import BitsInteger, BitsSwapped, BitStruct, Const, Container, Flag


class AccountFlagsJSON(typing.TypedDict):
    initialized: bool
    market: bool
    open_orders: bool
    request_queue: bool
    event_queue: bool
    bids: bool
    asks: bool
    disabled: bool
    closed: bool
    permissioned: bool
    crank_authority_required: bool


@dataclass
class AccountFlags:
    # idk if possible to represent this with borsh
    layout: typing.ClassVar = BitsSwapped(  # swap to little endian
        BitStruct(
            "initialized" / Flag,
            "market" / Flag,
            "open_orders" / Flag,
            "request_queue" / Flag,
            "event_queue" / Flag,
            "bids" / Flag,
            "asks" / Flag,
            "disabled" / Flag,
            "closed" / Flag,
            "permissioned" / Flag,
            "crank_authority_required" / Flag,
            Const(0, BitsInteger(53)),  # padding
        ),
    )
    initialized: bool
    market: bool
    open_orders: bool
    request_queue: bool
    event_queue: bool
    bids: bool
    asks: bool
    disabled: bool
    closed: bool
    permissioned: bool
    crank_authority_required: bool

    @classmethod
    def from_decoded(cls, obj: Container) -> "AccountFlags":
        return cls(
            initialized=obj.initialized,
            market=obj.market,
            open_orders=obj.open_orders,
            request_queue=obj.request_queue,
            event_queue=obj.event_queue,
            bids=obj.bids,
            asks=obj.asks,
            disabled=obj.disabled,
            closed=obj.closed,
            permissioned=obj.permissioned,
            crank_authority_required=obj.crank_authority_required,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "initialized": self.initialized,
            "market": self.market,
            "open_orders": self.open_orders,
            "request_queue": self.request_queue,
            "event_queue": self.event_queue,
            "bids": self.bids,
            "asks": self.asks,
            "disabled": self.disabled,
            "closed": self.closed,
            "permissioned": self.permissioned,
            "crank_authority_required": self.crank_authority_required,
        }

    def to_json(self) -> AccountFlagsJSON:
        return {
            "initialized": self.initialized,
            "market": self.market,
            "open_orders": self.open_orders,
            "request_queue": self.request_queue,
            "event_queue": self.event_queue,
            "bids": self.bids,
            "asks": self.asks,
            "disabled": self.disabled,
            "closed": self.closed,
            "permissioned": self.permissioned,
            "crank_authority_required": self.crank_authority_required,
        }

    @classmethod
    def from_json(cls, obj: AccountFlagsJSON) -> "AccountFlags":
        return cls(
            initialized=obj["initialized"],
            market=obj["market"],
            open_orders=obj["open_orders"],
            request_queue=obj["request_queue"],
            event_queue=obj["event_queue"],
            bids=obj["bids"],
            asks=obj["asks"],
            disabled=obj["disabled"],
            closed=obj["closed"],
            permissioned=obj["permissioned"],
            crank_authority_required=obj["crank_authority_required"],
        )
