from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class UpdateMinLotArgs(typing.TypedDict):
    asset: types.asset.AssetKind
    min_lot_size: int


layout = borsh.CStruct("asset" / types.asset.layout, "min_lot_size" / borsh.U32)


class UpdateMinLotAccounts(typing.TypedDict):
    state: Pubkey
    admin: Pubkey


def update_min_lot(
    args: UpdateMinLotArgs,
    accounts: UpdateMinLotAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x06\x88\x05\x0c\xe5\x92fY"
    encoded_args = layout.build(
        {
            "asset": args["asset"].to_encodable(),
            "min_lot_size": args["min_lot_size"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
