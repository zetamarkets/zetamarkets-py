from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import EnumForCodegen


class InitialJSON(typing.TypedDict):
    kind: typing.Literal["Initial"]


class MaintenanceJSON(typing.TypedDict):
    kind: typing.Literal["Maintenance"]


class MaintenanceIncludingOrdersJSON(typing.TypedDict):
    kind: typing.Literal["MaintenanceIncludingOrders"]


class MarketMakerConcessionJSON(typing.TypedDict):
    kind: typing.Literal["MarketMakerConcession"]


@dataclass
class Initial:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Initial"

    @classmethod
    def to_json(cls) -> InitialJSON:
        return InitialJSON(
            kind="Initial",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Initial": {},
        }


@dataclass
class Maintenance:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Maintenance"

    @classmethod
    def to_json(cls) -> MaintenanceJSON:
        return MaintenanceJSON(
            kind="Maintenance",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Maintenance": {},
        }


@dataclass
class MaintenanceIncludingOrders:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "MaintenanceIncludingOrders"

    @classmethod
    def to_json(cls) -> MaintenanceIncludingOrdersJSON:
        return MaintenanceIncludingOrdersJSON(
            kind="MaintenanceIncludingOrders",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MaintenanceIncludingOrders": {},
        }


@dataclass
class MarketMakerConcession:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "MarketMakerConcession"

    @classmethod
    def to_json(cls) -> MarketMakerConcessionJSON:
        return MarketMakerConcessionJSON(
            kind="MarketMakerConcession",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MarketMakerConcession": {},
        }


MarginRequirementKind = typing.Union[Initial, Maintenance, MaintenanceIncludingOrders, MarketMakerConcession]
MarginRequirementJSON = typing.Union[
    InitialJSON,
    MaintenanceJSON,
    MaintenanceIncludingOrdersJSON,
    MarketMakerConcessionJSON,
]


def from_decoded(obj: dict) -> MarginRequirementKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Initial" in obj:
        return Initial()
    if "Maintenance" in obj:
        return Maintenance()
    if "MaintenanceIncludingOrders" in obj:
        return MaintenanceIncludingOrders()
    if "MarketMakerConcession" in obj:
        return MarketMakerConcession()
    raise ValueError("Invalid enum object")


def from_json(obj: MarginRequirementJSON) -> MarginRequirementKind:
    if obj["kind"] == "Initial":
        return Initial()
    if obj["kind"] == "Maintenance":
        return Maintenance()
    if obj["kind"] == "MaintenanceIncludingOrders":
        return MaintenanceIncludingOrders()
    if obj["kind"] == "MarketMakerConcession":
        return MarketMakerConcession()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Initial" / borsh.CStruct(),
    "Maintenance" / borsh.CStruct(),
    "MaintenanceIncludingOrders" / borsh.CStruct(),
    "MarketMakerConcession" / borsh.CStruct(),
)
