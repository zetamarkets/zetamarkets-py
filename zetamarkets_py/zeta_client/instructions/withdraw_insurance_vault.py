from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID

from ..program_id import PROGRAM_ID


class WithdrawInsuranceVaultArgs(typing.TypedDict):
    percentage_amount: int


layout = borsh.CStruct("percentage_amount" / borsh.U64)


class WithdrawInsuranceVaultAccounts(typing.TypedDict):
    state: Pubkey
    insurance_vault: Pubkey
    insurance_deposit_account: Pubkey
    user_token_account: Pubkey
    authority: Pubkey


def withdraw_insurance_vault(
    args: WithdrawInsuranceVaultArgs,
    accounts: WithdrawInsuranceVaultAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["insurance_vault"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["insurance_deposit_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["user_token_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x11\xfa\xd5-\xacuQ\xe1"
    encoded_args = layout.build(
        {
            "percentage_amount": args["percentage_amount"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
