from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container

from . import anchor_decimal


class PricingParametersJSON(typing.TypedDict):
    option_trade_normalizer: anchor_decimal.AnchorDecimalJSON
    future_trade_normalizer: anchor_decimal.AnchorDecimalJSON
    max_volatility_retreat: anchor_decimal.AnchorDecimalJSON
    max_interest_retreat: anchor_decimal.AnchorDecimalJSON
    max_delta: int
    min_delta: int
    min_volatility: int
    max_volatility: int
    min_interest_rate: int
    max_interest_rate: int


@dataclass
class PricingParameters:
    layout: typing.ClassVar = borsh.CStruct(
        "option_trade_normalizer" / anchor_decimal.AnchorDecimal.layout,
        "future_trade_normalizer" / anchor_decimal.AnchorDecimal.layout,
        "max_volatility_retreat" / anchor_decimal.AnchorDecimal.layout,
        "max_interest_retreat" / anchor_decimal.AnchorDecimal.layout,
        "max_delta" / borsh.U64,
        "min_delta" / borsh.U64,
        "min_volatility" / borsh.U64,
        "max_volatility" / borsh.U64,
        "min_interest_rate" / borsh.I64,
        "max_interest_rate" / borsh.I64,
    )
    option_trade_normalizer: anchor_decimal.AnchorDecimal
    future_trade_normalizer: anchor_decimal.AnchorDecimal
    max_volatility_retreat: anchor_decimal.AnchorDecimal
    max_interest_retreat: anchor_decimal.AnchorDecimal
    max_delta: int
    min_delta: int
    min_volatility: int
    max_volatility: int
    min_interest_rate: int
    max_interest_rate: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "PricingParameters":
        return cls(
            option_trade_normalizer=anchor_decimal.AnchorDecimal.from_decoded(obj.option_trade_normalizer),
            future_trade_normalizer=anchor_decimal.AnchorDecimal.from_decoded(obj.future_trade_normalizer),
            max_volatility_retreat=anchor_decimal.AnchorDecimal.from_decoded(obj.max_volatility_retreat),
            max_interest_retreat=anchor_decimal.AnchorDecimal.from_decoded(obj.max_interest_retreat),
            max_delta=obj.max_delta,
            min_delta=obj.min_delta,
            min_volatility=obj.min_volatility,
            max_volatility=obj.max_volatility,
            min_interest_rate=obj.min_interest_rate,
            max_interest_rate=obj.max_interest_rate,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "option_trade_normalizer": self.option_trade_normalizer.to_encodable(),
            "future_trade_normalizer": self.future_trade_normalizer.to_encodable(),
            "max_volatility_retreat": self.max_volatility_retreat.to_encodable(),
            "max_interest_retreat": self.max_interest_retreat.to_encodable(),
            "max_delta": self.max_delta,
            "min_delta": self.min_delta,
            "min_volatility": self.min_volatility,
            "max_volatility": self.max_volatility,
            "min_interest_rate": self.min_interest_rate,
            "max_interest_rate": self.max_interest_rate,
        }

    def to_json(self) -> PricingParametersJSON:
        return {
            "option_trade_normalizer": self.option_trade_normalizer.to_json(),
            "future_trade_normalizer": self.future_trade_normalizer.to_json(),
            "max_volatility_retreat": self.max_volatility_retreat.to_json(),
            "max_interest_retreat": self.max_interest_retreat.to_json(),
            "max_delta": self.max_delta,
            "min_delta": self.min_delta,
            "min_volatility": self.min_volatility,
            "max_volatility": self.max_volatility,
            "min_interest_rate": self.min_interest_rate,
            "max_interest_rate": self.max_interest_rate,
        }

    @classmethod
    def from_json(cls, obj: PricingParametersJSON) -> "PricingParameters":
        return cls(
            option_trade_normalizer=anchor_decimal.AnchorDecimal.from_json(obj["option_trade_normalizer"]),
            future_trade_normalizer=anchor_decimal.AnchorDecimal.from_json(obj["future_trade_normalizer"]),
            max_volatility_retreat=anchor_decimal.AnchorDecimal.from_json(obj["max_volatility_retreat"]),
            max_interest_retreat=anchor_decimal.AnchorDecimal.from_json(obj["max_interest_retreat"]),
            max_delta=obj["max_delta"],
            min_delta=obj["min_delta"],
            min_volatility=obj["min_volatility"],
            max_volatility=obj["max_volatility"],
            min_interest_rate=obj["min_interest_rate"],
            max_interest_rate=obj["max_interest_rate"],
        )
