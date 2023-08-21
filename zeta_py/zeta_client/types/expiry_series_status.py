from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import EnumForCodegen


class UninitializedJSON(typing.TypedDict):
    kind: typing.Literal["Uninitialized"]


class InitializedJSON(typing.TypedDict):
    kind: typing.Literal["Initialized"]


class LiveJSON(typing.TypedDict):
    kind: typing.Literal["Live"]


class ExpiredJSON(typing.TypedDict):
    kind: typing.Literal["Expired"]


class ExpiredDirtyJSON(typing.TypedDict):
    kind: typing.Literal["ExpiredDirty"]


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
class Initialized:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Initialized"

    @classmethod
    def to_json(cls) -> InitializedJSON:
        return InitializedJSON(
            kind="Initialized",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Initialized": {},
        }


@dataclass
class Live:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "Live"

    @classmethod
    def to_json(cls) -> LiveJSON:
        return LiveJSON(
            kind="Live",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Live": {},
        }


@dataclass
class Expired:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "Expired"

    @classmethod
    def to_json(cls) -> ExpiredJSON:
        return ExpiredJSON(
            kind="Expired",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Expired": {},
        }


@dataclass
class ExpiredDirty:
    discriminator: typing.ClassVar = 4
    kind: typing.ClassVar = "ExpiredDirty"

    @classmethod
    def to_json(cls) -> ExpiredDirtyJSON:
        return ExpiredDirtyJSON(
            kind="ExpiredDirty",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ExpiredDirty": {},
        }


ExpirySeriesStatusKind = typing.Union[Uninitialized, Initialized, Live, Expired, ExpiredDirty]
ExpirySeriesStatusJSON = typing.Union[UninitializedJSON, InitializedJSON, LiveJSON, ExpiredJSON, ExpiredDirtyJSON]


def from_decoded(obj: dict) -> ExpirySeriesStatusKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Uninitialized" in obj:
        return Uninitialized()
    if "Initialized" in obj:
        return Initialized()
    if "Live" in obj:
        return Live()
    if "Expired" in obj:
        return Expired()
    if "ExpiredDirty" in obj:
        return ExpiredDirty()
    raise ValueError("Invalid enum object")


def from_json(obj: ExpirySeriesStatusJSON) -> ExpirySeriesStatusKind:
    if obj["kind"] == "Uninitialized":
        return Uninitialized()
    if obj["kind"] == "Initialized":
        return Initialized()
    if obj["kind"] == "Live":
        return Live()
    if obj["kind"] == "Expired":
        return Expired()
    if obj["kind"] == "ExpiredDirty":
        return ExpiredDirty()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Uninitialized" / borsh.CStruct(),
    "Initialized" / borsh.CStruct(),
    "Live" / borsh.CStruct(),
    "Expired" / borsh.CStruct(),
    "ExpiredDirty" / borsh.CStruct(),
)
