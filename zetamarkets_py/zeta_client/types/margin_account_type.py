from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import EnumForCodegen


class NormalJSON(typing.TypedDict):
    kind: typing.Literal["Normal"]


class MarketMakerJSON(typing.TypedDict):
    kind: typing.Literal["MarketMaker"]


class MarketMakerT1JSON(typing.TypedDict):
    kind: typing.Literal["MarketMakerT1"]


class MarketMakerT0JSON(typing.TypedDict):
    kind: typing.Literal["MarketMakerT0"]


class MarketMakerT2JSON(typing.TypedDict):
    kind: typing.Literal["MarketMakerT2"]


class MarketMakerT3JSON(typing.TypedDict):
    kind: typing.Literal["MarketMakerT3"]


class MarketMakerT4JSON(typing.TypedDict):
    kind: typing.Literal["MarketMakerT4"]


class MarketMakerT5JSON(typing.TypedDict):
    kind: typing.Literal["MarketMakerT5"]


class MarketMakerT6JSON(typing.TypedDict):
    kind: typing.Literal["MarketMakerT6"]


class MarketMakerT7JSON(typing.TypedDict):
    kind: typing.Literal["MarketMakerT7"]


class MarketMakerT8JSON(typing.TypedDict):
    kind: typing.Literal["MarketMakerT8"]


class MarketMakerT9JSON(typing.TypedDict):
    kind: typing.Literal["MarketMakerT9"]


class NormalT1JSON(typing.TypedDict):
    kind: typing.Literal["NormalT1"]


class NormalT2JSON(typing.TypedDict):
    kind: typing.Literal["NormalT2"]


class NormalT3JSON(typing.TypedDict):
    kind: typing.Literal["NormalT3"]


class NormalT4JSON(typing.TypedDict):
    kind: typing.Literal["NormalT4"]


class NormalT5JSON(typing.TypedDict):
    kind: typing.Literal["NormalT5"]


class NormalT6JSON(typing.TypedDict):
    kind: typing.Literal["NormalT6"]


class NormalT7JSON(typing.TypedDict):
    kind: typing.Literal["NormalT7"]


class NormalT8JSON(typing.TypedDict):
    kind: typing.Literal["NormalT8"]


class NormalT9JSON(typing.TypedDict):
    kind: typing.Literal["NormalT9"]


class WithdrawOnlyJSON(typing.TypedDict):
    kind: typing.Literal["WithdrawOnly"]


@dataclass
class Normal:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Normal"

    @classmethod
    def to_json(cls) -> NormalJSON:
        return NormalJSON(
            kind="Normal",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Normal": {},
        }


@dataclass
class MarketMaker:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "MarketMaker"

    @classmethod
    def to_json(cls) -> MarketMakerJSON:
        return MarketMakerJSON(
            kind="MarketMaker",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MarketMaker": {},
        }


@dataclass
class MarketMakerT1:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "MarketMakerT1"

    @classmethod
    def to_json(cls) -> MarketMakerT1JSON:
        return MarketMakerT1JSON(
            kind="MarketMakerT1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MarketMakerT1": {},
        }


@dataclass
class MarketMakerT0:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "MarketMakerT0"

    @classmethod
    def to_json(cls) -> MarketMakerT0JSON:
        return MarketMakerT0JSON(
            kind="MarketMakerT0",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MarketMakerT0": {},
        }


@dataclass
class MarketMakerT2:
    discriminator: typing.ClassVar = 4
    kind: typing.ClassVar = "MarketMakerT2"

    @classmethod
    def to_json(cls) -> MarketMakerT2JSON:
        return MarketMakerT2JSON(
            kind="MarketMakerT2",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MarketMakerT2": {},
        }


@dataclass
class MarketMakerT3:
    discriminator: typing.ClassVar = 5
    kind: typing.ClassVar = "MarketMakerT3"

    @classmethod
    def to_json(cls) -> MarketMakerT3JSON:
        return MarketMakerT3JSON(
            kind="MarketMakerT3",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MarketMakerT3": {},
        }


@dataclass
class MarketMakerT4:
    discriminator: typing.ClassVar = 6
    kind: typing.ClassVar = "MarketMakerT4"

    @classmethod
    def to_json(cls) -> MarketMakerT4JSON:
        return MarketMakerT4JSON(
            kind="MarketMakerT4",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MarketMakerT4": {},
        }


@dataclass
class MarketMakerT5:
    discriminator: typing.ClassVar = 7
    kind: typing.ClassVar = "MarketMakerT5"

    @classmethod
    def to_json(cls) -> MarketMakerT5JSON:
        return MarketMakerT5JSON(
            kind="MarketMakerT5",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MarketMakerT5": {},
        }


@dataclass
class MarketMakerT6:
    discriminator: typing.ClassVar = 8
    kind: typing.ClassVar = "MarketMakerT6"

    @classmethod
    def to_json(cls) -> MarketMakerT6JSON:
        return MarketMakerT6JSON(
            kind="MarketMakerT6",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MarketMakerT6": {},
        }


