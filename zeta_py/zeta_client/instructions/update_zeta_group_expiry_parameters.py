from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class UpdateZetaGroupExpiryParametersArgs(typing.TypedDict):
    args: types.update_zeta_group_expiry_args.UpdateZetaGroupExpiryArgs


layout = borsh.CStruct("args" / types.update_zeta_group_expiry_args.UpdateZetaGroupExpiryArgs.layout)


class UpdateZetaGroupExpiryParametersAccounts(typing.TypedDict):
    state: Pubkey
    zeta_group: Pubkey
    admin: Pubkey


def update_zeta_group_expiry_parameters(
    args: UpdateZetaGroupExpiryParametersArgs,
    accounts: UpdateZetaGroupExpiryParametersAccounts,
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
    identifier = b"\x11Eyh\xe1\xce\x8c\xd7"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
