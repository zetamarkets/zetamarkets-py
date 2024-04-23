from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class CloseOpenOrdersV4Args(typing.TypedDict):
    map_nonce: int
    asset: types.asset.AssetKind


layout = borsh.CStruct("map_nonce" / borsh.U8, "asset" / types.asset.layout)


class CloseOpenOrdersV4Accounts(typing.TypedDict):
    state: Pubkey
    pricing: Pubkey
    dex_program: Pubkey
    open_orders: Pubkey
    cross_margin_account: Pubkey
    authority: Pubkey
    market: Pubkey
    serum_authority: Pubkey
    open_orders_map: Pubkey
    event_queue: Pubkey


def close_open_orders_v4(
    args: CloseOpenOrdersV4Args,
    accounts: CloseOpenOrdersV4Accounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["pricing"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["dex_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["open_orders"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["cross_margin_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["authority"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["serum_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["open_orders_map"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["event_queue"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xa7e\xa1\xf6\xd01\x06\xe1"
    encoded_args = layout.build(
        {
            "map_nonce": args["map_nonce"],
            "asset": args["asset"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
