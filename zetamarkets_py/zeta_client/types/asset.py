from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import EnumForCodegen


class SOLJSON(typing.TypedDict):
    kind: typing.Literal["SOL"]


class BTCJSON(typing.TypedDict):
    kind: typing.Literal["BTC"]


class ETHJSON(typing.TypedDict):
    kind: typing.Literal["ETH"]


class APTJSON(typing.TypedDict):
    kind: typing.Literal["APT"]


class ARBJSON(typing.TypedDict):
    kind: typing.Literal["ARB"]


class UNDEFINEDJSON(typing.TypedDict):
    kind: typing.Literal["UNDEFINED"]


@dataclass
class SOL:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "SOL"

    @classmethod
    def to_json(cls) -> SOLJSON:
        return SOLJSON(
            kind="SOL",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "SOL": {},
        }


@dataclass
class BTC:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "BTC"

    @classmethod
    def to_json(cls) -> BTCJSON:
        return BTCJSON(
            kind="BTC",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "BTC": {},
        }


@dataclass
class ETH:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "ETH"

    @classmethod
    def to_json(cls) -> ETHJSON:
        return ETHJSON(
            kind="ETH",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ETH": {},
        }


@dataclass
class APT:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "APT"

    @classmethod
    def to_json(cls) -> APTJSON:
        return APTJSON(
            kind="APT",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "APT": {},
        }


@dataclass
class ARB:
    discriminator: typing.ClassVar = 4
    kind: typing.ClassVar = "ARB"

    @classmethod
    def to_json(cls) -> ARBJSON:
        return ARBJSON(
            kind="ARB",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ARB": {},
        }


@dataclass
class UNDEFINED:
    discriminator: typing.ClassVar = 5
    kind: typing.ClassVar = "UNDEFINED"

    @classmethod
    def to_json(cls) -> UNDEFINEDJSON:
        return UNDEFINEDJSON(
            kind="UNDEFINED",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "UNDEFINED": {},
        }


AssetKind = typing.Union[SOL, BTC, ETH, APT, ARB, UNDEFINED]
AssetJSON = typing.Union[SOLJSON, BTCJSON, ETHJSON, APTJSON, ARBJSON, UNDEFINEDJSON]


def from_decoded(obj: dict) -> AssetKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "SOL" in obj:
        return SOL()
    if "BTC" in obj:
        return BTC()
    if "ETH" in obj:
        return ETH()
    if "APT" in obj:
        return APT()
    if "ARB" in obj:
        return ARB()
    if "UNDEFINED" in obj:
        return UNDEFINED()
    raise ValueError("Invalid enum object")


def from_json(obj: AssetJSON) -> AssetKind:
    if obj["kind"] == "SOL":
        return SOL()
    if obj["kind"] == "BTC":
        return BTC()
    if obj["kind"] == "ETH":
        return ETH()
    if obj["kind"] == "APT":
        return APT()
    if obj["kind"] == "ARB":
        return ARB()
    if obj["kind"] == "UNDEFINED":
        return UNDEFINED()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "SOL" / borsh.CStruct(),
    "BTC" / borsh.CStruct(),
    "ETH" / borsh.CStruct(),
    "APT" / borsh.CStruct(),
    "ARB" / borsh.CStruct(),
    "UNDEFINED" / borsh.CStruct(),
)
