from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class InitializeMarketIndexesArgs(typing.TypedDict):
    nonce: int
    asset: types.asset.AssetKind


layout = borsh.CStruct("nonce" / borsh.U8, "asset" / types.asset.layout)


class InitializeMarketIndexesAccounts(typing.TypedDict):
    state: Pubkey
    market_indexes: Pubkey
    admin: Pubkey
    pricing: Pubkey


def initialize_market_indexes(
    args: InitializeMarketIndexesArgs,
    accounts: InitializeMarketIndexesAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["market_indexes"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["pricing"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"[?\xcd\x90\x14S\xb1x"
    encoded_args = layout.build(
        {
            "nonce": args["nonce"],
            "asset": args["asset"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
