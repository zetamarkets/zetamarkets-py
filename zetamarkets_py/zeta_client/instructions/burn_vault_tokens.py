from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID

from ..program_id import PROGRAM_ID


class BurnVaultTokensAccounts(typing.TypedDict):
    state: Pubkey
    mint: Pubkey
    vault: Pubkey
    serum_authority: Pubkey


def burn_vault_tokens(
    accounts: BurnVaultTokensAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["serum_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xe9\xcb\xa5\xc9\xaf+\xbc\x9f"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
