from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class UpdateZetaGroupPerpParametersArgs(typing.TypedDict):
    args: types.update_perp_parameters_args.UpdatePerpParametersArgs


layout = borsh.CStruct("args" / types.update_perp_parameters_args.UpdatePerpParametersArgs.layout)


class UpdateZetaGroupPerpParametersAccounts(typing.TypedDict):
    state: Pubkey
    zeta_group: Pubkey
    admin: Pubkey


def update_zeta_group_perp_parameters(
    args: UpdateZetaGroupPerpParametersArgs,
    accounts: UpdateZetaGroupPerpParametersAccounts,
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
    identifier = b"H\x98\x8c\x9e\xc3]\xf7\x1f"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
