from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class UpdateGreeksArgsJSON(typing.TypedDict):
    index: int
    theo: int
    delta: int
    gamma: int
    volatility: int


@dataclass
class UpdateGreeksArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "index" / borsh.U8,
        "theo" / borsh.U64,
        "delta" / borsh.U32,
        "gamma" / borsh.U32,
        "volatility" / borsh.U32,
    )
    index: int
    theo: int
    delta: int
    gamma: int
    volatility: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "UpdateGreeksArgs":
        return cls(
            index=obj.index,
            theo=obj.theo,
            delta=obj.delta,
            gamma=obj.gamma,
            volatility=obj.volatility,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "index": self.index,
            "theo": self.theo,
            "delta": self.delta,
            "gamma": self.gamma,
            "volatility": self.volatility,
        }

    def to_json(self) -> UpdateGreeksArgsJSON:
        return {
            "index": self.index,
            "theo": self.theo,
            "delta": self.delta,
            "gamma": self.gamma,
            "volatility": self.volatility,
        }

    @classmethod
    def from_json(cls, obj: UpdateGreeksArgsJSON) -> "UpdateGreeksArgs":
        return cls(
            index=obj["index"],
            theo=obj["theo"],
            delta=obj["delta"],
            gamma=obj["gamma"],
            volatility=obj["volatility"],
        )
