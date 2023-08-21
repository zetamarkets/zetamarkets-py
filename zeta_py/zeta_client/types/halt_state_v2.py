from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class HaltStateV2JSON(typing.TypedDict):
    halted: bool
    timestamp: int
    spot_price: int
    market_cleaned: bool


@dataclass
class HaltStateV2:
    layout: typing.ClassVar = borsh.CStruct(
        "halted" / borsh.Bool,
        "timestamp" / borsh.U64,
        "spot_price" / borsh.U64,
        "market_cleaned" / borsh.Bool,
    )
    halted: bool
    timestamp: int
    spot_price: int
    market_cleaned: bool

    @classmethod
    def from_decoded(cls, obj: Container) -> "HaltStateV2":
        return cls(
            halted=obj.halted,
            timestamp=obj.timestamp,
            spot_price=obj.spot_price,
            market_cleaned=obj.market_cleaned,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "halted": self.halted,
            "timestamp": self.timestamp,
            "spot_price": self.spot_price,
            "market_cleaned": self.market_cleaned,
        }

    def to_json(self) -> HaltStateV2JSON:
        return {
            "halted": self.halted,
            "timestamp": self.timestamp,
            "spot_price": self.spot_price,
            "market_cleaned": self.market_cleaned,
        }

    @classmethod
    def from_json(cls, obj: HaltStateV2JSON) -> "HaltStateV2":
        return cls(
            halted=obj["halted"],
            timestamp=obj["timestamp"],
            spot_price=obj["spot_price"],
            market_cleaned=obj["market_cleaned"],
        )
