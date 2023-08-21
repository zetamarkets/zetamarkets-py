from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID

from ..program_id import PROGRAM_ID


class InitializeReferrerAccountAccounts(typing.TypedDict):
    referrer: Pubkey
    referrer_account: Pubkey


def initialize_referrer_account(
    accounts: InitializeReferrerAccountAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["referrer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["referrer_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"-\\\xcaDGC3\x04"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
