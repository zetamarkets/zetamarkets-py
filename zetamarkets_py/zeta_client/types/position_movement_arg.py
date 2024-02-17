from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class PositionMovementArgJSON(typing.TypedDict):
    index: int
    size: int


@dataclass
class PositionMovementArg:
    layout: typing.ClassVar = borsh.CStruct("index" / borsh.U8, "size" / borsh.I64)
    index: int
    size: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "PositionMovementArg":
        return cls(index=obj.index, size=obj.size)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"index": self.index, "size": self.size}

    def to_json(self) -> PositionMovementArgJSON:
        return {"index": self.index, "size": self.size}

    @classmethod
    def from_json(cls, obj: PositionMovementArgJSON) -> "PositionMovementArg":
        return cls(index=obj["index"], size=obj["size"])
