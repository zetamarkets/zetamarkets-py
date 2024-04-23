from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class UpdateMaTypeAdminAccounts(typing.TypedDict):
    state: Pubkey
    admin: Pubkey
    new_admin: Pubkey


def update_ma_type_admin(
    accounts: UpdateMaTypeAdminAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["new_admin"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b",\xb9\x96fp\x1c\x81\xef"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
