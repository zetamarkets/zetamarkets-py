from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.sysvar import RENT
from spl.token.constants import TOKEN_PROGRAM_ID

from .. import types
from ..program_id import PROGRAM_ID


class InitializeZetaPricingArgs(typing.TypedDict):
    args: types.initialize_zeta_pricing_args.InitializeZetaPricingArgs


layout = borsh.CStruct("args" / types.initialize_zeta_pricing_args.InitializeZetaPricingArgs.layout)


class InitializeZetaPricingAccounts(typing.TypedDict):
    state: Pubkey
    pricing: Pubkey
    admin: Pubkey


def initialize_zeta_pricing(
    args: InitializeZetaPricingArgs,
    accounts: InitializeZetaPricingAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["pricing"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"#\xd1\xb4\x1d\xf5\xc7}\x10"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
