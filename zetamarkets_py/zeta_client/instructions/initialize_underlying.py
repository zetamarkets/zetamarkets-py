from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID

from ..program_id import PROGRAM_ID


class InitializeUnderlyingArgs(typing.TypedDict):
    flex_underlying: bool


layout = borsh.CStruct("flex_underlying" / borsh.Bool)


class InitializeUnderlyingAccounts(typing.TypedDict):
    admin: Pubkey
    zeta_program: Pubkey
    state: Pubkey
    underlying: Pubkey
    underlying_mint: Pubkey


def initialize_underlying(
    args: InitializeUnderlyingArgs,
    accounts: InitializeUnderlyingAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["underlying"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["underlying_mint"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"rl\xd5\\\xaf|+\x13"
    encoded_args = layout.build(
        {
            "flex_underlying": args["flex_underlying"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
