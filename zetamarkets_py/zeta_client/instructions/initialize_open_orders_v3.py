from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.sysvar import RENT

from .. import types
from ..program_id import PROGRAM_ID


class InitializeOpenOrdersV3Args(typing.TypedDict):
    asset: types.asset.AssetKind


layout = borsh.CStruct("asset" / types.asset.layout)


class InitializeOpenOrdersV3Accounts(typing.TypedDict):
    state: Pubkey
    dex_program: Pubkey
    open_orders: Pubkey
    cross_margin_account: Pubkey
    authority: Pubkey
    payer: Pubkey
    market: Pubkey
    serum_authority: Pubkey
    open_orders_map: Pubkey


def initialize_open_orders_v3(
    args: InitializeOpenOrdersV3Args,
    accounts: InitializeOpenOrdersV3Accounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["dex_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["open_orders"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["cross_margin_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["serum_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["open_orders_map"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x16\xbf\x8b\x88y'T\xca"
    encoded_args = layout.build(
        {
            "asset": args["asset"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
