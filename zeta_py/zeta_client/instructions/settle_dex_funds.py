from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID

from ..program_id import PROGRAM_ID


class SettleDexFundsAccounts(typing.TypedDict):
    state: Pubkey
    market: Pubkey
    zeta_base_vault: Pubkey
    zeta_quote_vault: Pubkey
    dex_base_vault: Pubkey
    dex_quote_vault: Pubkey
    vault_owner: Pubkey
    mint_authority: Pubkey
    serum_authority: Pubkey
    dex_program: Pubkey


def settle_dex_funds(
    accounts: SettleDexFundsAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["zeta_base_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["zeta_quote_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["dex_base_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["dex_quote_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["vault_owner"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["mint_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["serum_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["dex_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xa5g\x8e&\xd3\xa6\x0e\xe2"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
