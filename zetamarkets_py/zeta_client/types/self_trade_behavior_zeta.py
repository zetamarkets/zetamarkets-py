from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class CancelProvideJSON(typing.TypedDict):
    kind: typing.Literal["CancelProvide"]


class AbortTransactionJSON(typing.TypedDict):
    kind: typing.Literal["AbortTransaction"]


@dataclass
class CancelProvide:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "CancelProvide"

    @classmethod
    def to_json(cls) -> CancelProvideJSON:
        return CancelProvideJSON(
            kind="CancelProvide",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "CancelProvide": {},
        }


@dataclass
class AbortTransaction:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "AbortTransaction"

    @classmethod
    def to_json(cls) -> AbortTransactionJSON:
        return AbortTransactionJSON(
            kind="AbortTransaction",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "AbortTransaction": {},
        }


SelfTradeBehaviorZetaKind = typing.Union[CancelProvide, AbortTransaction]
SelfTradeBehaviorZetaJSON = typing.Union[CancelProvideJSON, AbortTransactionJSON]


def from_decoded(obj: dict) -> SelfTradeBehaviorZetaKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "CancelProvide" in obj:
        return CancelProvide()
    if "AbortTransaction" in obj:
        return AbortTransaction()
    raise ValueError("Invalid enum object")


def from_json(obj: SelfTradeBehaviorZetaJSON) -> SelfTradeBehaviorZetaKind:
    if obj["kind"] == "CancelProvide":
        return CancelProvide()
    if obj["kind"] == "AbortTransaction":
        return AbortTransaction()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "CancelProvide" / borsh.CStruct(), "AbortTransaction" / borsh.CStruct()
)
