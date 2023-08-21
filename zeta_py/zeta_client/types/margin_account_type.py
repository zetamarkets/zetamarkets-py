from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import EnumForCodegen


class NormalJSON(typing.TypedDict):
    kind: typing.Literal["Normal"]


class MarketMakerJSON(typing.TypedDict):
    kind: typing.Literal["MarketMaker"]


@dataclass
class Normal:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Normal"

    @classmethod
    def to_json(cls) -> NormalJSON:
        return NormalJSON(
            kind="Normal",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Normal": {},
        }


@dataclass
class MarketMaker:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "MarketMaker"

    @classmethod
    def to_json(cls) -> MarketMakerJSON:
        return MarketMakerJSON(
            kind="MarketMaker",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MarketMaker": {},
        }


MarginAccountTypeKind = typing.Union[Normal, MarketMaker]
MarginAccountTypeJSON = typing.Union[NormalJSON, MarketMakerJSON]


def from_decoded(obj: dict) -> MarginAccountTypeKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Normal" in obj:
        return Normal()
    if "MarketMaker" in obj:
        return MarketMaker()
    raise ValueError("Invalid enum object")


def from_json(obj: MarginAccountTypeJSON) -> MarginAccountTypeKind:
    if obj["kind"] == "Normal":
        return Normal()
    if obj["kind"] == "MarketMaker":
        return MarketMaker()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen("Normal" / borsh.CStruct(), "MarketMaker" / borsh.CStruct())
