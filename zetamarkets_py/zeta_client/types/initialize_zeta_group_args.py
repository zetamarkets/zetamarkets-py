from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container

from . import asset


class InitializeZetaGroupArgsJSON(typing.TypedDict):
    perps_only: bool
    flex_underlying: bool
    asset_override: typing.Optional[asset.AssetJSON]
    zeta_group_nonce: int
    underlying_nonce: int
    greeks_nonce: int
    vault_nonce: int
    insurance_vault_nonce: int
    socialized_loss_account_nonce: int
    perp_sync_queue_nonce: int
    interest_rate: int
    volatility: list[int]
    option_trade_normalizer: int
    future_trade_normalizer: int
    max_volatility_retreat: int
    max_interest_retreat: int
    max_delta: int
    min_delta: int
    min_interest_rate: int
    max_interest_rate: int
    min_volatility: int
    max_volatility: int
    future_margin_initial: int
    future_margin_maintenance: int
    expiry_interval_seconds: int
    new_expiry_threshold_seconds: int
    min_funding_rate_percent: int
    max_funding_rate_percent: int
    perp_impact_cash_delta: int


@dataclass
class InitializeZetaGroupArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "perps_only" / borsh.Bool,
        "flex_underlying" / borsh.Bool,
        "asset_override" / borsh.Option(asset.layout),
        "zeta_group_nonce" / borsh.U8,
        "underlying_nonce" / borsh.U8,
        "greeks_nonce" / borsh.U8,
        "vault_nonce" / borsh.U8,
        "insurance_vault_nonce" / borsh.U8,
        "socialized_loss_account_nonce" / borsh.U8,
        "perp_sync_queue_nonce" / borsh.U8,
        "interest_rate" / borsh.I64,
        "volatility" / borsh.U64[5],
        "option_trade_normalizer" / borsh.U64,
        "future_trade_normalizer" / borsh.U64,
        "max_volatility_retreat" / borsh.U64,
        "max_interest_retreat" / borsh.U64,
        "max_delta" / borsh.U64,
        "min_delta" / borsh.U64,
        "min_interest_rate" / borsh.I64,
        "max_interest_rate" / borsh.I64,
        "min_volatility" / borsh.U64,
        "max_volatility" / borsh.U64,
        "future_margin_initial" / borsh.U64,
        "future_margin_maintenance" / borsh.U64,
        "expiry_interval_seconds" / borsh.U32,
        "new_expiry_threshold_seconds" / borsh.U32,
        "min_funding_rate_percent" / borsh.I64,
        "max_funding_rate_percent" / borsh.I64,
        "perp_impact_cash_delta" / borsh.U64,
    )
    perps_only: bool
    flex_underlying: bool
    asset_override: typing.Optional[asset.AssetKind]
    zeta_group_nonce: int
    underlying_nonce: int
    greeks_nonce: int
    vault_nonce: int
    insurance_vault_nonce: int
    socialized_loss_account_nonce: int
    perp_sync_queue_nonce: int
    interest_rate: int
    volatility: list[int]
    option_trade_normalizer: int
    future_trade_normalizer: int
    max_volatility_retreat: int
    max_interest_retreat: int
    max_delta: int
    min_delta: int
    min_interest_rate: int
    max_interest_rate: int
    min_volatility: int
    max_volatility: int
    future_margin_initial: int
    future_margin_maintenance: int
    expiry_interval_seconds: int
    new_expiry_threshold_seconds: int
    min_funding_rate_percent: int
    max_funding_rate_percent: int
    perp_impact_cash_delta: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "InitializeZetaGroupArgs":
        return cls(
            perps_only=obj.perps_only,
            flex_underlying=obj.flex_underlying,
            asset_override=(None if obj.asset_override is None else asset.from_decoded(obj.asset_override)),
            zeta_group_nonce=obj.zeta_group_nonce,
            underlying_nonce=obj.underlying_nonce,
            greeks_nonce=obj.greeks_nonce,
            vault_nonce=obj.vault_nonce,
            insurance_vault_nonce=obj.insurance_vault_nonce,
            socialized_loss_account_nonce=obj.socialized_loss_account_nonce,
            perp_sync_queue_nonce=obj.perp_sync_queue_nonce,
            interest_rate=obj.interest_rate,
            volatility=obj.volatility,
            option_trade_normalizer=obj.option_trade_normalizer,
            future_trade_normalizer=obj.future_trade_normalizer,
            max_volatility_retreat=obj.max_volatility_retreat,
            max_interest_retreat=obj.max_interest_retreat,
            max_delta=obj.max_delta,
            min_delta=obj.min_delta,
            min_interest_rate=obj.min_interest_rate,
            max_interest_rate=obj.max_interest_rate,
            min_volatility=obj.min_volatility,
            max_volatility=obj.max_volatility,
            future_margin_initial=obj.future_margin_initial,
            future_margin_maintenance=obj.future_margin_maintenance,
            expiry_interval_seconds=obj.expiry_interval_seconds,
            new_expiry_threshold_seconds=obj.new_expiry_threshold_seconds,
            min_funding_rate_percent=obj.min_funding_rate_percent,
            max_funding_rate_percent=obj.max_funding_rate_percent,
            perp_impact_cash_delta=obj.perp_impact_cash_delta,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "perps_only": self.perps_only,
            "flex_underlying": self.flex_underlying,
            "asset_override": (None if self.asset_override is None else self.asset_override.to_encodable()),
            "zeta_group_nonce": self.zeta_group_nonce,
            "underlying_nonce": self.underlying_nonce,
            "greeks_nonce": self.greeks_nonce,
            "vault_nonce": self.vault_nonce,
            "insurance_vault_nonce": self.insurance_vault_nonce,
            "socialized_loss_account_nonce": self.socialized_loss_account_nonce,
            "perp_sync_queue_nonce": self.perp_sync_queue_nonce,
            "interest_rate": self.interest_rate,
            "volatility": self.volatility,
            "option_trade_normalizer": self.option_trade_normalizer,
            "future_trade_normalizer": self.future_trade_normalizer,
            "max_volatility_retreat": self.max_volatility_retreat,
            "max_interest_retreat": self.max_interest_retreat,
            "max_delta": self.max_delta,
            "min_delta": self.min_delta,
            "min_interest_rate": self.min_interest_rate,
            "max_interest_rate": self.max_interest_rate,
            "min_volatility": self.min_volatility,
            "max_volatility": self.max_volatility,
            "future_margin_initial": self.future_margin_initial,
            "future_margin_maintenance": self.future_margin_maintenance,
            "expiry_interval_seconds": self.expiry_interval_seconds,
            "new_expiry_threshold_seconds": self.new_expiry_threshold_seconds,
            "min_funding_rate_percent": self.min_funding_rate_percent,
            "max_funding_rate_percent": self.max_funding_rate_percent,
            "perp_impact_cash_delta": self.perp_impact_cash_delta,
        }

    def to_json(self) -> InitializeZetaGroupArgsJSON:
        return {
            "perps_only": self.perps_only,
            "flex_underlying": self.flex_underlying,
            "asset_override": (None if self.asset_override is None else self.asset_override.to_json()),
            "zeta_group_nonce": self.zeta_group_nonce,
            "underlying_nonce": self.underlying_nonce,
            "greeks_nonce": self.greeks_nonce,
            "vault_nonce": self.vault_nonce,
            "insurance_vault_nonce": self.insurance_vault_nonce,
            "socialized_loss_account_nonce": self.socialized_loss_account_nonce,
            "perp_sync_queue_nonce": self.perp_sync_queue_nonce,
            "interest_rate": self.interest_rate,
            "volatility": self.volatility,
            "option_trade_normalizer": self.option_trade_normalizer,
            "future_trade_normalizer": self.future_trade_normalizer,
            "max_volatility_retreat": self.max_volatility_retreat,
            "max_interest_retreat": self.max_interest_retreat,
            "max_delta": self.max_delta,
            "min_delta": self.min_delta,
            "min_interest_rate": self.min_interest_rate,
            "max_interest_rate": self.max_interest_rate,
            "min_volatility": self.min_volatility,
            "max_volatility": self.max_volatility,
            "future_margin_initial": self.future_margin_initial,
            "future_margin_maintenance": self.future_margin_maintenance,
            "expiry_interval_seconds": self.expiry_interval_seconds,
            "new_expiry_threshold_seconds": self.new_expiry_threshold_seconds,
            "min_funding_rate_percent": self.min_funding_rate_percent,
            "max_funding_rate_percent": self.max_funding_rate_percent,
            "perp_impact_cash_delta": self.perp_impact_cash_delta,
        }

    @classmethod
    def from_json(cls, obj: InitializeZetaGroupArgsJSON) -> "InitializeZetaGroupArgs":
        return cls(
            perps_only=obj["perps_only"],
            flex_underlying=obj["flex_underlying"],
            asset_override=(None if obj["asset_override"] is None else asset.from_json(obj["asset_override"])),
            zeta_group_nonce=obj["zeta_group_nonce"],
            underlying_nonce=obj["underlying_nonce"],
            greeks_nonce=obj["greeks_nonce"],
            vault_nonce=obj["vault_nonce"],
            insurance_vault_nonce=obj["insurance_vault_nonce"],
            socialized_loss_account_nonce=obj["socialized_loss_account_nonce"],
            perp_sync_queue_nonce=obj["perp_sync_queue_nonce"],
            interest_rate=obj["interest_rate"],
            volatility=obj["volatility"],
            option_trade_normalizer=obj["option_trade_normalizer"],
            future_trade_normalizer=obj["future_trade_normalizer"],
            max_volatility_retreat=obj["max_volatility_retreat"],
            max_interest_retreat=obj["max_interest_retreat"],
            max_delta=obj["max_delta"],
            min_delta=obj["min_delta"],
            min_interest_rate=obj["min_interest_rate"],
            max_interest_rate=obj["max_interest_rate"],
            min_volatility=obj["min_volatility"],
            max_volatility=obj["max_volatility"],
            future_margin_initial=obj["future_margin_initial"],
            future_margin_maintenance=obj["future_margin_maintenance"],
            expiry_interval_seconds=obj["expiry_interval_seconds"],
            new_expiry_threshold_seconds=obj["new_expiry_threshold_seconds"],
            min_funding_rate_percent=obj["min_funding_rate_percent"],
            max_funding_rate_percent=obj["max_funding_rate_percent"],
            perp_impact_cash_delta=obj["perp_impact_cash_delta"],
        )
