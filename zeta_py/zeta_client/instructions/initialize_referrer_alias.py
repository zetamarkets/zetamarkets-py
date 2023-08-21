from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID

from ..program_id import PROGRAM_ID


class InitializeReferrerAliasArgs(typing.TypedDict):
    alias: str


layout = borsh.CStruct("alias" / borsh.String)


class InitializeReferrerAliasAccounts(typing.TypedDict):
    referrer: Pubkey
    referrer_alias: Pubkey
    referrer_account: Pubkey


def initialize_referrer_alias(
    args: InitializeReferrerAliasArgs,
    accounts: InitializeReferrerAliasAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["referrer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["referrer_alias"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["referrer_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"C\x1c\x03N\x8cl\x14\x8a"
    encoded_args = layout.build(
        {
            "alias": args["alias"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
