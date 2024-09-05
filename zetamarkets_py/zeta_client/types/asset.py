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


class BNBJSON(typing.TypedDict):
    kind: typing.Literal["BNB"]


class PYTHJSON(typing.TypedDict):
    kind: typing.Literal["PYTH"]


class TIAJSON(typing.TypedDict):
    kind: typing.Literal["TIA"]


class JTOJSON(typing.TypedDict):
    kind: typing.Literal["JTO"]


class ONEMBONKJSON(typing.TypedDict):
    kind: typing.Literal["ONEMBONK"]


class SEIJSON(typing.TypedDict):
    kind: typing.Literal["SEI"]


class JUPJSON(typing.TypedDict):
    kind: typing.Literal["JUP"]


class DYMJSON(typing.TypedDict):
    kind: typing.Literal["DYM"]


class STRKJSON(typing.TypedDict):
    kind: typing.Literal["STRK"]


class WIFJSON(typing.TypedDict):
    kind: typing.Literal["WIF"]


class RNDRJSON(typing.TypedDict):
    kind: typing.Literal["RNDR"]


class TNSRJSON(typing.TypedDict):
    kind: typing.Literal["TNSR"]


class POPCATJSON(typing.TypedDict):
    kind: typing.Literal["POPCAT"]


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
class BNB:
    discriminator: typing.ClassVar = 5
    kind: typing.ClassVar = "BNB"

    @classmethod
    def to_json(cls) -> BNBJSON:
        return BNBJSON(
            kind="BNB",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "BNB": {},
        }


@dataclass
class PYTH:
    discriminator: typing.ClassVar = 6
    kind: typing.ClassVar = "PYTH"

    @classmethod
    def to_json(cls) -> PYTHJSON:
        return PYTHJSON(
            kind="PYTH",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "PYTH": {},
        }


@dataclass
class TIA:
    discriminator: typing.ClassVar = 7
    kind: typing.ClassVar = "TIA"

    @classmethod
    def to_json(cls) -> TIAJSON:
        return TIAJSON(
            kind="TIA",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "TIA": {},
        }


@dataclass
class JTO:
    discriminator: typing.ClassVar = 8
    kind: typing.ClassVar = "JTO"

    @classmethod
    def to_json(cls) -> JTOJSON:
        return JTOJSON(
            kind="JTO",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "JTO": {},
        }


@dataclass
class ONEMBONK:
    discriminator: typing.ClassVar = 9
    kind: typing.ClassVar = "ONEMBONK"

    @classmethod
    def to_json(cls) -> ONEMBONKJSON:
        return ONEMBONKJSON(
            kind="ONEMBONK",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ONEMBONK": {},
        }


@dataclass
class SEI:
    discriminator: typing.ClassVar = 10
    kind: typing.ClassVar = "SEI"

    @classmethod
    def to_json(cls) -> SEIJSON:
        return SEIJSON(
            kind="SEI",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "SEI": {},
        }


@dataclass
class JUP:
    discriminator: typing.ClassVar = 11
    kind: typing.ClassVar = "JUP"

    @classmethod
    def to_json(cls) -> JUPJSON:
        return JUPJSON(
            kind="JUP",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "JUP": {},
        }


@dataclass
class DYM:
    discriminator: typing.ClassVar = 12
    kind: typing.ClassVar = "DYM"

    @classmethod
    def to_json(cls) -> DYMJSON:
        return DYMJSON(
            kind="DYM",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "DYM": {},
        }


@dataclass
class STRK:
    discriminator: typing.ClassVar = 13
    kind: typing.ClassVar = "STRK"

    @classmethod
    def to_json(cls) -> STRKJSON:
        return STRKJSON(
            kind="STRK",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "STRK": {},
        }


@dataclass
class WIF:
    discriminator: typing.ClassVar = 14
    kind: typing.ClassVar = "WIF"

    @classmethod
    def to_json(cls) -> WIFJSON:
        return WIFJSON(
            kind="WIF",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "WIF": {},
        }