@dataclass
class MarketMakerT7:
    discriminator: typing.ClassVar = 9
    kind: typing.ClassVar = "MarketMakerT7"

    @classmethod
    def to_json(cls) -> MarketMakerT7JSON:
        return MarketMakerT7JSON(
            kind="MarketMakerT7",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MarketMakerT7": {},
        }


@dataclass
class MarketMakerT8:
    discriminator: typing.ClassVar = 10
    kind: typing.ClassVar = "MarketMakerT8"

    @classmethod
    def to_json(cls) -> MarketMakerT8JSON:
        return MarketMakerT8JSON(
            kind="MarketMakerT8",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MarketMakerT8": {},
        }


@dataclass
class MarketMakerT9:
    discriminator: typing.ClassVar = 11
    kind: typing.ClassVar = "MarketMakerT9"

    @classmethod
    def to_json(cls) -> MarketMakerT9JSON:
        return MarketMakerT9JSON(
            kind="MarketMakerT9",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MarketMakerT9": {},
        }


@dataclass
class NormalT1:
    discriminator: typing.ClassVar = 12
    kind: typing.ClassVar = "NormalT1"

    @classmethod
    def to_json(cls) -> NormalT1JSON:
        return NormalT1JSON(
            kind="NormalT1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "NormalT1": {},
        }


@dataclass
class NormalT2:
    discriminator: typing.ClassVar = 13
    kind: typing.ClassVar = "NormalT2"

    @classmethod
    def to_json(cls) -> NormalT2JSON:
        return NormalT2JSON(
            kind="NormalT2",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "NormalT2": {},
        }


@dataclass
class NormalT3:
    discriminator: typing.ClassVar = 14
    kind: typing.ClassVar = "NormalT3"

    @classmethod
    def to_json(cls) -> NormalT3JSON:
        return NormalT3JSON(
            kind="NormalT3",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "NormalT3": {},
        }


@dataclass
class NormalT4:
    discriminator: typing.ClassVar = 15
    kind: typing.ClassVar = "NormalT4"

    @classmethod
    def to_json(cls) -> NormalT4JSON:
        return NormalT4JSON(
            kind="NormalT4",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "NormalT4": {},
        }


@dataclass
class NormalT5:
    discriminator: typing.ClassVar = 16
    kind: typing.ClassVar = "NormalT5"

    @classmethod
    def to_json(cls) -> NormalT5JSON:
        return NormalT5JSON(
            kind="NormalT5",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "NormalT5": {},
        }


@dataclass
class NormalT6:
    discriminator: typing.ClassVar = 17
    kind: typing.ClassVar = "NormalT6"

    @classmethod
    def to_json(cls) -> NormalT6JSON:
        return NormalT6JSON(
            kind="NormalT6",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "NormalT6": {},
        }


@dataclass
class NormalT7:
    discriminator: typing.ClassVar = 18
    kind: typing.ClassVar = "NormalT7"

    @classmethod
    def to_json(cls) -> NormalT7JSON:
        return NormalT7JSON(
            kind="NormalT7",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "NormalT7": {},
        }


@dataclass
class NormalT8:
    discriminator: typing.ClassVar = 19
    kind: typing.ClassVar = "NormalT8"

    @classmethod
    def to_json(cls) -> NormalT8JSON:
        return NormalT8JSON(
            kind="NormalT8",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "NormalT8": {},
        }


@dataclass
class NormalT9:
    discriminator: typing.ClassVar = 20
    kind: typing.ClassVar = "NormalT9"

    @classmethod
    def to_json(cls) -> NormalT9JSON:
        return NormalT9JSON(
            kind="NormalT9",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "NormalT9": {},
        }


@dataclass
class WithdrawOnly:
    discriminator: typing.ClassVar = 21
    kind: typing.ClassVar = "WithdrawOnly"

    @classmethod
    def to_json(cls) -> WithdrawOnlyJSON:
        return WithdrawOnlyJSON(
            kind="WithdrawOnly",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "WithdrawOnly": {},
        }


MarginAccountTypeKind = typing.Union[
    Normal,
    MarketMaker,
    MarketMakerT1,
    MarketMakerT0,
    MarketMakerT2,
    MarketMakerT3,
    MarketMakerT4,
    MarketMakerT5,
    MarketMakerT6,
    MarketMakerT7,
    MarketMakerT8,
    MarketMakerT9,
    NormalT1,
    NormalT2,
    NormalT3,
    NormalT4,
    NormalT5,
    NormalT6,
    NormalT7,
    NormalT8,
    NormalT9,
    WithdrawOnly,
]
MarginAccountTypeJSON = typing.Union[
    NormalJSON,
    MarketMakerJSON,
    MarketMakerT1JSON,
    MarketMakerT0JSON,
    MarketMakerT2JSON,
    MarketMakerT3JSON,
    MarketMakerT4JSON,
    MarketMakerT5JSON,
    MarketMakerT6JSON,
    MarketMakerT7JSON,
    MarketMakerT8JSON,
    MarketMakerT9JSON,
    NormalT1JSON,
    NormalT2JSON,
    NormalT3JSON,
    NormalT4JSON,
    NormalT5JSON,
    NormalT6JSON,
    NormalT7JSON,
    NormalT8JSON,
    NormalT9JSON,
    WithdrawOnlyJSON,
]


