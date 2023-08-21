from typing import Tuple

from solana.utils.cluster import Cluster
from solders.pubkey import Pubkey

from zeta_py.constants import FLEXIBLE_MINTS, MINTS, Asset


def get_state(program_id: Pubkey) -> Tuple[Pubkey, int]:
    return Pubkey.find_program_address([b"state"], program_id)


def get_pricing(program_id: Pubkey) -> Tuple[Pubkey, int]:
    return Pubkey.find_program_address([b"pricing"], program_id)


def get_zeta_group(program_id: Pubkey, mint: Pubkey) -> Tuple[Pubkey, int]:
    return Pubkey.find_program_address([b"zeta-group", bytes(mint)], program_id)


def get_perp_sync_queue(program_id: Pubkey, zeta_group: Pubkey) -> Tuple[Pubkey, int]:
    return Pubkey.find_program_address([b"perp-sync-queue", bytes(zeta_group)], program_id)


def get_underlying_mint(asset: Asset, network: Cluster) -> Pubkey:
    if asset in MINTS:
        return MINTS[asset]
    if asset in FLEXIBLE_MINTS[network]:
        return FLEXIBLE_MINTS[network][asset]
    raise Exception("Underlying mint does not exist!")
