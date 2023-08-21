from __future__ import annotations

import typing

import borsh_construct as borsh
from construct import Construct
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class SetReferralsRewardsArgs(typing.TypedDict):
    args: list[types.set_referrals_rewards_args.SetReferralsRewardsArgs]


layout = borsh.CStruct(
    "args" / borsh.Vec(typing.cast(Construct, types.set_referrals_rewards_args.SetReferralsRewardsArgs.layout))
)


class SetReferralsRewardsAccounts(typing.TypedDict):
    state: Pubkey
    referrals_admin: Pubkey


def set_referrals_rewards(
    args: SetReferralsRewardsArgs,
    accounts: SetReferralsRewardsAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["referrals_admin"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b">\xe8\x01\x12K\x07M\x9e"
    encoded_args = layout.build(
        {
            "args": list(map(lambda item: item.to_encodable(), args["args"])),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
