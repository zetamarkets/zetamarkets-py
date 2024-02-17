from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class UpdateMarginParametersArgs(typing.TypedDict):
    args: types.update_margin_parameters_args.UpdateMarginParametersArgs
    asset: types.asset.AssetKind


layout = borsh.CStruct(
    "args" / types.update_margin_parameters_args.UpdateMarginParametersArgs.layout,
    "asset" / types.asset.layout,
)


class UpdateMarginParametersAccounts(typing.TypedDict):
    state: Pubkey
    pricing: Pubkey
    admin: Pubkey


def update_margin_parameters(
    args: UpdateMarginParametersArgs,
    accounts: UpdateMarginParametersAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["pricing"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"E2\xae\xc5{\xc4H\xec"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
            "asset": args["asset"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
