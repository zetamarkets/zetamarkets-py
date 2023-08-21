from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class CloseMarginAccountAccounts(typing.TypedDict):
    margin_account: Pubkey
    authority: Pubkey
    zeta_group: Pubkey


def close_margin_account(
    accounts: CloseMarginAccountAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["margin_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"i\xd7)\xef\xa6\xcf\x01g"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
