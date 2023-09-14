from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import EnumForCodegen


class CancelJSON(typing.TypedDict):
    kind: typing.Literal["Cancel"]


class FillJSON(typing.TypedDict):
    kind: typing.Literal["Fill"]


class BootedJSON(typing.TypedDict):
    kind: typing.Literal["Booted"]


@dataclass
class Cancel:
    discriminator: typing.ClassVar = 0
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
class Fill:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Fill"

    @classmethod
    def to_json(cls) -> FillJSON:
        return FillJSON(
            kind="Fill",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Fill": {},
        }


@dataclass
class Booted:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "Booted"

    @classmethod
    def to_json(cls) -> BootedJSON:
        return BootedJSON(
            kind="Booted",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Booted": {},
        }


OrderCompleteTypeKind = typing.Union[Cancel, Fill, Booted]
OrderCompleteTypeJSON = typing.Union[CancelJSON, FillJSON, BootedJSON]


def from_decoded(obj: dict) -> OrderCompleteTypeKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Cancel" in obj:
        return Cancel()
    if "Fill" in obj:
        return Fill()
    if "Booted" in obj:
        return Booted()
    raise ValueError("Invalid enum object")


def from_json(obj: OrderCompleteTypeJSON) -> OrderCompleteTypeKind:
    if obj["kind"] == "Cancel":
        return Cancel()
    if obj["kind"] == "Fill":
        return Fill()
    if obj["kind"] == "Booted":
        return Booted()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen("Cancel" / borsh.CStruct(), "Fill" / borsh.CStruct(), "Booted" / borsh.CStruct())
