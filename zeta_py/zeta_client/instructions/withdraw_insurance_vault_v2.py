from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID

from ..program_id import PROGRAM_ID


class WithdrawInsuranceVaultV2Args(typing.TypedDict):
    percentage_amount: int


layout = borsh.CStruct("percentage_amount" / borsh.U64)


class WithdrawInsuranceVaultV2Accounts(typing.TypedDict):
    state: Pubkey
    pricing: Pubkey
    insurance_vault: Pubkey
    insurance_deposit_account: Pubkey
    user_token_account: Pubkey
    authority: Pubkey


def withdraw_insurance_vault_v2(
    args: WithdrawInsuranceVaultV2Args,
    accounts: WithdrawInsuranceVaultV2Accounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["pricing"], is_signer=False, is_writable=True),
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
    identifier = b"\xcbG,\x94\xe0\xf2E\xa5"
    encoded_args = layout.build(
        {
            "percentage_amount": args["percentage_amount"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
