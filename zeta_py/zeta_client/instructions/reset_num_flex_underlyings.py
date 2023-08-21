from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class ResetNumFlexUnderlyingsAccounts(typing.TypedDict):
    state: Pubkey
    admin: Pubkey


def reset_num_flex_underlyings(
    accounts: ResetNumFlexUnderlyingsAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"0\x13\xfe\xd1\xc8\xd31="
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
