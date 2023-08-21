from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container

from . import asset


class HaltStateArgsJSON(typing.TypedDict):
    asset: asset.AssetJSON
    spot_price: int
    timestamp: int


@dataclass
class HaltStateArgs:
    layout: typing.ClassVar = borsh.CStruct("asset" / asset.layout, "spot_price" / borsh.U64, "timestamp" / borsh.U64)
    asset: asset.AssetKind
    spot_price: int
    timestamp: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "HaltStateArgs":
        return cls(
            asset=asset.from_decoded(obj.asset),
            spot_price=obj.spot_price,
            timestamp=obj.timestamp,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "asset": self.asset.to_encodable(),
            "spot_price": self.spot_price,
            "timestamp": self.timestamp,
        }

    def to_json(self) -> HaltStateArgsJSON:
        return {
            "asset": self.asset.to_json(),
            "spot_price": self.spot_price,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_json(cls, obj: HaltStateArgsJSON) -> "HaltStateArgs":
        return cls(
            asset=asset.from_json(obj["asset"]),
            spot_price=obj["spot_price"],
            timestamp=obj["timestamp"],
        )
