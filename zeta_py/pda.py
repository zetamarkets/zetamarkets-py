from typing import Tuple
from solders.pubkey import Pubkey


def get_state(program_id: Pubkey) -> Tuple[Pubkey, int]:
    return Pubkey.find_program_address([b"state"], program_id)


def get_pricing(program_id: Pubkey) -> Tuple[Pubkey, int]:
    return Pubkey.find_program_address([b"pricing"], program_id)
