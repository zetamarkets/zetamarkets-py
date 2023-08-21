from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class UpdateZetaGroupMarginParametersArgs(typing.TypedDict):
    args: types.update_margin_parameters_args.UpdateMarginParametersArgs


layout = borsh.CStruct("args" / types.update_margin_parameters_args.UpdateMarginParametersArgs.layout)


class UpdateZetaGroupMarginParametersAccounts(typing.TypedDict):
    state: Pubkey
    zeta_group: Pubkey
    admin: Pubkey


def update_zeta_group_margin_parameters(
    args: UpdateZetaGroupMarginParametersArgs,
    accounts: UpdateZetaGroupMarginParametersAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"<\xd0y\x93\xf2j\x0b\xfe"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
