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


class ZetaGroupJSON(typing.TypedDict):
    nonce: int
    nonce_padding: list[int]
    front_expiry_index: int
    halt_state: types.halt_state.HaltStateJSON
    underlying_mint: str
    oracle: str
    greeks: str
    pricing_parameters: types.pricing_parameters.PricingParametersJSON
    margin_parameters: types.margin_parameters.MarginParametersJSON
    margin_parameters_padding: list[int]
    products: list[types.product.ProductJSON]
    products_padding: list[types.product.ProductJSON]
    perp: types.product.ProductJSON
    expiry_series: list[types.expiry_series.ExpirySeriesJSON]
    expiry_series_padding: list[types.expiry_series.ExpirySeriesJSON]
    deprecated_padding: list[int]
    asset: types.asset.AssetJSON
    expiry_interval_seconds: int
    new_expiry_threshold_seconds: int
    perp_parameters: types.perp_parameters.PerpParametersJSON
    perp_sync_queue: str
    oracle_backup_feed: str
    perps_only: bool
    flex_underlying: bool
    padding: list[int]


@dataclass
class ZetaGroup:
    discriminator: typing.ClassVar = b"y\x11\xd2km\xeb\x0e\x0c"
    layout: typing.ClassVar = borsh.CStruct(
        "nonce" / borsh.U8,
        "nonce_padding" / borsh.U8[2],
        "front_expiry_index" / borsh.U8,
        "halt_state" / types.halt_state.HaltState.layout,
        "underlying_mint" / BorshPubkey,
        "oracle" / BorshPubkey,
        "greeks" / BorshPubkey,
        "pricing_parameters" / types.pricing_parameters.PricingParameters.layout,
        "margin_parameters" / types.margin_parameters.MarginParameters.layout,
        "margin_parameters_padding" / borsh.U8[104],
        "products" / types.product.Product.layout[46],
        "products_padding" / types.product.Product.layout[91],
        "perp" / types.product.Product.layout,
        "expiry_series" / types.expiry_series.ExpirySeries.layout[2],
        "expiry_series_padding" / types.expiry_series.ExpirySeries.layout[4],
        "deprecated_padding" / borsh.U8[8],
        "asset" / types.asset.layout,
        "expiry_interval_seconds" / borsh.U32,
        "new_expiry_threshold_seconds" / borsh.U32,
        "perp_parameters" / types.perp_parameters.PerpParameters.layout,
        "perp_sync_queue" / BorshPubkey,
        "oracle_backup_feed" / BorshPubkey,
        "perps_only" / borsh.Bool,
        "flex_underlying" / borsh.Bool,
        "padding" / borsh.U8[964],
    )
    nonce: int
    nonce_padding: list[int]
    front_expiry_index: int
    halt_state: types.halt_state.HaltState
    underlying_mint: Pubkey
    oracle: Pubkey
    greeks: Pubkey
    pricing_parameters: types.pricing_parameters.PricingParameters
    margin_parameters: types.margin_parameters.MarginParameters
    margin_parameters_padding: list[int]
    products: list[types.product.Product]
    products_padding: list[types.product.Product]
    perp: types.product.Product
    expiry_series: list[types.expiry_series.ExpirySeries]
    expiry_series_padding: list[types.expiry_series.ExpirySeries]
    deprecated_padding: list[int]
    asset: types.asset.AssetKind
    expiry_interval_seconds: int
    new_expiry_threshold_seconds: int
    perp_parameters: types.perp_parameters.PerpParameters
    perp_sync_queue: Pubkey
    oracle_backup_feed: Pubkey
    perps_only: bool
    flex_underlying: bool
    padding: list[int]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["ZetaGroup"]:
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
    ) -> typing.List[typing.Optional["ZetaGroup"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["ZetaGroup"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "ZetaGroup":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = ZetaGroup.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            nonce=dec.nonce,
            nonce_padding=dec.nonce_padding,
            front_expiry_index=dec.front_expiry_index,
            halt_state=types.halt_state.HaltState.from_decoded(dec.halt_state),
            underlying_mint=dec.underlying_mint,
            oracle=dec.oracle,
            greeks=dec.greeks,
            pricing_parameters=types.pricing_parameters.PricingParameters.from_decoded(dec.pricing_parameters),
            margin_parameters=types.margin_parameters.MarginParameters.from_decoded(dec.margin_parameters),
            margin_parameters_padding=dec.margin_parameters_padding,
            products=list(map(lambda item: types.product.Product.from_decoded(item), dec.products)),
            products_padding=list(
                map(
                    lambda item: types.product.Product.from_decoded(item),
                    dec.products_padding,
                )
            ),
            perp=types.product.Product.from_decoded(dec.perp),
            expiry_series=list(
                map(
                    lambda item: types.expiry_series.ExpirySeries.from_decoded(item),
                    dec.expiry_series,
                )
            ),
            expiry_series_padding=list(
                map(
                    lambda item: types.expiry_series.ExpirySeries.from_decoded(item),
                    dec.expiry_series_padding,
                )
            ),
            deprecated_padding=dec.deprecated_padding,
            asset=types.asset.from_decoded(dec.asset),
            expiry_interval_seconds=dec.expiry_interval_seconds,
            new_expiry_threshold_seconds=dec.new_expiry_threshold_seconds,
            perp_parameters=types.perp_parameters.PerpParameters.from_decoded(dec.perp_parameters),
            perp_sync_queue=dec.perp_sync_queue,
            oracle_backup_feed=dec.oracle_backup_feed,
            perps_only=dec.perps_only,
            flex_underlying=dec.flex_underlying,
            padding=dec.padding,
        )

    def to_json(self) -> ZetaGroupJSON:
        return {
            "nonce": self.nonce,
            "nonce_padding": self.nonce_padding,
            "front_expiry_index": self.front_expiry_index,
            "halt_state": self.halt_state.to_json(),
            "underlying_mint": str(self.underlying_mint),
            "oracle": str(self.oracle),
            "greeks": str(self.greeks),
            "pricing_parameters": self.pricing_parameters.to_json(),
            "margin_parameters": self.margin_parameters.to_json(),
            "margin_parameters_padding": self.margin_parameters_padding,
            "products": list(map(lambda item: item.to_json(), self.products)),
            "products_padding": list(map(lambda item: item.to_json(), self.products_padding)),
            "perp": self.perp.to_json(),
            "expiry_series": list(map(lambda item: item.to_json(), self.expiry_series)),
            "expiry_series_padding": list(map(lambda item: item.to_json(), self.expiry_series_padding)),
            "deprecated_padding": self.deprecated_padding,
            "asset": self.asset.to_json(),
            "expiry_interval_seconds": self.expiry_interval_seconds,
            "new_expiry_threshold_seconds": self.new_expiry_threshold_seconds,
            "perp_parameters": self.perp_parameters.to_json(),
            "perp_sync_queue": str(self.perp_sync_queue),
            "oracle_backup_feed": str(self.oracle_backup_feed),
            "perps_only": self.perps_only,
            "flex_underlying": self.flex_underlying,
            "padding": self.padding,
        }

    @classmethod
    def from_json(cls, obj: ZetaGroupJSON) -> "ZetaGroup":
        return cls(
            nonce=obj["nonce"],
            nonce_padding=obj["nonce_padding"],
            front_expiry_index=obj["front_expiry_index"],
            halt_state=types.halt_state.HaltState.from_json(obj["halt_state"]),
            underlying_mint=Pubkey.from_string(obj["underlying_mint"]),
            oracle=Pubkey.from_string(obj["oracle"]),
            greeks=Pubkey.from_string(obj["greeks"]),
            pricing_parameters=types.pricing_parameters.PricingParameters.from_json(obj["pricing_parameters"]),
            margin_parameters=types.margin_parameters.MarginParameters.from_json(obj["margin_parameters"]),
            margin_parameters_padding=obj["margin_parameters_padding"],
            products=list(map(lambda item: types.product.Product.from_json(item), obj["products"])),
            products_padding=list(
                map(
                    lambda item: types.product.Product.from_json(item),
                    obj["products_padding"],
                )
            ),
            perp=types.product.Product.from_json(obj["perp"]),
            expiry_series=list(
                map(
                    lambda item: types.expiry_series.ExpirySeries.from_json(item),
                    obj["expiry_series"],
                )
            ),
            expiry_series_padding=list(
                map(
                    lambda item: types.expiry_series.ExpirySeries.from_json(item),
                    obj["expiry_series_padding"],
                )
            ),
            deprecated_padding=obj["deprecated_padding"],
            asset=types.asset.from_json(obj["asset"]),
            expiry_interval_seconds=obj["expiry_interval_seconds"],
            new_expiry_threshold_seconds=obj["new_expiry_threshold_seconds"],
            perp_parameters=types.perp_parameters.PerpParameters.from_json(obj["perp_parameters"]),
            perp_sync_queue=Pubkey.from_string(obj["perp_sync_queue"]),
            oracle_backup_feed=Pubkey.from_string(obj["oracle_backup_feed"]),
            perps_only=obj["perps_only"],
            flex_underlying=obj["flex_underlying"],
            padding=obj["padding"],
        )
