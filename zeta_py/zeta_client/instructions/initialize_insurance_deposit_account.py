from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID

from ..program_id import PROGRAM_ID


class InitializeInsuranceDepositAccountArgs(typing.TypedDict):
    nonce: int


layout = borsh.CStruct("nonce" / borsh.U8)


class InitializeInsuranceDepositAccountAccounts(typing.TypedDict):
    insurance_deposit_account: Pubkey
    authority: Pubkey
    payer: Pubkey
    whitelist_insurance_account: Pubkey


def initialize_insurance_deposit_account(
    args: InitializeInsuranceDepositAccountArgs,
    accounts: InitializeInsuranceDepositAccountAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["insurance_deposit_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["whitelist_insurance_account"],
            is_signer=False,
            is_writable=False,
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"U\xa3ry\x8b\xa7)%"
    encoded_args = layout.build(
        {
            "nonce": args["nonce"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
