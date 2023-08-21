from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class CancelOrderNoErrorArgs(typing.TypedDict):
    side: types.side.SideKind
    order_id: int
    asset: types.asset.AssetKind


layout = borsh.CStruct("side" / types.side.layout, "order_id" / borsh.U128, "asset" / types.asset.layout)


class CancelOrderNoErrorAccounts(typing.TypedDict):
    authority: Pubkey
    cancel_accounts: CancelAccountsNested


class CancelAccountsNested(typing.TypedDict):
    state: Pubkey
    margin_account: Pubkey
    dex_program: Pubkey
    serum_authority: Pubkey
    open_orders: Pubkey
    market: Pubkey
    bids: Pubkey
    asks: Pubkey
    event_queue: Pubkey


def cancel_order_no_error(
    args: CancelOrderNoErrorArgs,
    accounts: CancelOrderNoErrorAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["state"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["margin_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["dex_program"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["serum_authority"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["open_orders"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["market"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["bids"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["asks"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["event_queue"],
            is_signer=False,
            is_writable=True,
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"_a\xd7\xcco3\xcc\xb8"
    encoded_args = layout.build(
        {
            "side": args["side"].to_encodable(),
            "order_id": args["order_id"],
            "asset": args["asset"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
