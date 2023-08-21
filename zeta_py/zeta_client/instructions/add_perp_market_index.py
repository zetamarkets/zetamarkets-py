from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class AddPerpMarketIndexArgs(typing.TypedDict):
    asset: types.asset.AssetKind


layout = borsh.CStruct("asset" / types.asset.layout)


class AddPerpMarketIndexAccounts(typing.TypedDict):
    market_indexes: Pubkey
    pricing: Pubkey


def add_perp_market_index(
    args: AddPerpMarketIndexArgs,
    accounts: AddPerpMarketIndexAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["market_indexes"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["pricing"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"z(\x0e@\xa9\x12\xe7\x88"
    encoded_args = layout.build(
        {
            "asset": args["asset"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
