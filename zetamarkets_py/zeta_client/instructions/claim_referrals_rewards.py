from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID

from ..program_id import PROGRAM_ID


class ClaimReferralsRewardsAccounts(typing.TypedDict):
    state: Pubkey
    referrals_rewards_wallet: Pubkey
    user_referrals_account: Pubkey
    user_token_account: Pubkey
    user: Pubkey


def claim_referrals_rewards(
    accounts: ClaimReferralsRewardsAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["referrals_rewards_wallet"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["user_referrals_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["user_token_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["user"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"y\x9cm\x9f\x9e\xdb\xd9\x8f"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
