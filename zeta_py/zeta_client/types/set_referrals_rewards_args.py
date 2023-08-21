from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import BorshPubkey
from construct import Container
from solders.pubkey import Pubkey


class SetReferralsRewardsArgsJSON(typing.TypedDict):
    referrals_account_key: str
    pending_rewards: int
    overwrite: bool


@dataclass
class SetReferralsRewardsArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "referrals_account_key" / BorshPubkey,
        "pending_rewards" / borsh.U64,
        "overwrite" / borsh.Bool,
    )
    referrals_account_key: Pubkey
    pending_rewards: int
    overwrite: bool

    @classmethod
    def from_decoded(cls, obj: Container) -> "SetReferralsRewardsArgs":
        return cls(
            referrals_account_key=obj.referrals_account_key,
            pending_rewards=obj.pending_rewards,
            overwrite=obj.overwrite,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "referrals_account_key": self.referrals_account_key,
            "pending_rewards": self.pending_rewards,
            "overwrite": self.overwrite,
        }

    def to_json(self) -> SetReferralsRewardsArgsJSON:
        return {
            "referrals_account_key": str(self.referrals_account_key),
            "pending_rewards": self.pending_rewards,
            "overwrite": self.overwrite,
        }

    @classmethod
    def from_json(cls, obj: SetReferralsRewardsArgsJSON) -> "SetReferralsRewardsArgs":
        return cls(
            referrals_account_key=Pubkey.from_string(obj["referrals_account_key"]),
            pending_rewards=obj["pending_rewards"],
            overwrite=obj["overwrite"],
        )
