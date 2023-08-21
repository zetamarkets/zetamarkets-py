from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class ExpirySeriesJSON(typing.TypedDict):
    active_ts: int
    expiry_ts: int
    dirty: bool
    padding: list[int]


@dataclass
class ExpirySeries:
    layout: typing.ClassVar = borsh.CStruct(
        "active_ts" / borsh.U64,
        "expiry_ts" / borsh.U64,
        "dirty" / borsh.Bool,
        "padding" / borsh.U8[15],
    )
    active_ts: int
    expiry_ts: int
    dirty: bool
    padding: list[int]

    @classmethod
    def from_decoded(cls, obj: Container) -> "ExpirySeries":
        return cls(
            active_ts=obj.active_ts,
            expiry_ts=obj.expiry_ts,
            dirty=obj.dirty,
            padding=obj.padding,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "active_ts": self.active_ts,
            "expiry_ts": self.expiry_ts,
            "dirty": self.dirty,
            "padding": self.padding,
        }

    def to_json(self) -> ExpirySeriesJSON:
        return {
            "active_ts": self.active_ts,
            "expiry_ts": self.expiry_ts,
            "dirty": self.dirty,
            "padding": self.padding,
        }

    @classmethod
    def from_json(cls, obj: ExpirySeriesJSON) -> "ExpirySeries":
        return cls(
            active_ts=obj["active_ts"],
            expiry_ts=obj["expiry_ts"],
            dirty=obj["dirty"],
            padding=obj["padding"],
        )
