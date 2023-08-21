from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class TransferExcessSpreadBalanceAccounts(typing.TypedDict):
    zeta_group: Pubkey
    margin_account: Pubkey
    spread_account: Pubkey
    authority: Pubkey


def transfer_excess_spread_balance(
    accounts: TransferExcessSpreadBalanceAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["margin_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["spread_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xac\xb8\x0c\n4i@\xd5"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
