from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID

from ..program_id import PROGRAM_ID


class InitializeReferrerAccountsArgs(typing.TypedDict):
    referrer_id: str


layout = borsh.CStruct("referrer_id" / borsh.String)


class InitializeReferrerAccountsAccounts(typing.TypedDict):
    authority: Pubkey
    referrer_id_account: Pubkey
    referrer_pubkey_account: Pubkey


def initialize_referrer_accounts(
    args: InitializeReferrerAccountsArgs,
    accounts: InitializeReferrerAccountsAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["referrer_id_account"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["referrer_pubkey_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"i\xe4H\xdd\xda\x12\xb3u"
    encoded_args = layout.build(
        {
            "referrer_id": args["referrer_id"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
