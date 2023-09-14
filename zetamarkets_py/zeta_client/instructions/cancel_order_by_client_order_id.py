from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class CancelOrderByClientOrderIdArgs(typing.TypedDict):
    client_order_id: int
    asset: types.asset.AssetKind


layout = borsh.CStruct("client_order_id" / borsh.U64, "asset" / types.asset.layout)


class CancelOrderByClientOrderIdAccounts(typing.TypedDict):
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


def cancel_order_by_client_order_id(
    args: CancelOrderByClientOrderIdArgs,
    accounts: CancelOrderByClientOrderIdAccounts,
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
    identifier = b"s\xb2\xc9\x08\xaf\xb7{w"
    encoded_args = layout.build(
        {
            "client_order_id": args["client_order_id"],
            "asset": args["asset"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
