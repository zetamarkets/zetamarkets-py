from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import EnumForCodegen


class PlaceJSON(typing.TypedDict):
    kind: typing.Literal["Place"]


class CancelJSON(typing.TypedDict):
    kind: typing.Literal["Cancel"]


class OpenOrdersJSON(typing.TypedDict):
    kind: typing.Literal["OpenOrders"]


class LiquidateJSON(typing.TypedDict):
    kind: typing.Literal["Liquidate"]


@dataclass
class Place:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Place"

    @classmethod
    def to_json(cls) -> PlaceJSON:
        return PlaceJSON(
            kind="Place",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Place": {},
        }


@dataclass
class Cancel:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Cancel"

    @classmethod
    def to_json(cls) -> CancelJSON:
        return CancelJSON(
            kind="Cancel",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Cancel": {},
        }


@dataclass
class OpenOrders:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "OpenOrders"

    @classmethod
    def to_json(cls) -> OpenOrdersJSON:
        return OpenOrdersJSON(
            kind="OpenOrders",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "OpenOrders": {},
        }


@dataclass
class Liquidate:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "Liquidate"

    @classmethod
    def to_json(cls) -> LiquidateJSON:
        return LiquidateJSON(
            kind="Liquidate",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Liquidate": {},
        }


ValidationTypeKind = typing.Union[Place, Cancel, OpenOrders, Liquidate]
ValidationTypeJSON = typing.Union[PlaceJSON, CancelJSON, OpenOrdersJSON, LiquidateJSON]


def from_decoded(obj: dict) -> ValidationTypeKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Place" in obj:
        return Place()
    if "Cancel" in obj:
        return Cancel()
    if "OpenOrders" in obj:
        return OpenOrders()
    if "Liquidate" in obj:
        return Liquidate()
    raise ValueError("Invalid enum object")


def from_json(obj: ValidationTypeJSON) -> ValidationTypeKind:
    if obj["kind"] == "Place":
        return Place()
    if obj["kind"] == "Cancel":
        return Cancel()
    if obj["kind"] == "OpenOrders":
        return OpenOrders()
    if obj["kind"] == "Liquidate":
        return Liquidate()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Place" / borsh.CStruct(),
    "Cancel" / borsh.CStruct(),
    "OpenOrders" / borsh.CStruct(),
    "Liquidate" / borsh.CStruct(),
)
