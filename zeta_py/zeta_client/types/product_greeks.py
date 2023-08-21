from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container

from . import anchor_decimal


class ProductGreeksJSON(typing.TypedDict):
    delta: int
    vega: anchor_decimal.AnchorDecimalJSON
    volatility: anchor_decimal.AnchorDecimalJSON


@dataclass
class ProductGreeks:
    layout: typing.ClassVar = borsh.CStruct(
        "delta" / borsh.U64,
        "vega" / anchor_decimal.AnchorDecimal.layout,
        "volatility" / anchor_decimal.AnchorDecimal.layout,
    )
    delta: int
    vega: anchor_decimal.AnchorDecimal
    volatility: anchor_decimal.AnchorDecimal

    @classmethod
    def from_decoded(cls, obj: Container) -> "ProductGreeks":
        return cls(
            delta=obj.delta,
            vega=anchor_decimal.AnchorDecimal.from_decoded(obj.vega),
            volatility=anchor_decimal.AnchorDecimal.from_decoded(obj.volatility),
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "delta": self.delta,
            "vega": self.vega.to_encodable(),
            "volatility": self.volatility.to_encodable(),
        }

    def to_json(self) -> ProductGreeksJSON:
        return {
            "delta": self.delta,
            "vega": self.vega.to_json(),
            "volatility": self.volatility.to_json(),
        }

    @classmethod
    def from_json(cls, obj: ProductGreeksJSON) -> "ProductGreeks":
        return cls(
            delta=obj["delta"],
            vega=anchor_decimal.AnchorDecimal.from_json(obj["vega"]),
            volatility=anchor_decimal.AnchorDecimal.from_json(obj["volatility"]),
        )
