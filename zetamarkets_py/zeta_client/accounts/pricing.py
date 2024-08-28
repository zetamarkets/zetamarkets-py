import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import BorshPubkey
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class PricingJSON(typing.TypedDict):
    nonce: int
    mark_prices: list[int]
    mark_prices_padding: list[int]
    update_timestamps: list[int]
    update_timestamps_padding: list[int]
    funding_deltas: list[types.anchor_decimal.AnchorDecimalJSON]
    funding_deltas_padding: list[types.anchor_decimal.AnchorDecimalJSON]
    latest_funding_rates: list[types.anchor_decimal.AnchorDecimalJSON]
    latest_funding_rates_padding: list[types.anchor_decimal.AnchorDecimalJSON]
    latest_midpoints: list[int]
    latest_midpoints_padding: list[int]
    oracles: list[str]
    oracles_padding: list[str]
    oracle_backup_feeds: list[str]
    oracle_backup_feeds_padding: list[str]
    markets: list[str]
    markets_padding: list[str]
    perp_sync_queues: list[str]
    perp_sync_queues_padding: list[str]
    perp_parameters: list[types.perp_parameters.PerpParametersJSON]
    perp_parameters_padding: list[types.perp_parameters.PerpParametersJSON]
    margin_parameters: list[types.margin_parameters.MarginParametersJSON]
    margin_parameters_padding: list[types.margin_parameters.MarginParametersJSON]
    products: list[types.product.ProductJSON]
    products_padding: list[types.product.ProductJSON]
    zeta_group_keys: list[str]
    zeta_group_keys_padding: list[str]
    total_insurance_vault_deposits: int
    last_withdraw_timestamp: int
    net_outflow_sum: int
    halt_force_pricing: list[bool]
    halt_force_pricing_padding: list[bool]
    padding: list[int]


