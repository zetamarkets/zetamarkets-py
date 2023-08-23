from solana.rpc import commitment
from solana.rpc.types import TxOpts
from solders.pubkey import Pubkey

from zeta_py.types import Asset, Network

ZETA_PID = {
    # Network.LOCALNET: Pubkey.from_string("BG3oRikW8d16YjUEmX3ZxHm9SiJzrGtMhsSR8aCw1Cd7"),
    Network.DEVNET: Pubkey.from_string("BG3oRikW8d16YjUEmX3ZxHm9SiJzrGtMhsSR8aCw1Cd7"),
    Network.MAINNET: Pubkey.from_string("ZETAxsqBRek56DhiGXrn75yj2NHU3aYUnxvHXpkf3aD"),
}

# Asset keys are wormhole from mainnet.
MINTS = {
    Asset.SOL: Pubkey.from_string("So11111111111111111111111111111111111111112"),
    Asset.BTC: Pubkey.from_string("qfnqNqs3nCAHjnyCgLRDbBtq4p2MtHZxw8YjSyYhPoL"),
    Asset.ETH: Pubkey.from_string("FeGn77dhg1KXRRFeSwwMiykZnZPw5JXW6naf2aQgZDQf"),
}

# These are generated flexible PDAs and aren't reflective of an spl token mint.
FLEXIBLE_MINTS = {
    Network.LOCALNET: {
        Asset.APT: Pubkey.from_string("FbfkphUHaAd7c27RqhzKBRAPX8T5AzFBH259sbGmNuvG"),
        Asset.ARB: Pubkey.from_string("w8h6r5ogLihfuWeCA1gs7boxNjzbwWeQbXMB3UATaC6"),
    },
    Network.DEVNET: {
        Asset.APT: Pubkey.from_string("FbfkphUHaAd7c27RqhzKBRAPX8T5AzFBH259sbGmNuvG"),
        Asset.ARB: Pubkey.from_string("w8h6r5ogLihfuWeCA1gs7boxNjzbwWeQbXMB3UATaC6"),
    },
    Network.MAINNET: {
        Asset.APT: Pubkey.from_string("8z8oShLky1PauW9hxv6AsjnricLqoK9MfmNZJDQNNNPr"),
        Asset.ARB: Pubkey.from_string("Ebd7aUFu3rtsZruCzTnG4tjBoxaJdWT8S3t4yC8hVpbo"),
    },
}

# ZETAGROUP_PUBKEY_ASSET_MAP = {
#     # Network.LOCALNET: {
#     #     "HRobFXQ2HQvSgCLq2CU9ZG3DR2BxRaAffw5SvdNnvk97": Asset.SOL,
#     #     "CcLF7qQbgRQqUDmQeEkTSP2UbX82N9G91THjV5uRGCMW": Asset.BTC,
#     #     "8Ccch7LW5hd5j2NW8HdhUbDqB1yUN4dULVMNNHtfbPbV": Asset.ETH,
#     #     "5QyPHfnRttz4Tq7W7U5XEpKpvj7g3FTvMpE1BzL9w2Qi": Asset.APT,
#     #     "4fecsFCi8Tx4aFxvc8rAYT74RBmknQ3kqidZTejoqiw7": Asset.ARB,
#     # },
#     Network.DEVNET: {
#         "HRobFXQ2HQvSgCLq2CU9ZG3DR2BxRaAffw5SvdNnvk97": Asset.SOL,
#         "CcLF7qQbgRQqUDmQeEkTSP2UbX82N9G91THjV5uRGCMW": Asset.BTC,
#         "8Ccch7LW5hd5j2NW8HdhUbDqB1yUN4dULVMNNHtfbPbV": Asset.ETH,
#         "5QyPHfnRttz4Tq7W7U5XEpKpvj7g3FTvMpE1BzL9w2Qi": Asset.APT,
#         "4fecsFCi8Tx4aFxvc8rAYT74RBmknQ3kqidZTejoqiw7": Asset.ARB,
#     },
#     Network.MAINNET: {
#         "CoGhjFdyqzMFr5xVgznuBjULvoFbFtNN4bCdQzRArNK2": Asset.SOL,
#         "5XC7JWvLGGds4tjaawgY8FwMdotUb5rrEUmxcmyp5ZiW": Asset.BTC,
#         "HPnqfiRSVvuBjfHN9ah4Kecb6J9et2UTnNgUwtAJdV26": Asset.ETH,
#         "D19K6rrppbWAFa4jE1DJUStPnr7cSrqKk5TruGqfc5Ns": Asset.APT,
#         "CU6pPA2E2yQFqMzZKrFCmfjrSBEc6GxfmFrSqpqazygu": Asset.ARB,
#     },
# }

USDC_MINT = {
    #   Network.LOCALNET: Pubkey.from_string("6PEh8n3p7BbCTykufbq1nSJYAZvUp6gSwEANAs1ZhsCX"),
    Network.DEVNET: Pubkey.from_string("6PEh8n3p7BbCTykufbq1nSJYAZvUp6gSwEANAs1ZhsCX"),
    Network.MAINNET: Pubkey.from_string("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"),
}

DEX_PID = {
    # Network.LOCALNET: Pubkey.from_string("5CmWtUihvSrJpaUrpJ3H1jUa9DRjYz4v2xs6c3EgQWMf"),
    Network.DEVNET: Pubkey.from_string("5CmWtUihvSrJpaUrpJ3H1jUa9DRjYz4v2xs6c3EgQWMf"),
    Network.MAINNET: Pubkey.from_string("zDEXqXEG7gAyxb1Kg9mK5fPnUdENCGKzWrM21RMdWRq"),
}

CHAINLINK_PID = Pubkey.from_string("HEvSKofvBgfaexv23kMabbYqxasxU3mQ4ibBMEmJWHny")

MAX_SETTLE_AND_CLOSE_PER_TX = 4
MAX_CANCELS_PER_TX = 3
MAX_CANCELS_PER_TX_LUT = 13
MAX_GREEK_UPDATES_PER_TX = 20
MAX_SETTLEMENT_ACCOUNTS = 20
MAX_FUNDING_ACCOUNTS = 20
MAX_REBALANCE_ACCOUNTS = 18
MAX_SETTLE_ACCOUNTS = 5
MAX_ZETA_GROUPS = 20
MAX_MARGIN_AND_SPREAD_ACCOUNTS = 20
MAX_SET_REFERRALS_REWARDS_ACCOUNTS = 12
MAX_INITIALIZE_MARKET_TIF_EPOCH_CYCLE_IXS_PER_TX = 15
MARKET_INDEX_LIMIT = 18
MARKET_LOAD_LIMIT = 12
MAX_MARKETS_TO_FETCH = 50

MIN_LOT_SIZE = 0.001
PERP_MARKET_ORDER_SPOT_SLIPPAGE = 0.02

# This is the most we can load per iteration without
# hitting the rate limit.
MARKET_LOAD_LIMIT = 12

# Numbers represented in BN are generally fixed point integers with precision of 6.
PLATFORM_PRECISION = 6
MARGIN_PRECISION = 8
POSITION_PRECISION = 3
TICK_SIZE = 100

DEFAULT_ORDER_TAG = "SDK"

MAX_POSITION_MOVEMENTS = 10
BPS_DENOMINATOR = 10_000

DEFAULT_MICRO_LAMPORTS_PER_CU_FEE = 1000


DEFAULT_COMMITMENT = commitment.Confirmed
DEFAULT_TX_OPTS = TxOpts(
    {
        "skip_preflight": False,
        "preflight_commitment": DEFAULT_COMMITMENT,
    }
)
