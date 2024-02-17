from solders.pubkey import Pubkey
from solders.token import ID as TOKEN_PROGRAM_ID
from spl.token.constants import ASSOCIATED_TOKEN_PROGRAM_ID

from zetamarkets_py.constants import FLEXIBLE_MINTS, MINTS, Asset
from zetamarkets_py.types import Network


def get_state_address(program_id: Pubkey) -> Pubkey:
    return Pubkey.find_program_address([b"state"], program_id)[0]


def get_pricing_address(program_id: Pubkey) -> Pubkey:
    return Pubkey.find_program_address([b"pricing"], program_id)[0]


def get_zeta_group_address(program_id: Pubkey, mint: Pubkey) -> Pubkey:
    return Pubkey.find_program_address([b"zeta-group", bytes(mint)], program_id)[0]


def get_perp_sync_queue_address(program_id: Pubkey, zeta_group: Pubkey) -> Pubkey:
    return Pubkey.find_program_address([b"perp-sync-queue", bytes(zeta_group)], program_id)[0]


def get_margin_account_address(
    program_id: Pubkey,
    authority: Pubkey,
    subaccount_index: int = 0,
) -> Pubkey:
    return Pubkey.find_program_address(
        [
            b"cross-margin",
            bytes(authority),
            bytes([subaccount_index]),
        ],
        program_id,
    )[0]


def get_open_orders_address(
    program_id: Pubkey, dex_program_id: Pubkey, market: Pubkey, margin_account: Pubkey
) -> Pubkey:
    return Pubkey.find_program_address(
        [b"cross-open-orders", bytes(dex_program_id), bytes(market), bytes(margin_account)],
        program_id,
    )[0]


def get_cross_margin_account_manager_address(program_id: Pubkey, authority: Pubkey) -> Pubkey:
    return Pubkey.find_program_address(
        [b"cross-margin-manager", bytes(authority)],
        program_id,
    )[0]


def get_combined_vault_address(program_id: Pubkey) -> Pubkey:
    return Pubkey.find_program_address(
        [b"combined-vault"],
        program_id,
    )[0]


def get_zeta_vault_address(program_id: Pubkey, mint: Pubkey) -> Pubkey:
    return Pubkey.find_program_address(
        [b"zeta-vault", bytes(mint)],
        program_id,
    )[0]


def get_combined_socialized_loss_address(program_id: Pubkey) -> Pubkey:
    return Pubkey.find_program_address(
        [b"combined-socialized-loss"],
        program_id,
    )[0]


def get_associated_token_address(authority: Pubkey, mint: Pubkey) -> Pubkey:
    return Pubkey.find_program_address(
        [bytes(authority), bytes(TOKEN_PROGRAM_ID), bytes(mint)],
        ASSOCIATED_TOKEN_PROGRAM_ID,
    )[0]


def get_serum_authority_address(program_id: Pubkey) -> Pubkey:
    return Pubkey.find_program_address(
        [b"serum"],
        program_id,
    )[0]


def get_open_orders_map_address(program_id: Pubkey, open_orders: Pubkey) -> Pubkey:
    return Pubkey.find_program_address(
        [b"cross-open-orders-map", bytes(open_orders)],
        program_id,
    )[0]


def get_mint_authority_address(program_id: Pubkey) -> Pubkey:
    return Pubkey.find_program_address(
        [b"mint-auth"],
        program_id,
    )[0]


def get_underlying_mint_address(asset: Asset, network: Network) -> Pubkey:
    if asset in MINTS:
        return MINTS[asset]
    if asset in FLEXIBLE_MINTS[network]:
        return FLEXIBLE_MINTS[network][asset]
    raise Exception("Underlying mint does not exist!")
