from __future__ import annotations

import typing

import borsh_construct as borsh
from construct import Construct
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.sysvar import RENT
from spl.token.constants import TOKEN_PROGRAM_ID

from .. import types
from ..program_id import PROGRAM_ID


class PlaceMultiOrdersArgs(typing.TypedDict):
    asset: types.asset.AssetKind
    bid_orders: list[types.order_args.OrderArgs]
    ask_orders: list[types.order_args.OrderArgs]
    order_type: types.order_type.OrderTypeKind


layout = borsh.CStruct(
    "asset" / types.asset.layout,
    "bid_orders" / borsh.Vec(typing.cast(Construct, types.order_args.OrderArgs.layout)),
    "ask_orders" / borsh.Vec(typing.cast(Construct, types.order_args.OrderArgs.layout)),
    "order_type" / types.order_type.layout,
)


class PlaceMultiOrdersAccounts(typing.TypedDict):
    authority: Pubkey
    state: Pubkey
    pricing: Pubkey
    margin_account: Pubkey
    dex_program: Pubkey
    serum_authority: Pubkey
    open_orders: Pubkey
    market: Pubkey
    request_queue: Pubkey
    event_queue: Pubkey
    bids: Pubkey
    asks: Pubkey
    market_base_vault: Pubkey
    market_quote_vault: Pubkey
    zeta_base_vault: Pubkey
    zeta_quote_vault: Pubkey
    oracle: Pubkey
    oracle_backup_feed: Pubkey
    oracle_backup_program: Pubkey
    market_base_mint: Pubkey
    market_quote_mint: Pubkey
    mint_authority: Pubkey
    perp_sync_queue: Pubkey


def place_multi_orders(
    args: PlaceMultiOrdersArgs,
    accounts: PlaceMultiOrdersAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["pricing"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["margin_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["dex_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["serum_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["open_orders"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["request_queue"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["event_queue"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["bids"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["asks"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["market_base_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["market_quote_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["zeta_base_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["zeta_quote_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle_backup_feed"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle_backup_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["market_base_mint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["market_quote_mint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["mint_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["perp_sync_queue"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xcc\xd7\xf3\xf3;\xea\xe1y"
    encoded_args = layout.build(
        {
            "asset": args["asset"].to_encodable(),
            "bid_orders": list(map(lambda item: item.to_encodable(), args["bid_orders"])),
            "ask_orders": list(map(lambda item: item.to_encodable(), args["ask_orders"])),
            "order_type": args["order_type"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
