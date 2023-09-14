from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import EnumForCodegen


class MarginAccountJSON(typing.TypedDict):
    kind: typing.Literal["MarginAccount"]


class CrossMarginAccountJSON(typing.TypedDict):
    kind: typing.Literal["CrossMarginAccount"]


@dataclass
class MarginAccount:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "MarginAccount"

    @classmethod
    def to_json(cls) -> MarginAccountJSON:
        return MarginAccountJSON(
            kind="MarginAccount",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MarginAccount": {},
        }


@dataclass
class CrossMarginAccount:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "CrossMarginAccount"

    @classmethod
    def to_json(cls) -> CrossMarginAccountJSON:
        return CrossMarginAccountJSON(
            kind="CrossMarginAccount",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "CrossMarginAccount": {},
        }


TraitTypeKind = typing.Union[MarginAccount, CrossMarginAccount]
TraitTypeJSON = typing.Union[MarginAccountJSON, CrossMarginAccountJSON]


def from_decoded(obj: dict) -> TraitTypeKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "MarginAccount" in obj:
        return MarginAccount()
    if "CrossMarginAccount" in obj:
        return CrossMarginAccount()
    raise ValueError("Invalid enum object")


def from_json(obj: TraitTypeJSON) -> TraitTypeKind:
    if obj["kind"] == "MarginAccount":
        return MarginAccount()
    if obj["kind"] == "CrossMarginAccount":
        return CrossMarginAccount()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen("MarginAccount" / borsh.CStruct(), "CrossMarginAccount" / borsh.CStruct())
