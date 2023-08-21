from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import EnumForCodegen


class UninitializedJSON(typing.TypedDict):
    kind: typing.Literal["Uninitialized"]


class CallJSON(typing.TypedDict):
    kind: typing.Literal["Call"]


class PutJSON(typing.TypedDict):
    kind: typing.Literal["Put"]


class FutureJSON(typing.TypedDict):
    kind: typing.Literal["Future"]


class PerpJSON(typing.TypedDict):
    kind: typing.Literal["Perp"]


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
class Call:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Call"

    @classmethod
    def to_json(cls) -> CallJSON:
        return CallJSON(
            kind="Call",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Call": {},
        }


@dataclass
class Put:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "Put"

    @classmethod
    def to_json(cls) -> PutJSON:
        return PutJSON(
            kind="Put",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Put": {},
        }


@dataclass
class Future:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "Future"

    @classmethod
    def to_json(cls) -> FutureJSON:
        return FutureJSON(
            kind="Future",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Future": {},
        }


@dataclass
class Perp:
    discriminator: typing.ClassVar = 4
    kind: typing.ClassVar = "Perp"

    @classmethod
    def to_json(cls) -> PerpJSON:
        return PerpJSON(
            kind="Perp",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Perp": {},
        }


KindKind = typing.Union[Uninitialized, Call, Put, Future, Perp]
KindJSON = typing.Union[UninitializedJSON, CallJSON, PutJSON, FutureJSON, PerpJSON]


def from_decoded(obj: dict) -> KindKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Uninitialized" in obj:
        return Uninitialized()
    if "Call" in obj:
        return Call()
    if "Put" in obj:
        return Put()
    if "Future" in obj:
        return Future()
    if "Perp" in obj:
        return Perp()
    raise ValueError("Invalid enum object")


def from_json(obj: KindJSON) -> KindKind:
    if obj["kind"] == "Uninitialized":
        return Uninitialized()
    if obj["kind"] == "Call":
        return Call()
    if obj["kind"] == "Put":
        return Put()
    if obj["kind"] == "Future":
        return Future()
    if obj["kind"] == "Perp":
        return Perp()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Uninitialized" / borsh.CStruct(),
    "Call" / borsh.CStruct(),
    "Put" / borsh.CStruct(),
    "Future" / borsh.CStruct(),
    "Perp" / borsh.CStruct(),
)
