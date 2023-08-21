from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class UpdateOracleBackupFeedAccounts(typing.TypedDict):
    state: Pubkey
    zeta_group: Pubkey
    admin: Pubkey
    oracle: Pubkey


def update_oracle_backup_feed(
    accounts: UpdateOracleBackupFeedAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xe6\t!\xca\xe4\xd1\xb4b"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
