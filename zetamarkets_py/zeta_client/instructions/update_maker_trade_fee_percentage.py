from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class UpdateMakerTradeFeePercentageArgs(typing.TypedDict):
    new_native_maker_trade_fee_percentage: int


layout = borsh.CStruct("new_native_maker_trade_fee_percentage" / borsh.U64)


class UpdateMakerTradeFeePercentageAccounts(typing.TypedDict):
    state: Pubkey
    admin: Pubkey


def update_maker_trade_fee_percentage(
    args: UpdateMakerTradeFeePercentageArgs,
    accounts: UpdateMakerTradeFeePercentageAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"8>y\xd2\xa6\xce&\xda"
    encoded_args = layout.build(
        {
            "new_native_maker_trade_fee_percentage": args["new_native_maker_trade_fee_percentage"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
