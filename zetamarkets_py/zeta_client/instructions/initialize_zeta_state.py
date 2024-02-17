from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.sysvar import RENT
from spl.token.constants import TOKEN_PROGRAM_ID

from .. import types
from ..program_id import PROGRAM_ID


class InitializeZetaStateArgs(typing.TypedDict):
    args: types.initialize_state_args.InitializeStateArgs


layout = borsh.CStruct("args" / types.initialize_state_args.InitializeStateArgs.layout)


class InitializeZetaStateAccounts(typing.TypedDict):
    state: Pubkey
    mint_authority: Pubkey
    serum_authority: Pubkey
    treasury_wallet: Pubkey
    referrals_admin: Pubkey
    referrals_rewards_wallet: Pubkey
    usdc_mint: Pubkey
    admin: Pubkey
    secondary_admin: Pubkey


def initialize_zeta_state(
    args: InitializeZetaStateArgs,
    accounts: InitializeZetaStateAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["mint_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["serum_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["treasury_wallet"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["referrals_admin"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["referrals_rewards_wallet"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["usdc_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["secondary_admin"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"D'K\x8e\xbf\x92^\xde"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
