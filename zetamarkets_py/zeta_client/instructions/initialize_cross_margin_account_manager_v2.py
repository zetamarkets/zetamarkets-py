from __future__ import annotations

import typing

import borsh_construct as borsh
from anchorpy.borsh_extension import BorshPubkey
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID

from ..program_id import PROGRAM_ID


class InitializeCrossMarginAccountManagerV2Args(typing.TypedDict):
    referrer: typing.Optional[Pubkey]


layout = borsh.CStruct("referrer" / borsh.Option(BorshPubkey))


class InitializeCrossMarginAccountManagerV2Accounts(typing.TypedDict):
    cross_margin_account_manager: Pubkey
    authority: Pubkey
    payer: Pubkey
    zeta_program: Pubkey


def initialize_cross_margin_account_manager_v2(
    args: InitializeCrossMarginAccountManagerV2Args,
    accounts: InitializeCrossMarginAccountManagerV2Accounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["cross_margin_account_manager"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["zeta_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xa6\xcb\xb0\xd2\xb04\x8ci"
    encoded_args = layout.build(
        {
            "referrer": args["referrer"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
