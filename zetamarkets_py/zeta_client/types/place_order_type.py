from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import EnumForCodegen


class PlaceOrderJSON(typing.TypedDict):
    kind: typing.Literal["PlaceOrder"]


class PlacePerpOrderJSON(typing.TypedDict):
    kind: typing.Literal["PlacePerpOrder"]


@dataclass
class PlaceOrder:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "PlaceOrder"

    @classmethod
    def to_json(cls) -> PlaceOrderJSON:
        return PlaceOrderJSON(
            kind="PlaceOrder",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "PlaceOrder": {},
        }


@dataclass
class PlacePerpOrder:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "PlacePerpOrder"

    @classmethod
    def to_json(cls) -> PlacePerpOrderJSON:
        return PlacePerpOrderJSON(
            kind="PlacePerpOrder",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "PlacePerpOrder": {},
        }


PlaceOrderTypeKind = typing.Union[PlaceOrder, PlacePerpOrder]
PlaceOrderTypeJSON = typing.Union[PlaceOrderJSON, PlacePerpOrderJSON]


def from_decoded(obj: dict) -> PlaceOrderTypeKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "PlaceOrder" in obj:
        return PlaceOrder()
    if "PlacePerpOrder" in obj:
        return PlacePerpOrder()
    raise ValueError("Invalid enum object")


def from_json(obj: PlaceOrderTypeJSON) -> PlaceOrderTypeKind:
    if obj["kind"] == "PlaceOrder":
        return PlaceOrder()
    if obj["kind"] == "PlacePerpOrder":
        return PlacePerpOrder()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen("PlaceOrder" / borsh.CStruct(), "PlacePerpOrder" / borsh.CStruct())
