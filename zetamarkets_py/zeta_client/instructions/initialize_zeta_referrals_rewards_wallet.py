from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.sysvar import RENT
from spl.token.constants import TOKEN_PROGRAM_ID

from ..program_id import PROGRAM_ID


class InitializeZetaReferralsRewardsWalletAccounts(typing.TypedDict):
    state: Pubkey
    referrals_rewards_wallet: Pubkey
    usdc_mint: Pubkey
    admin: Pubkey


def initialize_zeta_referrals_rewards_wallet(
    accounts: InitializeZetaReferralsRewardsWalletAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["referrals_rewards_wallet"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["usdc_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xf5\xe5\xdfx\x07\x86\xf7\xf8"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
