from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class CleanZetaMarketsAccounts(typing.TypedDict):
    state: Pubkey
    zeta_group: Pubkey


def clean_zeta_markets(
    accounts: CleanZetaMarketsAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"z\x7f1YD\xe4U\x9d"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
