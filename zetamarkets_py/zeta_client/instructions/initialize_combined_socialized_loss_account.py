from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from spl.token.constants import TOKEN_PROGRAM_ID

from ..program_id import PROGRAM_ID


class InitializeCombinedSocializedLossAccountArgs(typing.TypedDict):
    nonce: int


layout = borsh.CStruct("nonce" / borsh.U8)


class InitializeCombinedSocializedLossAccountAccounts(typing.TypedDict):
    state: Pubkey
    socialized_loss_account: Pubkey
    usdc_mint: Pubkey
    admin: Pubkey


def initialize_combined_socialized_loss_account(
    args: InitializeCombinedSocializedLossAccountArgs,
    accounts: InitializeCombinedSocializedLossAccountAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["socialized_loss_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["usdc_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x88lX\xf5\xe6\xe0eR"
    encoded_args = layout.build(
        {
            "nonce": args["nonce"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
