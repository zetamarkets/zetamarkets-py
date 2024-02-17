from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class ToggleMarketMakerArgs(typing.TypedDict):
    is_market_maker: bool


layout = borsh.CStruct("is_market_maker" / borsh.Bool)


class ToggleMarketMakerAccounts(typing.TypedDict):
    state: Pubkey
    admin: Pubkey
    margin_account: Pubkey


def toggle_market_maker(
    args: ToggleMarketMakerArgs,
    accounts: ToggleMarketMakerAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["margin_account"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xcb\xf7T\x9fh\xfd\x94P"
    encoded_args = layout.build(
        {
            "is_market_maker": args["is_market_maker"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
