from __future__ import annotations

import typing

import borsh_construct as borsh
from construct import Construct
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class PositionMovementArgs(typing.TypedDict):
    movement_type: types.movement_type.MovementTypeKind
    movements: list[types.position_movement_arg.PositionMovementArg]


layout = borsh.CStruct(
    "movement_type" / types.movement_type.layout,
    "movements" / borsh.Vec(typing.cast(Construct, types.position_movement_arg.PositionMovementArg.layout)),
)


class PositionMovementAccounts(typing.TypedDict):
    state: Pubkey
    zeta_group: Pubkey
    margin_account: Pubkey
    spread_account: Pubkey
    authority: Pubkey
    greeks: Pubkey
    oracle: Pubkey
    oracle_backup_feed: Pubkey
    oracle_backup_program: Pubkey


def position_movement(
    args: PositionMovementArgs,
    accounts: PositionMovementAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["margin_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["spread_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle_backup_feed"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle_backup_program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"u\x10K\xf9\xb3\x7f\xab\x93"
    encoded_args = layout.build(
        {
            "movement_type": args["movement_type"].to_encodable(),
            "movements": list(map(lambda item: item.to_encodable(), args["movements"])),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
