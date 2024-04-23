from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class UpdateStateArgsJSON(typing.TypedDict):
    strike_initialization_threshold_seconds: int
    pricing_frequency_seconds: int
    liquidator_liquidation_percentage: int
    insurance_vault_liquidation_percentage: int
    native_deposit_limit: int
    expiration_threshold_seconds: int
    position_movement_fee_bps: int
    margin_concession_percentage: int
    max_perp_delta_age_seconds: int
    native_withdraw_limit: int
    withdraw_limit_epoch_seconds: int
    native_open_interest_limit: int


@dataclass
class UpdateStateArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "strike_initialization_threshold_seconds" / borsh.U32,
        "pricing_frequency_seconds" / borsh.U32,
        "liquidator_liquidation_percentage" / borsh.U32,
        "insurance_vault_liquidation_percentage" / borsh.U32,
        "native_deposit_limit" / borsh.U64,
        "expiration_threshold_seconds" / borsh.U32,
        "position_movement_fee_bps" / borsh.U8,
        "margin_concession_percentage" / borsh.U8,
        "max_perp_delta_age_seconds" / borsh.U16,
        "native_withdraw_limit" / borsh.U64,
        "withdraw_limit_epoch_seconds" / borsh.U32,
        "native_open_interest_limit" / borsh.U64,
    )
    strike_initialization_threshold_seconds: int
    pricing_frequency_seconds: int
    liquidator_liquidation_percentage: int
    insurance_vault_liquidation_percentage: int
    native_deposit_limit: int
    expiration_threshold_seconds: int
    position_movement_fee_bps: int
    margin_concession_percentage: int
    max_perp_delta_age_seconds: int
    native_withdraw_limit: int
    withdraw_limit_epoch_seconds: int
    native_open_interest_limit: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "UpdateStateArgs":
        return cls(
            strike_initialization_threshold_seconds=obj.strike_initialization_threshold_seconds,
            pricing_frequency_seconds=obj.pricing_frequency_seconds,
            liquidator_liquidation_percentage=obj.liquidator_liquidation_percentage,
            insurance_vault_liquidation_percentage=obj.insurance_vault_liquidation_percentage,
            native_deposit_limit=obj.native_deposit_limit,
            expiration_threshold_seconds=obj.expiration_threshold_seconds,
            position_movement_fee_bps=obj.position_movement_fee_bps,
            margin_concession_percentage=obj.margin_concession_percentage,
            max_perp_delta_age_seconds=obj.max_perp_delta_age_seconds,
            native_withdraw_limit=obj.native_withdraw_limit,
            withdraw_limit_epoch_seconds=obj.withdraw_limit_epoch_seconds,
            native_open_interest_limit=obj.native_open_interest_limit,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "strike_initialization_threshold_seconds": self.strike_initialization_threshold_seconds,
            "pricing_frequency_seconds": self.pricing_frequency_seconds,
            "liquidator_liquidation_percentage": self.liquidator_liquidation_percentage,
            "insurance_vault_liquidation_percentage": self.insurance_vault_liquidation_percentage,
            "native_deposit_limit": self.native_deposit_limit,
            "expiration_threshold_seconds": self.expiration_threshold_seconds,
            "position_movement_fee_bps": self.position_movement_fee_bps,
            "margin_concession_percentage": self.margin_concession_percentage,
            "max_perp_delta_age_seconds": self.max_perp_delta_age_seconds,
            "native_withdraw_limit": self.native_withdraw_limit,
            "withdraw_limit_epoch_seconds": self.withdraw_limit_epoch_seconds,
            "native_open_interest_limit": self.native_open_interest_limit,
        }

    def to_json(self) -> UpdateStateArgsJSON:
        return {
            "strike_initialization_threshold_seconds": self.strike_initialization_threshold_seconds,
            "pricing_frequency_seconds": self.pricing_frequency_seconds,
            "liquidator_liquidation_percentage": self.liquidator_liquidation_percentage,
            "insurance_vault_liquidation_percentage": self.insurance_vault_liquidation_percentage,
            "native_deposit_limit": self.native_deposit_limit,
            "expiration_threshold_seconds": self.expiration_threshold_seconds,
            "position_movement_fee_bps": self.position_movement_fee_bps,
            "margin_concession_percentage": self.margin_concession_percentage,
            "max_perp_delta_age_seconds": self.max_perp_delta_age_seconds,
            "native_withdraw_limit": self.native_withdraw_limit,
            "withdraw_limit_epoch_seconds": self.withdraw_limit_epoch_seconds,
            "native_open_interest_limit": self.native_open_interest_limit,
        }

    @classmethod
    def from_json(cls, obj: UpdateStateArgsJSON) -> "UpdateStateArgs":
        return cls(
            strike_initialization_threshold_seconds=obj["strike_initialization_threshold_seconds"],
            pricing_frequency_seconds=obj["pricing_frequency_seconds"],
            liquidator_liquidation_percentage=obj["liquidator_liquidation_percentage"],
            insurance_vault_liquidation_percentage=obj["insurance_vault_liquidation_percentage"],
            native_deposit_limit=obj["native_deposit_limit"],
            expiration_threshold_seconds=obj["expiration_threshold_seconds"],
            position_movement_fee_bps=obj["position_movement_fee_bps"],
            margin_concession_percentage=obj["margin_concession_percentage"],
            max_perp_delta_age_seconds=obj["max_perp_delta_age_seconds"],
            native_withdraw_limit=obj["native_withdraw_limit"],
            withdraw_limit_epoch_seconds=obj["withdraw_limit_epoch_seconds"],
            native_open_interest_limit=obj["native_open_interest_limit"],
        )