@dataclass
class Pricing:
    discriminator: typing.ClassVar = b"\xbe{\xd2\xb6\x8f\x0b\x98\x88"
    layout: typing.ClassVar = borsh.CStruct(
        "nonce" / borsh.U8,
        "mark_prices" / borsh.U64[18],
        "mark_prices_padding" / borsh.U64[7],
        "update_timestamps" / borsh.U64[18],
        "update_timestamps_padding" / borsh.U64[7],
        "funding_deltas" / types.anchor_decimal.AnchorDecimal.layout[18],
        "funding_deltas_padding" / types.anchor_decimal.AnchorDecimal.layout[7],
        "latest_funding_rates" / types.anchor_decimal.AnchorDecimal.layout[18],
        "latest_funding_rates_padding" / types.anchor_decimal.AnchorDecimal.layout[7],
        "latest_midpoints" / borsh.U64[18],
        "latest_midpoints_padding" / borsh.U64[7],
        "oracles" / BorshPubkey[18],
        "oracles_padding" / BorshPubkey[7],
        "oracle_backup_feeds" / BorshPubkey[18],
        "oracle_backup_feeds_padding" / BorshPubkey[7],
        "markets" / BorshPubkey[18],
        "markets_padding" / BorshPubkey[7],
        "perp_sync_queues" / BorshPubkey[18],
        "perp_sync_queues_padding" / BorshPubkey[7],
        "perp_parameters" / types.perp_parameters.PerpParameters.layout[18],
        "perp_parameters_padding" / types.perp_parameters.PerpParameters.layout[7],
        "margin_parameters" / types.margin_parameters.MarginParameters.layout[18],
        "margin_parameters_padding" / types.margin_parameters.MarginParameters.layout[7],
        "products" / types.product.Product.layout[18],
        "products_padding" / types.product.Product.layout[7],
        "zeta_group_keys" / BorshPubkey[18],
        "zeta_group_keys_padding" / BorshPubkey[7],
        "total_insurance_vault_deposits" / borsh.U64,
        "last_withdraw_timestamp" / borsh.U64,
        "net_outflow_sum" / borsh.I64,
        "halt_force_pricing" / borsh.Bool[18],
        "halt_force_pricing_padding" / borsh.Bool[7],
        "padding" / borsh.U8[2707],
    )
    nonce: int
    mark_prices: list[int]
    mark_prices_padding: list[int]
    update_timestamps: list[int]
    update_timestamps_padding: list[int]
    funding_deltas: list[types.anchor_decimal.AnchorDecimal]
    funding_deltas_padding: list[types.anchor_decimal.AnchorDecimal]
    latest_funding_rates: list[types.anchor_decimal.AnchorDecimal]
    latest_funding_rates_padding: list[types.anchor_decimal.AnchorDecimal]
    latest_midpoints: list[int]
    latest_midpoints_padding: list[int]
    oracles: list[Pubkey]
    oracles_padding: list[Pubkey]
    oracle_backup_feeds: list[Pubkey]
    oracle_backup_feeds_padding: list[Pubkey]
    markets: list[Pubkey]
    markets_padding: list[Pubkey]
    perp_sync_queues: list[Pubkey]
    perp_sync_queues_padding: list[Pubkey]
    perp_parameters: list[types.perp_parameters.PerpParameters]
    perp_parameters_padding: list[types.perp_parameters.PerpParameters]
    margin_parameters: list[types.margin_parameters.MarginParameters]
    margin_parameters_padding: list[types.margin_parameters.MarginParameters]
    products: list[types.product.Product]
    products_padding: list[types.product.Product]
    zeta_group_keys: list[Pubkey]
    zeta_group_keys_padding: list[Pubkey]
    total_insurance_vault_deposits: int
    last_withdraw_timestamp: int
    net_outflow_sum: int
    halt_force_pricing: list[bool]
    halt_force_pricing_padding: list[bool]
    padding: list[int]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["Pricing"]:
        resp = await conn.get_account_info(address, commitment=commitment)
        info = resp.value
        if info is None:
            return None
        if info.owner != program_id:
            raise ValueError("Account does not belong to this program")
        bytes_data = info.data
        return cls.decode(bytes_data)

    @classmethod
    async def fetch_multiple(
        cls,
        conn: AsyncClient,
        addresses: list[Pubkey],
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.List[typing.Optional["Pricing"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["Pricing"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "Pricing":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = Pricing.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            nonce=dec.nonce,
            mark_prices=dec.mark_prices,
            mark_prices_padding=dec.mark_prices_padding,
            update_timestamps=dec.update_timestamps,
            update_timestamps_padding=dec.update_timestamps_padding,
            funding_deltas=list(
                map(
                    lambda item: types.anchor_decimal.AnchorDecimal.from_decoded(item),
                    dec.funding_deltas,
                )
            ),
            funding_deltas_padding=list(
                map(
                    lambda item: types.anchor_decimal.AnchorDecimal.from_decoded(item),
                    dec.funding_deltas_padding,
                )
            ),
            latest_funding_rates=list(
                map(
                    lambda item: types.anchor_decimal.AnchorDecimal.from_decoded(item),
                    dec.latest_funding_rates,
                )
            ),
            latest_funding_rates_padding=list(
                map(
                    lambda item: types.anchor_decimal.AnchorDecimal.from_decoded(item),
                    dec.latest_funding_rates_padding,
                )
            ),
            latest_midpoints=dec.latest_midpoints,
            latest_midpoints_padding=dec.latest_midpoints_padding,
            oracles=dec.oracles,
            oracles_padding=dec.oracles_padding,
            oracle_backup_feeds=dec.oracle_backup_feeds,
            oracle_backup_feeds_padding=dec.oracle_backup_feeds_padding,
            markets=dec.markets,
            markets_padding=dec.markets_padding,
            perp_sync_queues=dec.perp_sync_queues,
            perp_sync_queues_padding=dec.perp_sync_queues_padding,
            perp_parameters=list(
                map(
                    lambda item: types.perp_parameters.PerpParameters.from_decoded(item),
                    dec.perp_parameters,
                )
            ),
            perp_parameters_padding=list(
                map(
                    lambda item: types.perp_parameters.PerpParameters.from_decoded(item),
                    dec.perp_parameters_padding,
                )
            ),
            margin_parameters=list(
                map(
                    lambda item: types.margin_parameters.MarginParameters.from_decoded(item),
                    dec.margin_parameters,
                )
            ),
            margin_parameters_padding=list(
                map(
                    lambda item: types.margin_parameters.MarginParameters.from_decoded(item),
                    dec.margin_parameters_padding,
                )
            ),
            products=list(map(lambda item: types.product.Product.from_decoded(item), dec.products)),
            products_padding=list(
                map(
                    lambda item: types.product.Product.from_decoded(item),
                    dec.products_padding,
                )
            ),
            zeta_group_keys=dec.zeta_group_keys,
            zeta_group_keys_padding=dec.zeta_group_keys_padding,
            total_insurance_vault_deposits=dec.total_insurance_vault_deposits,
            last_withdraw_timestamp=dec.last_withdraw_timestamp,
            net_outflow_sum=dec.net_outflow_sum,
            halt_force_pricing=dec.halt_force_pricing,
            halt_force_pricing_padding=dec.halt_force_pricing_padding,
            padding=dec.padding,
        )

    def to_json(self) -> PricingJSON:
        return {
            "nonce": self.nonce,
            "mark_prices": self.mark_prices,
            "mark_prices_padding": self.mark_prices_padding,
            "update_timestamps": self.update_timestamps,
            "update_timestamps_padding": self.update_timestamps_padding,
            "funding_deltas": list(map(lambda item: item.to_json(), self.funding_deltas)),
            "funding_deltas_padding": list(map(lambda item: item.to_json(), self.funding_deltas_padding)),
            "latest_funding_rates": list(map(lambda item: item.to_json(), self.latest_funding_rates)),
            "latest_funding_rates_padding": list(map(lambda item: item.to_json(), self.latest_funding_rates_padding)),
            "latest_midpoints": self.latest_midpoints,
            "latest_midpoints_padding": self.latest_midpoints_padding,
            "oracles": list(map(lambda item: str(item), self.oracles)),
            "oracles_padding": list(map(lambda item: str(item), self.oracles_padding)),
            "oracle_backup_feeds": list(map(lambda item: str(item), self.oracle_backup_feeds)),
            "oracle_backup_feeds_padding": list(map(lambda item: str(item), self.oracle_backup_feeds_padding)),
            "markets": list(map(lambda item: str(item), self.markets)),
            "markets_padding": list(map(lambda item: str(item), self.markets_padding)),
            "perp_sync_queues": list(map(lambda item: str(item), self.perp_sync_queues)),
            "perp_sync_queues_padding": list(map(lambda item: str(item), self.perp_sync_queues_padding)),
            "perp_parameters": list(map(lambda item: item.to_json(), self.perp_parameters)),
            "perp_parameters_padding": list(map(lambda item: item.to_json(), self.perp_parameters_padding)),
            "margin_parameters": list(map(lambda item: item.to_json(), self.margin_parameters)),
            "margin_parameters_padding": list(map(lambda item: item.to_json(), self.margin_parameters_padding)),
            "products": list(map(lambda item: item.to_json(), self.products)),
            "products_padding": list(map(lambda item: item.to_json(), self.products_padding)),
            "zeta_group_keys": list(map(lambda item: str(item), self.zeta_group_keys)),
            "zeta_group_keys_padding": list(map(lambda item: str(item), self.zeta_group_keys_padding)),
            "total_insurance_vault_deposits": self.total_insurance_vault_deposits,
            "last_withdraw_timestamp": self.last_withdraw_timestamp,
            "net_outflow_sum": self.net_outflow_sum,
            "halt_force_pricing": self.halt_force_pricing,
            "halt_force_pricing_padding": self.halt_force_pricing_padding,
            "padding": self.padding,
        }

    @classmethod
    def from_json(cls, obj: PricingJSON) -> "Pricing":
        return cls(
            nonce=obj["nonce"],
            mark_prices=obj["mark_prices"],
            mark_prices_padding=obj["mark_prices_padding"],
            update_timestamps=obj["update_timestamps"],
            update_timestamps_padding=obj["update_timestamps_padding"],
            funding_deltas=list(
                map(
                    lambda item: types.anchor_decimal.AnchorDecimal.from_json(item),
                    obj["funding_deltas"],
                )
            ),
            funding_deltas_padding=list(
                map(
                    lambda item: types.anchor_decimal.AnchorDecimal.from_json(item),
                    obj["funding_deltas_padding"],
                )
            ),
            latest_funding_rates=list(
                map(
                    lambda item: types.anchor_decimal.AnchorDecimal.from_json(item),
                    obj["latest_funding_rates"],
                )
            ),
            latest_funding_rates_padding=list(
                map(
                    lambda item: types.anchor_decimal.AnchorDecimal.from_json(item),
                    obj["latest_funding_rates_padding"],
                )
            ),
            latest_midpoints=obj["latest_midpoints"],
            latest_midpoints_padding=obj["latest_midpoints_padding"],
            oracles=list(map(lambda item: Pubkey.from_string(item), obj["oracles"])),
            oracles_padding=list(map(lambda item: Pubkey.from_string(item), obj["oracles_padding"])),
            oracle_backup_feeds=list(map(lambda item: Pubkey.from_string(item), obj["oracle_backup_feeds"])),
            oracle_backup_feeds_padding=list(
                map(
                    lambda item: Pubkey.from_string(item),
                    obj["oracle_backup_feeds_padding"],
                )
            ),
            markets=list(map(lambda item: Pubkey.from_string(item), obj["markets"])),
            markets_padding=list(map(lambda item: Pubkey.from_string(item), obj["markets_padding"])),
            perp_sync_queues=list(map(lambda item: Pubkey.from_string(item), obj["perp_sync_queues"])),
            perp_sync_queues_padding=list(
                map(
                    lambda item: Pubkey.from_string(item),
                    obj["perp_sync_queues_padding"],
                )
            ),
            perp_parameters=list(
                map(
                    lambda item: types.perp_parameters.PerpParameters.from_json(item),
                    obj["perp_parameters"],
                )
            ),
            perp_parameters_padding=list(
                map(
                    lambda item: types.perp_parameters.PerpParameters.from_json(item),
                    obj["perp_parameters_padding"],
                )
            ),
            margin_parameters=list(
                map(
                    lambda item: types.margin_parameters.MarginParameters.from_json(item),
                    obj["margin_parameters"],
                )
            ),
            margin_parameters_padding=list(
                map(
                    lambda item: types.margin_parameters.MarginParameters.from_json(item),
                    obj["margin_parameters_padding"],
                )
            ),
            products=list(map(lambda item: types.product.Product.from_json(item), obj["products"])),
            products_padding=list(
                map(
                    lambda item: types.product.Product.from_json(item),
                    obj["products_padding"],
                )
            ),
            zeta_group_keys=list(map(lambda item: Pubkey.from_string(item), obj["zeta_group_keys"])),
            zeta_group_keys_padding=list(
                map(
                    lambda item: Pubkey.from_string(item),
                    obj["zeta_group_keys_padding"],
                )
            ),
            total_insurance_vault_deposits=obj["total_insurance_vault_deposits"],
            last_withdraw_timestamp=obj["last_withdraw_timestamp"],
            net_outflow_sum=obj["net_outflow_sum"],
            halt_force_pricing=obj["halt_force_pricing"],
            halt_force_pricing_padding=obj["halt_force_pricing_padding"],
            padding=obj["padding"],
        )
