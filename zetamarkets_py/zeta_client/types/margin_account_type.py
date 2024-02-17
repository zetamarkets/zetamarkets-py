from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import EnumForCodegen


class NormalJSON(typing.TypedDict):
    kind: typing.Literal["Normal"]


class MarketMakerJSON(typing.TypedDict):
    kind: typing.Literal["MarketMaker"]


class MarketMakerT1JSON(typing.TypedDict):
    kind: typing.Literal["MarketMakerT1"]


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


@dataclass
class MarketMakerT1:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "MarketMakerT1"

    @classmethod
    def to_json(cls) -> MarketMakerT1JSON:
        return MarketMakerT1JSON(
            kind="MarketMakerT1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MarketMakerT1": {},
        }


MarginAccountTypeKind = typing.Union[Normal, MarketMaker, MarketMakerT1]
MarginAccountTypeJSON = typing.Union[NormalJSON, MarketMakerJSON, MarketMakerT1JSON]


def from_decoded(obj: dict) -> MarginAccountTypeKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Normal" in obj:
        return Normal()
    if "MarketMaker" in obj:
        return MarketMaker()
    if "MarketMakerT1" in obj:
        return MarketMakerT1()
    raise ValueError("Invalid enum object")


def from_json(obj: MarginAccountTypeJSON) -> MarginAccountTypeKind:
    if obj["kind"] == "Normal":
        return Normal()
    if obj["kind"] == "MarketMaker":
        return MarketMaker()
    if obj["kind"] == "MarketMakerT1":
        return MarketMakerT1()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Normal" / borsh.CStruct(),
    "MarketMaker" / borsh.CStruct(),
    "MarketMakerT1" / borsh.CStruct(),
)
