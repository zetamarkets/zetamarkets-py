from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class CloseReferrerAccountsAccounts(typing.TypedDict):
    referrer_id_account: Pubkey
    referrer_pubkey_account: Pubkey
    authority: Pubkey


def close_referrer_accounts(
    accounts: CloseReferrerAccountsAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["referrer_id_account"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["referrer_pubkey_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xe0N7\x8b\xcb\xec>N"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
