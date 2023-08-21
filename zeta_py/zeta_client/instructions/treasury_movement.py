from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID

from .. import types
from ..program_id import PROGRAM_ID


class TreasuryMovementArgs(typing.TypedDict):
    treasury_movement_type: types.treasury_movement_type.TreasuryMovementTypeKind
    amount: int


layout = borsh.CStruct("treasury_movement_type" / types.treasury_movement_type.layout, "amount" / borsh.U64)


class TreasuryMovementAccounts(typing.TypedDict):
    state: Pubkey
    insurance_vault: Pubkey
    treasury_wallet: Pubkey
    referrals_rewards_wallet: Pubkey
    admin: Pubkey


def treasury_movement(
    args: TreasuryMovementArgs,
    accounts: TreasuryMovementAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["insurance_vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["treasury_wallet"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["referrals_rewards_wallet"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b'\x01"\xf2i\xd7\xd3\x9d\x12'
    encoded_args = layout.build(
        {
            "treasury_movement_type": args["treasury_movement_type"].to_encodable(),
            "amount": args["amount"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
