from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class MarginParametersJSON(typing.TypedDict):
    future_margin_initial: int
    future_margin_maintenance: int


@dataclass
class MarginParameters:
    layout: typing.ClassVar = borsh.CStruct(
        "future_margin_initial" / borsh.U64, "future_margin_maintenance" / borsh.U64
    )
    future_margin_initial: int
    future_margin_maintenance: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "MarginParameters":
        return cls(
            future_margin_initial=obj.future_margin_initial,
            future_margin_maintenance=obj.future_margin_maintenance,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "future_margin_initial": self.future_margin_initial,
            "future_margin_maintenance": self.future_margin_maintenance,
        }

    def to_json(self) -> MarginParametersJSON:
        return {
            "future_margin_initial": self.future_margin_initial,
            "future_margin_maintenance": self.future_margin_maintenance,
        }

    @classmethod
    def from_json(cls, obj: MarginParametersJSON) -> "MarginParameters":
        return cls(
            future_margin_initial=obj["future_margin_initial"],
            future_margin_maintenance=obj["future_margin_maintenance"],
        )
