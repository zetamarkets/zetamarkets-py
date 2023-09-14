from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import EnumForCodegen


class UndefinedJSON(typing.TypedDict):
    kind: typing.Literal["Undefined"]


class LockJSON(typing.TypedDict):
    kind: typing.Literal["Lock"]


class UnlockJSON(typing.TypedDict):
    kind: typing.Literal["Unlock"]


@dataclass
class Undefined:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Undefined"

    @classmethod
    def to_json(cls) -> UndefinedJSON:
        return UndefinedJSON(
            kind="Undefined",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Undefined": {},
        }


@dataclass
class Lock:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Lock"

    @classmethod
    def to_json(cls) -> LockJSON:
        return LockJSON(
            kind="Lock",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Lock": {},
        }


@dataclass
class Unlock:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "Unlock"

    @classmethod
    def to_json(cls) -> UnlockJSON:
        return UnlockJSON(
            kind="Unlock",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Unlock": {},
        }


MovementTypeKind = typing.Union[Undefined, Lock, Unlock]
MovementTypeJSON = typing.Union[UndefinedJSON, LockJSON, UnlockJSON]


def from_decoded(obj: dict) -> MovementTypeKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Undefined" in obj:
        return Undefined()
    if "Lock" in obj:
        return Lock()
    if "Unlock" in obj:
        return Unlock()
    raise ValueError("Invalid enum object")


def from_json(obj: MovementTypeJSON) -> MovementTypeKind:
    if obj["kind"] == "Undefined":
        return Undefined()
    if obj["kind"] == "Lock":
        return Lock()
    if obj["kind"] == "Unlock":
        return Unlock()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen("Undefined" / borsh.CStruct(), "Lock" / borsh.CStruct(), "Unlock" / borsh.CStruct())
