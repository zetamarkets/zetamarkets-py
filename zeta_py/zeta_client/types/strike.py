from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class StrikeJSON(typing.TypedDict):
    is_set: bool
    value: int


@dataclass
class Strike:
    layout: typing.ClassVar = borsh.CStruct("is_set" / borsh.Bool, "value" / borsh.U64)
    is_set: bool
    value: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "Strike":
        return cls(is_set=obj.is_set, value=obj.value)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"is_set": self.is_set, "value": self.value}

    def to_json(self) -> StrikeJSON:
        return {"is_set": self.is_set, "value": self.value}

    @classmethod
    def from_json(cls, obj: StrikeJSON) -> "Strike":
        return cls(is_set=obj["is_set"], value=obj["value"])
