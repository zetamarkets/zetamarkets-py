from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class UpdatePricingParametersArgsJSON(typing.TypedDict):
    option_trade_normalizer: int
    future_trade_normalizer: int
    max_volatility_retreat: int
    max_interest_retreat: int
    min_delta: int
    max_delta: int
    min_interest_rate: int
    max_interest_rate: int
    min_volatility: int
    max_volatility: int


@dataclass
class UpdatePricingParametersArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "option_trade_normalizer" / borsh.U64,
        "future_trade_normalizer" / borsh.U64,
        "max_volatility_retreat" / borsh.U64,
        "max_interest_retreat" / borsh.U64,
        "min_delta" / borsh.U64,
        "max_delta" / borsh.U64,
        "min_interest_rate" / borsh.I64,
        "max_interest_rate" / borsh.I64,
        "min_volatility" / borsh.U64,
        "max_volatility" / borsh.U64,
    )
    option_trade_normalizer: int
    future_trade_normalizer: int
    max_volatility_retreat: int
    max_interest_retreat: int
    min_delta: int
    max_delta: int
    min_interest_rate: int
    max_interest_rate: int
    min_volatility: int
    max_volatility: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "UpdatePricingParametersArgs":
        return cls(
            option_trade_normalizer=obj.option_trade_normalizer,
            future_trade_normalizer=obj.future_trade_normalizer,
            max_volatility_retreat=obj.max_volatility_retreat,
            max_interest_retreat=obj.max_interest_retreat,
            min_delta=obj.min_delta,
            max_delta=obj.max_delta,
            min_interest_rate=obj.min_interest_rate,
            max_interest_rate=obj.max_interest_rate,
            min_volatility=obj.min_volatility,
            max_volatility=obj.max_volatility,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "option_trade_normalizer": self.option_trade_normalizer,
            "future_trade_normalizer": self.future_trade_normalizer,
            "max_volatility_retreat": self.max_volatility_retreat,
            "max_interest_retreat": self.max_interest_retreat,
            "min_delta": self.min_delta,
            "max_delta": self.max_delta,
            "min_interest_rate": self.min_interest_rate,
            "max_interest_rate": self.max_interest_rate,
            "min_volatility": self.min_volatility,
            "max_volatility": self.max_volatility,
        }

    def to_json(self) -> UpdatePricingParametersArgsJSON:
        return {
            "option_trade_normalizer": self.option_trade_normalizer,
            "future_trade_normalizer": self.future_trade_normalizer,
            "max_volatility_retreat": self.max_volatility_retreat,
            "max_interest_retreat": self.max_interest_retreat,
            "min_delta": self.min_delta,
            "max_delta": self.max_delta,
            "min_interest_rate": self.min_interest_rate,
            "max_interest_rate": self.max_interest_rate,
            "min_volatility": self.min_volatility,
            "max_volatility": self.max_volatility,
        }

    @classmethod
    def from_json(cls, obj: UpdatePricingParametersArgsJSON) -> "UpdatePricingParametersArgs":
        return cls(
            option_trade_normalizer=obj["option_trade_normalizer"],
            future_trade_normalizer=obj["future_trade_normalizer"],
            max_volatility_retreat=obj["max_volatility_retreat"],
            max_interest_retreat=obj["max_interest_retreat"],
            min_delta=obj["min_delta"],
            max_delta=obj["max_delta"],
            min_interest_rate=obj["min_interest_rate"],
            max_interest_rate=obj["max_interest_rate"],
            min_volatility=obj["min_volatility"],
            max_volatility=obj["max_volatility"],
        )
