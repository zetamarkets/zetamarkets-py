from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class UpdateInterestRateArgsJSON(typing.TypedDict):
    expiry_index: int
    interest_rate: int


@dataclass
class UpdateInterestRateArgs:
    layout: typing.ClassVar = borsh.CStruct("expiry_index" / borsh.U8, "interest_rate" / borsh.I64)
    expiry_index: int
    interest_rate: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "UpdateInterestRateArgs":
        return cls(expiry_index=obj.expiry_index, interest_rate=obj.interest_rate)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"expiry_index": self.expiry_index, "interest_rate": self.interest_rate}

    def to_json(self) -> UpdateInterestRateArgsJSON:
        return {"expiry_index": self.expiry_index, "interest_rate": self.interest_rate}

    @classmethod
    def from_json(cls, obj: UpdateInterestRateArgsJSON) -> "UpdateInterestRateArgs":
        return cls(expiry_index=obj["expiry_index"], interest_rate=obj["interest_rate"])
