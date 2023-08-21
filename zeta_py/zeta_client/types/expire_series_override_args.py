from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class ExpireSeriesOverrideArgsJSON(typing.TypedDict):
    settlement_nonce: int
    settlement_price: int


@dataclass
class ExpireSeriesOverrideArgs:
    layout: typing.ClassVar = borsh.CStruct("settlement_nonce" / borsh.U8, "settlement_price" / borsh.U64)
    settlement_nonce: int
    settlement_price: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "ExpireSeriesOverrideArgs":
        return cls(settlement_nonce=obj.settlement_nonce, settlement_price=obj.settlement_price)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "settlement_nonce": self.settlement_nonce,
            "settlement_price": self.settlement_price,
        }

    def to_json(self) -> ExpireSeriesOverrideArgsJSON:
        return {
            "settlement_nonce": self.settlement_nonce,
            "settlement_price": self.settlement_price,
        }

    @classmethod
    def from_json(cls, obj: ExpireSeriesOverrideArgsJSON) -> "ExpireSeriesOverrideArgs":
        return cls(
            settlement_nonce=obj["settlement_nonce"],
            settlement_price=obj["settlement_price"],
        )
