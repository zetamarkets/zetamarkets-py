from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class LiquidateV2Args(typing.TypedDict):
    size: int
    asset: types.asset.AssetKind


layout = borsh.CStruct("size" / borsh.U64, "asset" / types.asset.layout)


class LiquidateV2Accounts(typing.TypedDict):
    state: Pubkey
    liquidator: Pubkey
    liquidator_account: Pubkey
    pricing: Pubkey
    oracle: Pubkey
    oracle_backup_feed: Pubkey
    oracle_backup_program: Pubkey
    market: Pubkey
    liquidated_account: Pubkey


def liquidate_v2(
    args: LiquidateV2Args,
    accounts: LiquidateV2Accounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["liquidator"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["liquidator_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["pricing"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle_backup_feed"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle_backup_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["liquidated_account"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x0fVU7\x02\xe1\xa1\xeb"
    encoded_args = layout.build(
        {
            "size": args["size"],
            "asset": args["asset"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
