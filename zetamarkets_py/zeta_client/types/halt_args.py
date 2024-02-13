from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class HaltArgsJSON(typing.TypedDict):
    spot_prices: list[int]
    timestamp: int


@dataclass
class HaltArgs:
    layout: typing.ClassVar = borsh.CStruct("spot_prices" / borsh.U64[13], "timestamp" / borsh.U64)
    spot_prices: list[int]
    timestamp: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "HaltArgs":
        return cls(spot_prices=obj.spot_prices, timestamp=obj.timestamp)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"spot_prices": self.spot_prices, "timestamp": self.timestamp}

    def to_json(self) -> HaltArgsJSON:
        return {"spot_prices": self.spot_prices, "timestamp": self.timestamp}

    @classmethod
    def from_json(cls, obj: HaltArgsJSON) -> "HaltArgs":
        return cls(spot_prices=obj["spot_prices"], timestamp=obj["timestamp"])
