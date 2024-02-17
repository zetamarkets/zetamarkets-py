from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.sysvar import RENT
from spl.token.constants import TOKEN_PROGRAM_ID

from ..program_id import PROGRAM_ID


class ExecuteTriggerOrderV2Args(typing.TypedDict):
    trigger_order_bit: int


layout = borsh.CStruct("trigger_order_bit" / borsh.U8)


class ExecuteTriggerOrderV2Accounts(typing.TypedDict):
    payer: Pubkey
    trigger_order: Pubkey
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


def execute_trigger_order_v2(
    args: ExecuteTriggerOrderV2Args,
    accounts: ExecuteTriggerOrderV2Accounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["trigger_order"], is_signer=False, is_writable=True),
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
    identifier = b"\x05\xe40w\x08\xd6\xb7\x96"
    encoded_args = layout.build(
        {
            "trigger_order_bit": args["trigger_order_bit"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
