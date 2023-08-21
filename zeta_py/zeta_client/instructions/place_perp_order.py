from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.sysvar import RENT
from spl.token.constants import TOKEN_PROGRAM_ID

from .. import types
from ..program_id import PROGRAM_ID


class PlacePerpOrderArgs(typing.TypedDict):
    price: int
    size: int
    side: types.side.SideKind
    order_type: types.order_type.OrderTypeKind
    client_order_id: typing.Optional[int]
    tag: typing.Optional[str]


layout = borsh.CStruct(
    "price" / borsh.U64,
    "size" / borsh.U64,
    "side" / types.side.layout,
    "order_type" / types.order_type.layout,
    "client_order_id" / borsh.Option(borsh.U64),
    "tag" / borsh.Option(borsh.String),
)


class PlacePerpOrderAccounts(typing.TypedDict):
    state: Pubkey
    zeta_group: Pubkey
    margin_account: Pubkey
    authority: Pubkey
    dex_program: Pubkey
    serum_authority: Pubkey
    greeks: Pubkey
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


def place_perp_order(
    args: PlacePerpOrderArgs,
    accounts: PlacePerpOrderAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["margin_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["dex_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["serum_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["open_orders"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["market_accounts"]["market"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["market_accounts"]["request_queue"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["market_accounts"]["event_queue"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["market_accounts"]["bids"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["market_accounts"]["asks"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["market_accounts"]["order_payer_token_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["market_accounts"]["coin_vault"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["market_accounts"]["pc_vault"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["market_accounts"]["coin_wallet"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["market_accounts"]["pc_wallet"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle_backup_feed"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle_backup_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["market_mint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["mint_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["perp_sync_queue"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"E\xa1]\xcax~L\xb9"
    encoded_args = layout.build(
        {
            "price": args["price"],
            "size": args["size"],
            "side": args["side"].to_encodable(),
            "order_type": args["order_type"].to_encodable(),
            "client_order_id": args["client_order_id"],
            "tag": args["tag"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
