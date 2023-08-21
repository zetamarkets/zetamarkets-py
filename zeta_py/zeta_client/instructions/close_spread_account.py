from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class CloseSpreadAccountAccounts(typing.TypedDict):
    spread_account: Pubkey
    authority: Pubkey
    zeta_group: Pubkey


def close_spread_account(
    accounts: CloseSpreadAccountAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["spread_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xbe\xe4\xfd\x10\xc9\x94\xa1\xf0"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
