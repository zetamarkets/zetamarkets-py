from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class ChooseAirdropCommunityArgs(typing.TypedDict):
    community: int


layout = borsh.CStruct("community" / borsh.U8)


class ChooseAirdropCommunityAccounts(typing.TypedDict):
    cross_margin_account_manager: Pubkey
    authority: Pubkey


def choose_airdrop_community(
    args: ChooseAirdropCommunityArgs,
    accounts: ChooseAirdropCommunityAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["cross_margin_account_manager"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"t\x9c\xc0R\xf8)s\xba"
    encoded_args = layout.build(
        {
            "community": args["community"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
