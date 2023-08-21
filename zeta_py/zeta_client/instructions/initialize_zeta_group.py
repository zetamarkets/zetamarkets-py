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


class InitializeZetaGroupArgs(typing.TypedDict):
    args: types.initialize_zeta_group_args.InitializeZetaGroupArgs


layout = borsh.CStruct("args" / types.initialize_zeta_group_args.InitializeZetaGroupArgs.layout)


class InitializeZetaGroupAccounts(typing.TypedDict):
    state: Pubkey
    admin: Pubkey
    underlying_mint: Pubkey
    zeta_program: Pubkey
    oracle: Pubkey
    oracle_backup_feed: Pubkey
    oracle_backup_program: Pubkey
    zeta_group: Pubkey
    greeks: Pubkey
    perp_sync_queue: Pubkey
    underlying: Pubkey
    vault: Pubkey
    insurance_vault: Pubkey
    socialized_loss_account: Pubkey
    usdc_mint: Pubkey


def initialize_zeta_group(
    args: InitializeZetaGroupArgs,
    accounts: InitializeZetaGroupAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["underlying_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle_backup_feed"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle_backup_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["perp_sync_queue"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["underlying"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["insurance_vault"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["socialized_loss_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["usdc_mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x06\x87$\xe8#'\xfaG"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
