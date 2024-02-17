from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import EnumForCodegen


class UninitializedJSON(typing.TypedDict):
    kind: typing.Literal["Uninitialized"]


class LessThanOrEqualJSON(typing.TypedDict):
    kind: typing.Literal["LessThanOrEqual"]


class GreaterThanOrEqualJSON(typing.TypedDict):
    kind: typing.Literal["GreaterThanOrEqual"]


@dataclass
class Uninitialized:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Uninitialized"

    @classmethod
    def to_json(cls) -> UninitializedJSON:
        return UninitializedJSON(
            kind="Uninitialized",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Uninitialized": {},
        }


@dataclass
class LessThanOrEqual:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "LessThanOrEqual"

    @classmethod
    def to_json(cls) -> LessThanOrEqualJSON:
        return LessThanOrEqualJSON(
            kind="LessThanOrEqual",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "LessThanOrEqual": {},
        }


@dataclass
class GreaterThanOrEqual:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "GreaterThanOrEqual"

    @classmethod
    def to_json(cls) -> GreaterThanOrEqualJSON:
        return GreaterThanOrEqualJSON(
            kind="GreaterThanOrEqual",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "GreaterThanOrEqual": {},
        }


TriggerDirectionKind = typing.Union[Uninitialized, LessThanOrEqual, GreaterThanOrEqual]
TriggerDirectionJSON = typing.Union[UninitializedJSON, LessThanOrEqualJSON, GreaterThanOrEqualJSON]


def from_decoded(obj: dict) -> TriggerDirectionKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Uninitialized" in obj:
        return Uninitialized()
    if "LessThanOrEqual" in obj:
        return LessThanOrEqual()
    if "GreaterThanOrEqual" in obj:
        return GreaterThanOrEqual()
    raise ValueError("Invalid enum object")


def from_json(obj: TriggerDirectionJSON) -> TriggerDirectionKind:
    if obj["kind"] == "Uninitialized":
        return Uninitialized()
    if obj["kind"] == "LessThanOrEqual":
        return LessThanOrEqual()
    if obj["kind"] == "GreaterThanOrEqual":
        return GreaterThanOrEqual()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Uninitialized" / borsh.CStruct(),
    "LessThanOrEqual" / borsh.CStruct(),
    "GreaterThanOrEqual" / borsh.CStruct(),
)
