from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from spl.token.constants import WRAPPED_SOL_MINT

from .utils import parse_bytes_data, parse_mint_decimals, parse_multiple_bytes_data


async def load_bytes_data(addr: Pubkey, conn: AsyncClient) -> bytes:
    res = await conn.get_account_info(addr)
    return parse_bytes_data(res)


async def load_multiple_bytes_data(addrs: list[Pubkey], conn: AsyncClient) -> list[bytes]:
    res = await conn.get_multiple_accounts(addrs)
    return parse_multiple_bytes_data(res)


async def get_mint_decimals(conn: AsyncClient, mint_pub_key: Pubkey) -> int:
    """Get the mint decimals for a token mint"""
    if mint_pub_key == WRAPPED_SOL_MINT:
        return 9

    bytes_data = await load_bytes_data(mint_pub_key, conn)
    return parse_mint_decimals(bytes_data)
