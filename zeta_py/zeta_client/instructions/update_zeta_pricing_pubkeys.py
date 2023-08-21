from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class UpdateZetaPricingPubkeysArgs(typing.TypedDict):
    args: types.update_zeta_pricing_pubkeys_args.UpdateZetaPricingPubkeysArgs


layout = borsh.CStruct("args" / types.update_zeta_pricing_pubkeys_args.UpdateZetaPricingPubkeysArgs.layout)


class UpdateZetaPricingPubkeysAccounts(typing.TypedDict):
    state: Pubkey
    pricing: Pubkey
    admin: Pubkey


def update_zeta_pricing_pubkeys(
    args: UpdateZetaPricingPubkeysArgs,
    accounts: UpdateZetaPricingPubkeysAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["pricing"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xa9\xdd\x17\xf8\xdbz\x8e\x9e"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
