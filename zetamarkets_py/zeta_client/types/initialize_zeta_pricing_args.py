from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class InitializeZetaPricingArgsJSON(typing.TypedDict):
    min_funding_rate_percent: int
    max_funding_rate_percent: int
    perp_impact_cash_delta: int
    margin_initial: int
    margin_maintenance: int
    pricing_nonce: int


@dataclass
class InitializeZetaPricingArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "min_funding_rate_percent" / borsh.I64,
        "max_funding_rate_percent" / borsh.I64,
        "perp_impact_cash_delta" / borsh.U64,
        "margin_initial" / borsh.U64,
        "margin_maintenance" / borsh.U64,
        "pricing_nonce" / borsh.U8,
    )
    min_funding_rate_percent: int
    max_funding_rate_percent: int
    perp_impact_cash_delta: int
    margin_initial: int
    margin_maintenance: int
    pricing_nonce: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "InitializeZetaPricingArgs":
        return cls(
            min_funding_rate_percent=obj.min_funding_rate_percent,
            max_funding_rate_percent=obj.max_funding_rate_percent,
            perp_impact_cash_delta=obj.perp_impact_cash_delta,
            margin_initial=obj.margin_initial,
            margin_maintenance=obj.margin_maintenance,
            pricing_nonce=obj.pricing_nonce,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "min_funding_rate_percent": self.min_funding_rate_percent,
            "max_funding_rate_percent": self.max_funding_rate_percent,
            "perp_impact_cash_delta": self.perp_impact_cash_delta,
            "margin_initial": self.margin_initial,
            "margin_maintenance": self.margin_maintenance,
            "pricing_nonce": self.pricing_nonce,
        }

    def to_json(self) -> InitializeZetaPricingArgsJSON:
        return {
            "min_funding_rate_percent": self.min_funding_rate_percent,
            "max_funding_rate_percent": self.max_funding_rate_percent,
            "perp_impact_cash_delta": self.perp_impact_cash_delta,
            "margin_initial": self.margin_initial,
            "margin_maintenance": self.margin_maintenance,
            "pricing_nonce": self.pricing_nonce,
        }

    @classmethod
    def from_json(cls, obj: InitializeZetaPricingArgsJSON) -> "InitializeZetaPricingArgs":
        return cls(
            min_funding_rate_percent=obj["min_funding_rate_percent"],
            max_funding_rate_percent=obj["max_funding_rate_percent"],
            perp_impact_cash_delta=obj["perp_impact_cash_delta"],
            margin_initial=obj["margin_initial"],
            margin_maintenance=obj["margin_maintenance"],
            pricing_nonce=obj["pricing_nonce"],
        )
