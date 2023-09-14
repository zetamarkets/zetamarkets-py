from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import EnumForCodegen


class UndefinedJSON(typing.TypedDict):
    kind: typing.Literal["Undefined"]


class ToTreasuryFromInsuranceJSON(typing.TypedDict):
    kind: typing.Literal["ToTreasuryFromInsurance"]


class ToInsuranceFromTreasuryJSON(typing.TypedDict):
    kind: typing.Literal["ToInsuranceFromTreasury"]


class ToTreasuryFromReferralsRewardsJSON(typing.TypedDict):
    kind: typing.Literal["ToTreasuryFromReferralsRewards"]


class ToReferralsRewardsFromTreasuryJSON(typing.TypedDict):
    kind: typing.Literal["ToReferralsRewardsFromTreasury"]


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
class ToTreasuryFromInsurance:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "ToTreasuryFromInsurance"

    @classmethod
    def to_json(cls) -> ToTreasuryFromInsuranceJSON:
        return ToTreasuryFromInsuranceJSON(
            kind="ToTreasuryFromInsurance",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ToTreasuryFromInsurance": {},
        }


@dataclass
class ToInsuranceFromTreasury:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "ToInsuranceFromTreasury"

    @classmethod
    def to_json(cls) -> ToInsuranceFromTreasuryJSON:
        return ToInsuranceFromTreasuryJSON(
            kind="ToInsuranceFromTreasury",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ToInsuranceFromTreasury": {},
        }


@dataclass
class ToTreasuryFromReferralsRewards:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "ToTreasuryFromReferralsRewards"

    @classmethod
    def to_json(cls) -> ToTreasuryFromReferralsRewardsJSON:
        return ToTreasuryFromReferralsRewardsJSON(
            kind="ToTreasuryFromReferralsRewards",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ToTreasuryFromReferralsRewards": {},
        }


@dataclass
class ToReferralsRewardsFromTreasury:
    discriminator: typing.ClassVar = 4
    kind: typing.ClassVar = "ToReferralsRewardsFromTreasury"

    @classmethod
    def to_json(cls) -> ToReferralsRewardsFromTreasuryJSON:
        return ToReferralsRewardsFromTreasuryJSON(
            kind="ToReferralsRewardsFromTreasury",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ToReferralsRewardsFromTreasury": {},
        }


TreasuryMovementTypeKind = typing.Union[
    Undefined,
    ToTreasuryFromInsurance,
    ToInsuranceFromTreasury,
    ToTreasuryFromReferralsRewards,
    ToReferralsRewardsFromTreasury,
]
TreasuryMovementTypeJSON = typing.Union[
    UndefinedJSON,
    ToTreasuryFromInsuranceJSON,
    ToInsuranceFromTreasuryJSON,
    ToTreasuryFromReferralsRewardsJSON,
    ToReferralsRewardsFromTreasuryJSON,
]


def from_decoded(obj: dict) -> TreasuryMovementTypeKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Undefined" in obj:
        return Undefined()
    if "ToTreasuryFromInsurance" in obj:
        return ToTreasuryFromInsurance()
    if "ToInsuranceFromTreasury" in obj:
        return ToInsuranceFromTreasury()
    if "ToTreasuryFromReferralsRewards" in obj:
        return ToTreasuryFromReferralsRewards()
    if "ToReferralsRewardsFromTreasury" in obj:
        return ToReferralsRewardsFromTreasury()
    raise ValueError("Invalid enum object")


def from_json(obj: TreasuryMovementTypeJSON) -> TreasuryMovementTypeKind:
    if obj["kind"] == "Undefined":
        return Undefined()
    if obj["kind"] == "ToTreasuryFromInsurance":
        return ToTreasuryFromInsurance()
    if obj["kind"] == "ToInsuranceFromTreasury":
        return ToInsuranceFromTreasury()
    if obj["kind"] == "ToTreasuryFromReferralsRewards":
        return ToTreasuryFromReferralsRewards()
    if obj["kind"] == "ToReferralsRewardsFromTreasury":
        return ToReferralsRewardsFromTreasury()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Undefined" / borsh.CStruct(),
    "ToTreasuryFromInsurance" / borsh.CStruct(),
    "ToInsuranceFromTreasury" / borsh.CStruct(),
    "ToTreasuryFromReferralsRewards" / borsh.CStruct(),
    "ToReferralsRewardsFromTreasury" / borsh.CStruct(),
)