def from_decoded(obj: dict) -> MarginAccountTypeKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Normal" in obj:
        return Normal()
    if "MarketMaker" in obj:
        return MarketMaker()
    if "MarketMakerT1" in obj:
        return MarketMakerT1()
    if "MarketMakerT0" in obj:
        return MarketMakerT0()
    if "MarketMakerT2" in obj:
        return MarketMakerT2()
    if "MarketMakerT3" in obj:
        return MarketMakerT3()
    if "MarketMakerT4" in obj:
        return MarketMakerT4()
    if "MarketMakerT5" in obj:
        return MarketMakerT5()
    if "MarketMakerT6" in obj:
        return MarketMakerT6()
    if "MarketMakerT7" in obj:
        return MarketMakerT7()
    if "MarketMakerT8" in obj:
        return MarketMakerT8()
    if "MarketMakerT9" in obj:
        return MarketMakerT9()
    if "NormalT1" in obj:
        return NormalT1()
    if "NormalT2" in obj:
        return NormalT2()
    if "NormalT3" in obj:
        return NormalT3()
    if "NormalT4" in obj:
        return NormalT4()
    if "NormalT5" in obj:
        return NormalT5()
    if "NormalT6" in obj:
        return NormalT6()
    if "NormalT7" in obj:
        return NormalT7()
    if "NormalT8" in obj:
        return NormalT8()
    if "NormalT9" in obj:
        return NormalT9()
    if "WithdrawOnly" in obj:
        return WithdrawOnly()
    raise ValueError("Invalid enum object")


def from_json(obj: MarginAccountTypeJSON) -> MarginAccountTypeKind:
    if obj["kind"] == "Normal":
        return Normal()
    if obj["kind"] == "MarketMaker":
        return MarketMaker()
    if obj["kind"] == "MarketMakerT1":
        return MarketMakerT1()
    if obj["kind"] == "MarketMakerT0":
        return MarketMakerT0()
    if obj["kind"] == "MarketMakerT2":
        return MarketMakerT2()
    if obj["kind"] == "MarketMakerT3":
        return MarketMakerT3()
    if obj["kind"] == "MarketMakerT4":
        return MarketMakerT4()
    if obj["kind"] == "MarketMakerT5":
        return MarketMakerT5()
    if obj["kind"] == "MarketMakerT6":
        return MarketMakerT6()
    if obj["kind"] == "MarketMakerT7":
        return MarketMakerT7()
    if obj["kind"] == "MarketMakerT8":
        return MarketMakerT8()
    if obj["kind"] == "MarketMakerT9":
        return MarketMakerT9()
    if obj["kind"] == "NormalT1":
        return NormalT1()
    if obj["kind"] == "NormalT2":
        return NormalT2()
    if obj["kind"] == "NormalT3":
        return NormalT3()
    if obj["kind"] == "NormalT4":
        return NormalT4()
    if obj["kind"] == "NormalT5":
        return NormalT5()
    if obj["kind"] == "NormalT6":
        return NormalT6()
    if obj["kind"] == "NormalT7":
        return NormalT7()
    if obj["kind"] == "NormalT8":
        return NormalT8()
    if obj["kind"] == "NormalT9":
        return NormalT9()
    if obj["kind"] == "WithdrawOnly":
        return WithdrawOnly()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Normal" / borsh.CStruct(),
    "MarketMaker" / borsh.CStruct(),
    "MarketMakerT1" / borsh.CStruct(),
    "MarketMakerT0" / borsh.CStruct(),
    "MarketMakerT2" / borsh.CStruct(),
    "MarketMakerT3" / borsh.CStruct(),
    "MarketMakerT4" / borsh.CStruct(),
    "MarketMakerT5" / borsh.CStruct(),
    "MarketMakerT6" / borsh.CStruct(),
    "MarketMakerT7" / borsh.CStruct(),
    "MarketMakerT8" / borsh.CStruct(),
    "MarketMakerT9" / borsh.CStruct(),
    "NormalT1" / borsh.CStruct(),
    "NormalT2" / borsh.CStruct(),
    "NormalT3" / borsh.CStruct(),
    "NormalT4" / borsh.CStruct(),
    "NormalT5" / borsh.CStruct(),
    "NormalT6" / borsh.CStruct(),
    "NormalT7" / borsh.CStruct(),
    "NormalT8" / borsh.CStruct(),
    "NormalT9" / borsh.CStruct(),
    "WithdrawOnly" / borsh.CStruct(),
)
