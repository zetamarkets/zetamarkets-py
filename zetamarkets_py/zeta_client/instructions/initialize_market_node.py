from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID

from .. import types
from ..program_id import PROGRAM_ID


class InitializeMarketNodeArgs(typing.TypedDict):
    args: types.initialize_market_node_args.InitializeMarketNodeArgs


layout = borsh.CStruct("args" / types.initialize_market_node_args.InitializeMarketNodeArgs.layout)


class InitializeMarketNodeAccounts(typing.TypedDict):
    zeta_group: Pubkey
    market_node: Pubkey
    greeks: Pubkey
    payer: Pubkey


def initialize_market_node(
    args: InitializeMarketNodeArgs,
    accounts: InitializeMarketNodeAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["market_node"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"2v\x15\x15\xb3\xf8\x17\x80"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
