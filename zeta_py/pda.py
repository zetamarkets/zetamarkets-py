from typing import Tuple

from solders.pubkey import Pubkey
from zeta_py import constants

from zeta_py.constants import FLEXIBLE_MINTS, MINTS, Asset
from zeta_py.types import Network


def get_state_address(program_id: Pubkey) -> Tuple[Pubkey, int]:
    return Pubkey.find_program_address([b"state"], program_id)


def get_pricing_address(program_id: Pubkey) -> Tuple[Pubkey, int]:
    return Pubkey.find_program_address([b"pricing"], program_id)


def get_zeta_group_address(program_id: Pubkey, mint: Pubkey) -> Tuple[Pubkey, int]:
    return Pubkey.find_program_address([b"zeta-group", bytes(mint)], program_id)


def get_perp_sync_queue_address(program_id: Pubkey, zeta_group: Pubkey) -> Tuple[Pubkey, int]:
    return Pubkey.find_program_address([b"perp-sync-queue", bytes(zeta_group)], program_id)


def get_margin_account_address(
    program_id: Pubkey,
    authority: Pubkey,
    subaccount_index: int = 0,
) -> Tuple[Pubkey, int]:
    return Pubkey.find_program_address(
        [
            b"cross-margin",
            bytes(authority),
            bytes([subaccount_index]),
        ],
        program_id,
    )


def get_open_orders_address(
    program_id: Pubkey, dex_program_id: Pubkey, market: Pubkey, margin_account: Pubkey
) -> Tuple[Pubkey, int]:
    return Pubkey.find_program_address(
        [b"cross-open-orders", bytes(dex_program_id), bytes(market), bytes(margin_account)],
        program_id,
    )


def get_underlying_mint_address(asset: Asset, network: Network) -> Pubkey:
    if asset in MINTS:
        return MINTS[asset]
    if asset in FLEXIBLE_MINTS[network]:
        return FLEXIBLE_MINTS[network][asset]
    raise Exception("Underlying mint does not exist!")
