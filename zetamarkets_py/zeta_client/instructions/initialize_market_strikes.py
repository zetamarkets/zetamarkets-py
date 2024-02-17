from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class InitializeMarketStrikesAccounts(typing.TypedDict):
    state: Pubkey
    zeta_group: Pubkey
    oracle: Pubkey
    oracle_backup_feed: Pubkey
    oracle_backup_program: Pubkey


def initialize_market_strikes(
    accounts: InitializeMarketStrikesAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle_backup_feed"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle_backup_program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xbd.\xff!~\x85+\xab"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
