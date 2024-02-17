from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID

from .. import types
from ..program_id import PROGRAM_ID


class PlaceTriggerOrderArgs(typing.TypedDict):
    trigger_order_bit: int
    order_price: int
    trigger_price: typing.Optional[int]
    trigger_direction: typing.Optional[types.trigger_direction.TriggerDirectionKind]
    trigger_ts: typing.Optional[int]
    size: int
    side: types.side.SideKind
    order_type: types.order_type.OrderTypeKind
    reduce_only: bool
    tag: typing.Optional[str]
    asset: types.asset.AssetKind


layout = borsh.CStruct(
    "trigger_order_bit" / borsh.U8,
    "order_price" / borsh.U64,
    "trigger_price" / borsh.Option(borsh.U64),
    "trigger_direction" / borsh.Option(types.trigger_direction.layout),
    "trigger_ts" / borsh.Option(borsh.U64),
    "size" / borsh.U64,
    "side" / types.side.layout,
    "order_type" / types.order_type.layout,
    "reduce_only" / borsh.Bool,
    "tag" / borsh.Option(borsh.String),
    "asset" / types.asset.layout,
)


class PlaceTriggerOrderAccounts(typing.TypedDict):
    state: Pubkey
    open_orders: Pubkey
    authority: Pubkey
    margin_account: Pubkey
    pricing: Pubkey
    trigger_order: Pubkey
    dex_program: Pubkey
    market: Pubkey


def place_trigger_order(
    args: PlaceTriggerOrderArgs,
    accounts: PlaceTriggerOrderAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["open_orders"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["margin_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["pricing"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["trigger_order"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["dex_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b" \x9c2\xbc\xe8\x9fp\xec"
    encoded_args = layout.build(
        {
            "trigger_order_bit": args["trigger_order_bit"],
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
            "tag": args["tag"],
            "asset": args["asset"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
