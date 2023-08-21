from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class InitializeMarketTifEpochCycleArgs(typing.TypedDict):
    epoch_length: int


layout = borsh.CStruct("epoch_length" / borsh.U16)


class InitializeMarketTifEpochCycleAccounts(typing.TypedDict):
    state: Pubkey
    admin: Pubkey
    market: Pubkey
    serum_authority: Pubkey
    dex_program: Pubkey


def initialize_market_tif_epoch_cycle(
    args: InitializeMarketTifEpochCycleArgs,
    accounts: InitializeMarketTifEpochCycleAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["serum_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["dex_program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xc7\x8f\xad\x93\xca\xcc@\xcc"
    encoded_args = layout.build(
        {
            "epoch_length": args["epoch_length"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
