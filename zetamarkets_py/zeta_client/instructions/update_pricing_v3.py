from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class UpdatePricingV3Args(typing.TypedDict):
    asset: types.asset.AssetKind
    price: int
    timestamp: int


layout = borsh.CStruct("asset" / types.asset.layout, "price" / borsh.U64, "timestamp" / borsh.U64)


class UpdatePricingV3Accounts(typing.TypedDict):
    state: Pubkey
    pricing: Pubkey
    oracle: Pubkey
    perp_market: Pubkey
    perp_bids: Pubkey
    perp_asks: Pubkey
    pricing_admin: Pubkey


def update_pricing_v3(
    args: UpdatePricingV3Args,
    accounts: UpdatePricingV3Accounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["pricing"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["perp_market"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["perp_bids"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["perp_asks"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["pricing_admin"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xdf:\xb4Vf\xfb\xedR"
    encoded_args = layout.build(
        {
            "asset": args["asset"].to_encodable(),
            "price": args["price"],
            "timestamp": args["timestamp"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
