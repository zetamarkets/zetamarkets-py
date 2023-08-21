from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID

from ..program_id import PROGRAM_ID


class CollectTreasuryFundsArgs(typing.TypedDict):
    amount: int


layout = borsh.CStruct("amount" / borsh.U64)


class CollectTreasuryFundsAccounts(typing.TypedDict):
    state: Pubkey
    treasury_wallet: Pubkey
    collection_token_account: Pubkey
    admin: Pubkey


def collect_treasury_funds(
    args: CollectTreasuryFundsArgs,
    accounts: CollectTreasuryFundsAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["treasury_wallet"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["collection_token_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xf3\xd5\x04\xec\x1a\xf6\xb4\xae"
    encoded_args = layout.build(
        {
            "amount": args["amount"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
