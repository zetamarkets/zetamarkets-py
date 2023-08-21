from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class UpdateZetaGroupExpiryArgsJSON(typing.TypedDict):
    expiry_interval_seconds: int
    new_expiry_threshold_seconds: int


@dataclass
class UpdateZetaGroupExpiryArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "expiry_interval_seconds" / borsh.U32,
        "new_expiry_threshold_seconds" / borsh.U32,
    )
    expiry_interval_seconds: int
    new_expiry_threshold_seconds: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "UpdateZetaGroupExpiryArgs":
        return cls(
            expiry_interval_seconds=obj.expiry_interval_seconds,
            new_expiry_threshold_seconds=obj.new_expiry_threshold_seconds,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "expiry_interval_seconds": self.expiry_interval_seconds,
            "new_expiry_threshold_seconds": self.new_expiry_threshold_seconds,
        }

    def to_json(self) -> UpdateZetaGroupExpiryArgsJSON:
        return {
            "expiry_interval_seconds": self.expiry_interval_seconds,
            "new_expiry_threshold_seconds": self.new_expiry_threshold_seconds,
        }

    @classmethod
    def from_json(cls, obj: UpdateZetaGroupExpiryArgsJSON) -> "UpdateZetaGroupExpiryArgs":
        return cls(
            expiry_interval_seconds=obj["expiry_interval_seconds"],
            new_expiry_threshold_seconds=obj["new_expiry_threshold_seconds"],
        )
