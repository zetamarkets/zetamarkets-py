from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID

from ..program_id import PROGRAM_ID


class RebalanceInsuranceVaultAccounts(typing.TypedDict):
    state: Pubkey
    zeta_vault: Pubkey
    insurance_vault: Pubkey
    treasury_wallet: Pubkey
    socialized_loss_account: Pubkey


def rebalance_insurance_vault(
    accounts: RebalanceInsuranceVaultAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["insurance_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["treasury_wallet"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["socialized_loss_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x0b\xc4B\xeb;\xed\xdfo"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
