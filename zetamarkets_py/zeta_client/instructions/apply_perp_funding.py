from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class ApplyPerpFundingArgs(typing.TypedDict):
    asset: types.asset.AssetKind


layout = borsh.CStruct("asset" / types.asset.layout)


class ApplyPerpFundingAccounts(typing.TypedDict):
    state: Pubkey
    pricing: Pubkey


def apply_perp_funding(
    args: ApplyPerpFundingArgs,
    accounts: ApplyPerpFundingAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["pricing"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x17R\xe1\xde\xdbz\xe6\xfb"
    encoded_args = layout.build(
        {
            "asset": args["asset"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
