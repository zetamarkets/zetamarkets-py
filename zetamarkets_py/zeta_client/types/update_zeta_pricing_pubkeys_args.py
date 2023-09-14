from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import BorshPubkey
from construct import Container
from solders.pubkey import Pubkey

from . import asset


class UpdateZetaPricingPubkeysArgsJSON(typing.TypedDict):
    asset: asset.AssetJSON
    oracle: str
    oracle_backup_feed: str
    market: str
    perp_sync_queue: str
    zeta_group_key: str


@dataclass
class UpdateZetaPricingPubkeysArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "asset" / asset.layout,
        "oracle" / BorshPubkey,
        "oracle_backup_feed" / BorshPubkey,
        "market" / BorshPubkey,
        "perp_sync_queue" / BorshPubkey,
        "zeta_group_key" / BorshPubkey,
    )
    asset: asset.AssetKind
    oracle: Pubkey
    oracle_backup_feed: Pubkey
    market: Pubkey
    perp_sync_queue: Pubkey
    zeta_group_key: Pubkey

    @classmethod
    def from_decoded(cls, obj: Container) -> "UpdateZetaPricingPubkeysArgs":
        return cls(
            asset=asset.from_decoded(obj.asset),
            oracle=obj.oracle,
            oracle_backup_feed=obj.oracle_backup_feed,
            market=obj.market,
            perp_sync_queue=obj.perp_sync_queue,
            zeta_group_key=obj.zeta_group_key,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "asset": self.asset.to_encodable(),
            "oracle": self.oracle,
            "oracle_backup_feed": self.oracle_backup_feed,
            "market": self.market,
            "perp_sync_queue": self.perp_sync_queue,
            "zeta_group_key": self.zeta_group_key,
        }

    def to_json(self) -> UpdateZetaPricingPubkeysArgsJSON:
        return {
            "asset": self.asset.to_json(),
            "oracle": str(self.oracle),
            "oracle_backup_feed": str(self.oracle_backup_feed),
            "market": str(self.market),
            "perp_sync_queue": str(self.perp_sync_queue),
            "zeta_group_key": str(self.zeta_group_key),
        }

    @classmethod
    def from_json(cls, obj: UpdateZetaPricingPubkeysArgsJSON) -> "UpdateZetaPricingPubkeysArgs":
        return cls(
            asset=asset.from_json(obj["asset"]),
            oracle=Pubkey.from_string(obj["oracle"]),
            oracle_backup_feed=Pubkey.from_string(obj["oracle_backup_feed"]),
            market=Pubkey.from_string(obj["market"]),
            perp_sync_queue=Pubkey.from_string(obj["perp_sync_queue"]),
            zeta_group_key=Pubkey.from_string(obj["zeta_group_key"]),
        )
