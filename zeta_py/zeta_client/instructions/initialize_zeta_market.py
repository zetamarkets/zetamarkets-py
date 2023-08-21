from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.sysvar import RENT
from spl.token.constants import TOKEN_PROGRAM_ID

from .. import types
from ..program_id import PROGRAM_ID


class InitializeZetaMarketArgs(typing.TypedDict):
    args: types.initialize_market_args.InitializeMarketArgs


layout = borsh.CStruct("args" / types.initialize_market_args.InitializeMarketArgs.layout)


class InitializeZetaMarketAccounts(typing.TypedDict):
    state: Pubkey
    market_indexes: Pubkey
    pricing: Pubkey
    admin: Pubkey
    market: Pubkey
    request_queue: Pubkey
    event_queue: Pubkey
    bids: Pubkey
    asks: Pubkey
    base_mint: Pubkey
    quote_mint: Pubkey
    zeta_base_vault: Pubkey
    zeta_quote_vault: Pubkey
    dex_base_vault: Pubkey
    dex_quote_vault: Pubkey
    vault_owner: Pubkey
    mint_authority: Pubkey
    serum_authority: Pubkey
    dex_program: Pubkey


def initialize_zeta_market(
    args: InitializeZetaMarketArgs,
    accounts: InitializeZetaMarketAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["market_indexes"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["pricing"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["request_queue"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["event_queue"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["bids"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["asks"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["base_mint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["quote_mint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["zeta_base_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["zeta_quote_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["dex_base_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["dex_quote_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["vault_owner"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["mint_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["serum_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["dex_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"t\xef\xe2\x95.\xa3\xdd\x03"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