@dataclass
class RNDR:
    discriminator: typing.ClassVar = 15
    kind: typing.ClassVar = "RNDR"

    @classmethod
    def to_json(cls) -> RNDRJSON:
        return RNDRJSON(
            kind="RNDR",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "RNDR": {},
        }


@dataclass
class TNSR:
    discriminator: typing.ClassVar = 16
    kind: typing.ClassVar = "TNSR"

    @classmethod
    def to_json(cls) -> TNSRJSON:
        return TNSRJSON(
            kind="TNSR",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "TNSR": {},
        }


@dataclass
class POPCAT:
    discriminator: typing.ClassVar = 17
    kind: typing.ClassVar = "POPCAT"

    @classmethod
    def to_json(cls) -> POPCATJSON:
        return POPCATJSON(
            kind="POPCAT",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "POPCAT": {},
        }


@dataclass
class UNDEFINED:
    discriminator: typing.ClassVar = 18
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


AssetKind = typing.Union[
    SOL,
    BTC,
    ETH,
    APT,
    ARB,
    BNB,
    PYTH,
    TIA,
    JTO,
    ONEMBONK,
    SEI,
    JUP,
    DYM,
    STRK,
    WIF,
    RNDR,
    TNSR,
    POPCAT,
    UNDEFINED,
]
AssetJSON = typing.Union[
    SOLJSON,
    BTCJSON,
    ETHJSON,
    APTJSON,
    ARBJSON,
    BNBJSON,
    PYTHJSON,
    TIAJSON,
    JTOJSON,
    ONEMBONKJSON,
    SEIJSON,
    JUPJSON,
    DYMJSON,
    STRKJSON,
    WIFJSON,
    RNDRJSON,
    TNSRJSON,
    POPCATJSON,
    UNDEFINEDJSON,
]


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
    if "BNB" in obj:
        return BNB()
    if "PYTH" in obj:
        return PYTH()
    if "TIA" in obj:
        return TIA()
    if "JTO" in obj:
        return JTO()
    if "ONEMBONK" in obj:
        return ONEMBONK()
    if "SEI" in obj:
        return SEI()
    if "JUP" in obj:
        return JUP()
    if "DYM" in obj:
        return DYM()
    if "STRK" in obj:
        return STRK()
    if "WIF" in obj:
        return WIF()
    if "RNDR" in obj:
        return RNDR()
    if "TNSR" in obj:
        return TNSR()
    if "POPCAT" in obj:
        return POPCAT()
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
    if obj["kind"] == "BNB":
        return BNB()
    if obj["kind"] == "PYTH":
        return PYTH()
    if obj["kind"] == "TIA":
        return TIA()
    if obj["kind"] == "JTO":
        return JTO()
    if obj["kind"] == "ONEMBONK":
        return ONEMBONK()
    if obj["kind"] == "SEI":
        return SEI()
    if obj["kind"] == "JUP":
        return JUP()
    if obj["kind"] == "DYM":
        return DYM()
    if obj["kind"] == "STRK":
        return STRK()
    if obj["kind"] == "WIF":
        return WIF()
    if obj["kind"] == "RNDR":
        return RNDR()
    if obj["kind"] == "TNSR":
        return TNSR()
    if obj["kind"] == "POPCAT":
        return POPCAT()
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
    "BNB" / borsh.CStruct(),
    "PYTH" / borsh.CStruct(),
    "TIA" / borsh.CStruct(),
    "JTO" / borsh.CStruct(),
    "ONEMBONK" / borsh.CStruct(),
    "SEI" / borsh.CStruct(),
    "JUP" / borsh.CStruct(),
    "DYM" / borsh.CStruct(),
    "STRK" / borsh.CStruct(),
    "WIF" / borsh.CStruct(),
    "RNDR" / borsh.CStruct(),
    "TNSR" / borsh.CStruct(),
    "POPCAT" / borsh.CStruct(),
    "UNDEFINED" / borsh.CStruct(),
)
