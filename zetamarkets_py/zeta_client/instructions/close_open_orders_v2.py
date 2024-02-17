from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class CloseOpenOrdersV2Args(typing.TypedDict):
    map_nonce: int


layout = borsh.CStruct("map_nonce" / borsh.U8)


class CloseOpenOrdersV2Accounts(typing.TypedDict):
    state: Pubkey
    dex_program: Pubkey
    open_orders: Pubkey
    margin_account: Pubkey
    authority: Pubkey
    market: Pubkey
    serum_authority: Pubkey
    open_orders_map: Pubkey


def close_open_orders_v2(
    args: CloseOpenOrdersV2Args,
    accounts: CloseOpenOrdersV2Accounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["dex_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["open_orders"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["margin_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["serum_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["open_orders_map"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"N\x98\xc4\xa3D\xb3yH"
    encoded_args = layout.build(
        {
            "map_nonce": args["map_nonce"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
