from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import EnumForCodegen


class LimitJSON(typing.TypedDict):
    kind: typing.Literal["Limit"]


class PostOnlyJSON(typing.TypedDict):
    kind: typing.Literal["PostOnly"]


class FillOrKillJSON(typing.TypedDict):
    kind: typing.Literal["FillOrKill"]


class ImmediateOrCancelJSON(typing.TypedDict):
    kind: typing.Literal["ImmediateOrCancel"]


class PostOnlySlideJSON(typing.TypedDict):
    kind: typing.Literal["PostOnlySlide"]


class PostOnlyFrontJSON(typing.TypedDict):
    kind: typing.Literal["PostOnlyFront"]


@dataclass
class Limit:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Limit"

    @classmethod
    def to_json(cls) -> LimitJSON:
        return LimitJSON(
            kind="Limit",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Limit": {},
        }


@dataclass
class PostOnly:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "PostOnly"

    @classmethod
    def to_json(cls) -> PostOnlyJSON:
        return PostOnlyJSON(
            kind="PostOnly",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "PostOnly": {},
        }


@dataclass
class FillOrKill:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "FillOrKill"

    @classmethod
    def to_json(cls) -> FillOrKillJSON:
        return FillOrKillJSON(
            kind="FillOrKill",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "FillOrKill": {},
        }


@dataclass
class ImmediateOrCancel:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "ImmediateOrCancel"

    @classmethod
    def to_json(cls) -> ImmediateOrCancelJSON:
        return ImmediateOrCancelJSON(
            kind="ImmediateOrCancel",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ImmediateOrCancel": {},
        }


@dataclass
class PostOnlySlide:
    discriminator: typing.ClassVar = 4
    kind: typing.ClassVar = "PostOnlySlide"

    @classmethod
    def to_json(cls) -> PostOnlySlideJSON:
        return PostOnlySlideJSON(
            kind="PostOnlySlide",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "PostOnlySlide": {},
        }


@dataclass
class PostOnlyFront:
    discriminator: typing.ClassVar = 5
    kind: typing.ClassVar = "PostOnlyFront"

    @classmethod
    def to_json(cls) -> PostOnlyFrontJSON:
        return PostOnlyFrontJSON(
            kind="PostOnlyFront",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "PostOnlyFront": {},
        }


OrderTypeKind = typing.Union[Limit, PostOnly, FillOrKill, ImmediateOrCancel, PostOnlySlide, PostOnlyFront]
OrderTypeJSON = typing.Union[
    LimitJSON,
    PostOnlyJSON,
    FillOrKillJSON,
    ImmediateOrCancelJSON,
    PostOnlySlideJSON,
    PostOnlyFrontJSON,
]


def from_decoded(obj: dict) -> OrderTypeKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Limit" in obj:
        return Limit()
    if "PostOnly" in obj:
        return PostOnly()
    if "FillOrKill" in obj:
        return FillOrKill()
    if "ImmediateOrCancel" in obj:
        return ImmediateOrCancel()
    if "PostOnlySlide" in obj:
        return PostOnlySlide()
    if "PostOnlyFront" in obj:
        return PostOnlyFront()
    raise ValueError("Invalid enum object")


def from_json(obj: OrderTypeJSON) -> OrderTypeKind:
    if obj["kind"] == "Limit":
        return Limit()
    if obj["kind"] == "PostOnly":
        return PostOnly()
    if obj["kind"] == "FillOrKill":
        return FillOrKill()
    if obj["kind"] == "ImmediateOrCancel":
        return ImmediateOrCancel()
    if obj["kind"] == "PostOnlySlide":
        return PostOnlySlide()
    if obj["kind"] == "PostOnlyFront":
        return PostOnlyFront()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Limit" / borsh.CStruct(),
    "PostOnly" / borsh.CStruct(),
    "FillOrKill" / borsh.CStruct(),
    "ImmediateOrCancel" / borsh.CStruct(),
    "PostOnlySlide" / borsh.CStruct(),
    "PostOnlyFront" / borsh.CStruct(),
)
