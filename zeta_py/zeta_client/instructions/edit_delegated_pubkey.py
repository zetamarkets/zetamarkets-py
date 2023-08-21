from __future__ import annotations

import typing

import borsh_construct as borsh
from anchorpy.borsh_extension import BorshPubkey
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class EditDelegatedPubkeyArgs(typing.TypedDict):
    new_key: Pubkey


layout = borsh.CStruct("new_key" / BorshPubkey)


class EditDelegatedPubkeyAccounts(typing.TypedDict):
    margin_account: Pubkey
    authority: Pubkey


def edit_delegated_pubkey(
    args: EditDelegatedPubkeyArgs,
    accounts: EditDelegatedPubkeyAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["margin_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x89\xf5GY.\xf9\x165"
    encoded_args = layout.build(
        {
            "new_key": args["new_key"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
