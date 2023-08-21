from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class CleanZetaMarketHaltedArgs(typing.TypedDict):
    asset: types.asset.AssetKind


layout = borsh.CStruct("asset" / types.asset.layout)


class CleanZetaMarketHaltedAccounts(typing.TypedDict):
    state: Pubkey
    market: Pubkey
    bids: Pubkey
    asks: Pubkey


def clean_zeta_market_halted(
    args: CleanZetaMarketHaltedArgs,
    accounts: CleanZetaMarketHaltedAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["bids"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["asks"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x89\x8c^\x12\xe7\xe8\xd9\xcc"
    encoded_args = layout.build(
        {
            "asset": args["asset"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
