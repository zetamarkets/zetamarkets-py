from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class EditTriggerOrderV2Args(typing.TypedDict):
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


class EditTriggerOrderV2Accounts(typing.TypedDict):
    owner: Pubkey
    trigger_order: Pubkey
    state: Pubkey
    margin_account: Pubkey


def edit_trigger_order_v2(
    args: EditTriggerOrderV2Args,
    accounts: EditTriggerOrderV2Accounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["owner"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["trigger_order"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["margin_account"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"I\x9f\xcd\xb1+Uu\x89"
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
