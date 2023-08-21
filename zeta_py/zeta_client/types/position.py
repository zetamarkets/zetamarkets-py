from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class PositionJSON(typing.TypedDict):
    size: int
    cost_of_trades: int


@dataclass
class Position:
    layout: typing.ClassVar = borsh.CStruct("size" / borsh.I64, "cost_of_trades" / borsh.U64)
    size: int
    cost_of_trades: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "Position":
        return cls(size=obj.size, cost_of_trades=obj.cost_of_trades)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"size": self.size, "cost_of_trades": self.cost_of_trades}

    def to_json(self) -> PositionJSON:
        return {"size": self.size, "cost_of_trades": self.cost_of_trades}

    @classmethod
    def from_json(cls, obj: PositionJSON) -> "Position":
        return cls(size=obj["size"], cost_of_trades=obj["cost_of_trades"])
