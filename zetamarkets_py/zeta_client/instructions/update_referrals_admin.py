from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class UpdateReferralsAdminAccounts(typing.TypedDict):
    state: Pubkey
    admin: Pubkey
    new_admin: Pubkey


def update_referrals_admin(
    accounts: UpdateReferralsAdminAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["new_admin"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"I\x90\\wJj\x10\xc8"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
