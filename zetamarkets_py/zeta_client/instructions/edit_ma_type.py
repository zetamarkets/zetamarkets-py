from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class EditMaTypeArgs(typing.TypedDict):
    ma_type: types.margin_account_type.MarginAccountTypeKind


layout = borsh.CStruct("ma_type" / types.margin_account_type.layout)


class EditMaTypeAccounts(typing.TypedDict):
    state: Pubkey
    admin: Pubkey
    margin_account: Pubkey


def edit_ma_type(
    args: EditMaTypeArgs,
    accounts: EditMaTypeAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["margin_account"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xe7\xd032\xde\x93LN"
    encoded_args = layout.build(
        {
            "ma_type": args["ma_type"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
