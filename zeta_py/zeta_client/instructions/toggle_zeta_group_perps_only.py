from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class ToggleZetaGroupPerpsOnlyAccounts(typing.TypedDict):
    state: Pubkey
    zeta_group: Pubkey
    admin: Pubkey


def toggle_zeta_group_perps_only(
    accounts: ToggleZetaGroupPerpsOnlyAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xaasM\x0b\xa1\x9d\xf7\xa9"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
