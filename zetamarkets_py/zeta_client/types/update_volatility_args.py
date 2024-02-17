from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class UpdateVolatilityArgsJSON(typing.TypedDict):
    expiry_index: int
    volatility: list[int]


@dataclass
class UpdateVolatilityArgs:
    layout: typing.ClassVar = borsh.CStruct("expiry_index" / borsh.U8, "volatility" / borsh.U64[5])
    expiry_index: int
    volatility: list[int]

    @classmethod
    def from_decoded(cls, obj: Container) -> "UpdateVolatilityArgs":
        return cls(expiry_index=obj.expiry_index, volatility=obj.volatility)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"expiry_index": self.expiry_index, "volatility": self.volatility}

    def to_json(self) -> UpdateVolatilityArgsJSON:
        return {"expiry_index": self.expiry_index, "volatility": self.volatility}

    @classmethod
    def from_json(cls, obj: UpdateVolatilityArgsJSON) -> "UpdateVolatilityArgs":
        return cls(expiry_index=obj["expiry_index"], volatility=obj["volatility"])
