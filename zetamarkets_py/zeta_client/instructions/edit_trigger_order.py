from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class EditTriggerOrderArgs(typing.TypedDict):
    order_price: int
    trigger_price: typing.Optional[int]
    trigger_direction: typing.Optional[types.trigger_direction.TriggerDirectionKind]
    trigger_ts: typing.Optional[int]
    size: int
    side: types.side.SideKind
    order_type: types.order_type.OrderTypeKind
    reduce_only: bool


layout = borsh.CStruct(
    "order_price" / borsh.U64,
    "trigger_price" / borsh.Option(borsh.U64),
    "trigger_direction" / borsh.Option(types.trigger_direction.layout),
    "trigger_ts" / borsh.Option(borsh.U64),
    "size" / borsh.U64,
    "side" / types.side.layout,
    "order_type" / types.order_type.layout,
    "reduce_only" / borsh.Bool,
)


class EditTriggerOrderAccounts(typing.TypedDict):
    owner: Pubkey
    trigger_order: Pubkey


def edit_trigger_order(
    args: EditTriggerOrderArgs,
    accounts: EditTriggerOrderAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["owner"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["trigger_order"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xb4+\xd7p\xfet\x14\x85"
    encoded_args = layout.build(
        {
            "order_price": args["order_price"],
            "trigger_price": args["trigger_price"],
            "trigger_direction": (
                None if args["trigger_direction"] is None else args["trigger_direction"].to_encodable()
            ),
            "trigger_ts": args["trigger_ts"],
            "size": args["size"],
            "side": args["side"].to_encodable(),
            "order_type": args["order_type"].to_encodable(),
            "reduce_only": args["reduce_only"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
