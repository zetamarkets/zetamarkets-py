from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class OverrideExpiryArgsJSON(typing.TypedDict):
    expiry_index: int
    active_ts: int
    expiry_ts: int


@dataclass
class OverrideExpiryArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "expiry_index" / borsh.U8, "active_ts" / borsh.U64, "expiry_ts" / borsh.U64
    )
    expiry_index: int
    active_ts: int
    expiry_ts: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "OverrideExpiryArgs":
        return cls(
            expiry_index=obj.expiry_index,
            active_ts=obj.active_ts,
            expiry_ts=obj.expiry_ts,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "expiry_index": self.expiry_index,
            "active_ts": self.active_ts,
            "expiry_ts": self.expiry_ts,
        }

    def to_json(self) -> OverrideExpiryArgsJSON:
        return {
            "expiry_index": self.expiry_index,
            "active_ts": self.active_ts,
            "expiry_ts": self.expiry_ts,
        }

    @classmethod
    def from_json(cls, obj: OverrideExpiryArgsJSON) -> "OverrideExpiryArgs":
        return cls(
            expiry_index=obj["expiry_index"],
            active_ts=obj["active_ts"],
            expiry_ts=obj["expiry_ts"],
        )
