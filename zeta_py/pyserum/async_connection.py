import httpx
from solana.rpc.async_api import (  # pylint: disable=unused-import # noqa:F401
    AsyncClient as async_conn,
)

from .connection import (
    LIVE_MARKETS_URL,
    TOKEN_MINTS_URL,
    parse_live_markets,
    parse_token_mints,
)
from .market.types import MarketInfo, TokenInfo


async def get_live_markets(httpx_client: httpx.AsyncClient) -> list[MarketInfo]:
    resp = await httpx_client.get(LIVE_MARKETS_URL)
    return parse_live_markets(resp.json())


async def get_token_mints(httpx_client: httpx.AsyncClient) -> list[TokenInfo]:
    resp = await httpx_client.get(TOKEN_MINTS_URL)
    return parse_token_mints(resp.json())
