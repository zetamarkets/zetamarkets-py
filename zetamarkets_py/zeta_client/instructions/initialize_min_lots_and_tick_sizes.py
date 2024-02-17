from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class InitializeMinLotsAndTickSizesAccounts(typing.TypedDict):
    state: Pubkey
    admin: Pubkey


def initialize_min_lots_and_tick_sizes(
    accounts: InitializeMinLotsAndTickSizesAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"D\x193+~\xabPW"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
