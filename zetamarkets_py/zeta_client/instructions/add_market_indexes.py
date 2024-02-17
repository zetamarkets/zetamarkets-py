from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class AddMarketIndexesAccounts(typing.TypedDict):
    market_indexes: Pubkey
    zeta_group: Pubkey


def add_market_indexes(
    accounts: AddMarketIndexesAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["market_indexes"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"^\xf6\x90\xaf\x04\xa4\xe9\xfc"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
