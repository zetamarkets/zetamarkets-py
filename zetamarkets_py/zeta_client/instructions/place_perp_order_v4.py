from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.sysvar import RENT
from spl.token.constants import TOKEN_PROGRAM_ID

from .. import types
from ..program_id import PROGRAM_ID


class PlacePerpOrderV4Args(typing.TypedDict):
    price: int
    size: int
    side: types.side.SideKind
    order_type: types.order_type.OrderTypeKind
    reduce_only: bool
    client_order_id: typing.Optional[int]
    tag: typing.Optional[str]
    tif_offset: typing.Optional[int]
    asset: types.asset.AssetKind


layout = borsh.CStruct(
    "price" / borsh.U64,
    "size" / borsh.U64,
    "side" / types.side.layout,
    "order_type" / types.order_type.layout,
    "reduce_only" / borsh.Bool,
    "client_order_id" / borsh.Option(borsh.U64),
    "tag" / borsh.Option(borsh.String),
    "tif_offset" / borsh.Option(borsh.U16),
    "asset" / types.asset.layout,
)


class PlacePerpOrderV4Accounts(typing.TypedDict):
    authority: Pubkey
    place_order_accounts: PlaceOrderAccountsNested


class PlaceOrderAccountsNested(typing.TypedDict):
    state: Pubkey
    pricing: Pubkey
    margin_account: Pubkey
    dex_program: Pubkey
    serum_authority: Pubkey
    open_orders: Pubkey
    market_accounts: MarketAccountsNested
    oracle: Pubkey
    oracle_backup_feed: Pubkey
    oracle_backup_program: Pubkey
    market_mint: Pubkey
    mint_authority: Pubkey
    perp_sync_queue: Pubkey


class MarketAccountsNested(typing.TypedDict):
    market: Pubkey
    request_queue: Pubkey
    event_queue: Pubkey
    bids: Pubkey
    asks: Pubkey
    order_payer_token_account: Pubkey
    coin_vault: Pubkey
    pc_vault: Pubkey
    coin_wallet: Pubkey
    pc_wallet: Pubkey


def place_perp_order_v4(
    args: PlacePerpOrderV4Args,
    accounts: PlacePerpOrderV4Accounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["state"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["pricing"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["margin_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["dex_program"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["serum_authority"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["open_orders"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["market_accounts"]["market"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["market_accounts"]["request_queue"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["market_accounts"]["event_queue"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["market_accounts"]["bids"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["market_accounts"]["asks"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["market_accounts"]["order_payer_token_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["market_accounts"]["coin_vault"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["market_accounts"]["pc_vault"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["market_accounts"]["coin_wallet"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["market_accounts"]["pc_wallet"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["oracle"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["oracle_backup_feed"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["oracle_backup_program"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["market_mint"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["mint_authority"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["place_order_accounts"]["perp_sync_queue"],
            is_signer=False,
            is_writable=True,
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xa6\x8a\xcddZn\xbf["
    encoded_args = layout.build(
        {
            "price": args["price"],
            "size": args["size"],
            "side": args["side"].to_encodable(),
            "order_type": args["order_type"].to_encodable(),
            "reduce_only": args["reduce_only"],
            "client_order_id": args["client_order_id"],
            "tag": args["tag"],
            "tif_offset": args["tif_offset"],
            "asset": args["asset"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
