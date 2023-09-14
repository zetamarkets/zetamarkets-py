from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class CrossMarginAccountInfoJSON(typing.TypedDict):
    initialized: bool
    name: list[int]


@dataclass
class CrossMarginAccountInfo:
    layout: typing.ClassVar = borsh.CStruct("initialized" / borsh.Bool, "name" / borsh.U8[10])
    initialized: bool
    name: list[int]

    @classmethod
    def from_decoded(cls, obj: Container) -> "CrossMarginAccountInfo":
        return cls(initialized=obj.initialized, name=obj.name)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"initialized": self.initialized, "name": self.name}

    def to_json(self) -> CrossMarginAccountInfoJSON:
        return {"initialized": self.initialized, "name": self.name}

    @classmethod
    def from_json(cls, obj: CrossMarginAccountInfoJSON) -> "CrossMarginAccountInfo":
        return cls(initialized=obj["initialized"], name=obj["name"])
