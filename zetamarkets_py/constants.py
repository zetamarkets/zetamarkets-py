from solana.rpc import commitment
from solders.address_lookup_table_account import AddressLookupTableAccount
from solders.pubkey import Pubkey

from zetamarkets_py.types import Asset, Network

ZETA_PID = {
    # Network.LOCALNET: Pubkey.from_string("BG3oRikW8d16YjUEmX3ZxHm9SiJzrGtMhsSR8aCw1Cd7"),
    Network.DEVNET: Pubkey.from_string("BG3oRikW8d16YjUEmX3ZxHm9SiJzrGtMhsSR8aCw1Cd7"),
    Network.MAINNET: Pubkey.from_string("ZETAxsqBRek56DhiGXrn75yj2NHU3aYUnxvHXpkf3aD"),
}

DEX_PID = {
    # Network.LOCALNET: Pubkey.from_string("5CmWtUihvSrJpaUrpJ3H1jUa9DRjYz4v2xs6c3EgQWMf"),
    Network.DEVNET: Pubkey.from_string("5CmWtUihvSrJpaUrpJ3H1jUa9DRjYz4v2xs6c3EgQWMf"),
    Network.MAINNET: Pubkey.from_string("zDEXqXEG7gAyxb1Kg9mK5fPnUdENCGKzWrM21RMdWRq"),
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

# DEX
BASE_MINT_DECIMALS = 0
QUOTE_MINT_DECIMALS = 6

BLOCKHASH_COMMITMENT = commitment.Finalized

ZETA_LUT = {
    # Network.LOCALNET: None,
    Network.DEVNET: AddressLookupTableAccount(
        key=Pubkey.from_string("3a2We1NeafvL9Hnx41ZXZQRjxLxr8M6MnjneZZjJDRfZ"),
        addresses=[
            Pubkey.from_string("9VddCF6iEyZbjkCQ4g8VJpjEtuLsgmvRCc6LQwAvXigC"),
            Pubkey.from_string("BditorsEXbVw6R8Woe6JhoyXC1beJCixYt57UMKuiwQi"),
            Pubkey.from_string("5CmWtUihvSrJpaUrpJ3H1jUa9DRjYz4v2xs6c3EgQWMf"),
            Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
            Pubkey.from_string("7m134nU79ezr3b7jYSehnhto94AvSP4yexa3Wdhxff99"),
            Pubkey.from_string("SysvarRent111111111111111111111111111111111"),
            Pubkey.from_string("HEvSKofvBgfaexv23kMabbYqxasxU3mQ4ibBMEmJWHny"),
            Pubkey.from_string("J83w4HKfqxwcq3BEMMkPFSppX3gqekLyLJBexebFVkix"),
            Pubkey.from_string("99B2bTijsU6f1GCT73HmdR7HCFFjGMBcPZY6jZ96ynrR"),
            Pubkey.from_string("HovQMDrbAgAYPCmHVSrezcSmkMtXSSUsLDFANExrZh2J"),
            Pubkey.from_string("6PxBx93S8x3tno1TsFZwT5VqP8drrRCbCXygEXYNkFJe"),
            Pubkey.from_string("EdVCmQ9FSPcVe5YySXDPCRmc8aDQLKJ9xvYBMZPie1Vw"),
            Pubkey.from_string("669U43LNHx7LsVj95uYksnhXUfWKDsdzVqev3V4Jpw3P"),
            Pubkey.from_string("5d2QJ6u2NveZufmJ4noHja5EHs3Bv1DUMPLG5xfasSVs"),
            Pubkey.from_string("11111111111111111111111111111111"),
            Pubkey.from_string("5SSkXsEKQepHHAewytPVwdej4epN1nxgLVM84L4KXgy7"),
            Pubkey.from_string("11111111111111111111111111111111"),
            Pubkey.from_string("JB43m9cTZVb4LcEfBA1Bf49nz4cod2Xt5i2HRAAMQvdo"),
            Pubkey.from_string("6YcgjoTUTeafyFC5C6vgFCVoM69qgpj966PhCojwiS4Z"),
            Pubkey.from_string("qjoUa8fC1DjsnwVwUCJQcVDJVYUhAnrqz3B9FSxVPAm"),
            Pubkey.from_string("5kSQn4o4S4mRR48sLZ5kijvCjnnD4NbwPqaBaQYvC6wk"),
            Pubkey.from_string("7Nm1pAysuk38D6uiU83wXfegzruqohVNwUippwSZNx71"),
            Pubkey.from_string("V6Y9bCVTTwjBDYAJ6ixMWWFK7RKZcQeUcpufZaM3DDB"),
            Pubkey.from_string("5yiNVYs4xpC26yY9K3DYTRvdFkdjBSnkyeSAA3Huf4Q2"),
            Pubkey.from_string("CjwQEszLimhf3FkwqcB5rGppZS4ADLeCmtPvcRefv5qi"),
            Pubkey.from_string("HM95yakZehLhBkVx2a5mwzTTf4UeqfDeSno17NstQKzd"),
            Pubkey.from_string("GHSuFYv8SicmVC3c5DeKgFhjDdegNH552srPFufFysDU"),
            Pubkey.from_string("HT9nmiVtAbLp3GFtfrhGCPGz1tBcvHyFz43pf8rtDArs"),
            Pubkey.from_string("J8yPaachUYRo1qbtdvkQU6Ee2vzEt3JiYRncwkfoB3iZ"),
            Pubkey.from_string("D9mSSsfXp9SUrSCrmPA8sDJ42GMn65Z5tZr9wtwbHEBy"),
            Pubkey.from_string("AYUthyJDg6mvBWjGfEGYcnjRbw3TZbYCnEQyqUiPyw57"),
            Pubkey.from_string("D7g6CGNVzebzzH1t98tBJKjA6FokiuXKaX3QVF53ZqcC"),
            Pubkey.from_string("DLzvYrHo4bT8PoSwhxDWKhH9ZNsnPbE5cgCx1coCpeR6"),
            Pubkey.from_string("2CtvLehungAsAcYhqnhLEoxuTaM5WqHrycn2YNpmnC4z"),
            Pubkey.from_string("9bGCvH7MwfwyKuNzgfGRXU8sW9jWtFMJf4FmUsQxk13Z"),
            Pubkey.from_string("8pQvXjUf9qq6Lsk9WE8tqtPXxgf4Yav32DneQDLaJr9k"),
            Pubkey.from_string("Gxc3KYEgasnSbevj9GnzwDk2i82BRHACQ8HWtgA1VXUk"),
            Pubkey.from_string("2fgyaTU1BeSk3LWbEh9p3D1H29hEt1wyy8qchKNGxBhg"),
            Pubkey.from_string("FDXX8a9asz32d6EteL6Wnra71YjT45TuGHy8Y8dPntbq"),
            Pubkey.from_string("JCk2bU5xNDUBk55W5BoEgNeKqssXdj15vLqhuzQEEiCU"),
            Pubkey.from_string("HYv5Vb7G3849dYN8RG2pQx7awXiEk3nE9F3AGWnedffs"),
            Pubkey.from_string("5RDbC6wYGhc1AjCCArwggtbAyPUse6yMcq3fgSzZqY5E"),
            Pubkey.from_string("2CCypxRdB6tCackur4De72ZSnsNcicfSjWYZwAcVzEZ9"),
            Pubkey.from_string("J5e19jEz625k7K5K3yinpMoHNzznv8smCemvKAYCWLMH"),
            Pubkey.from_string("7QDHQhNjMzuKKk9T5vsdZ5hTfLu2P1pUGk2TKJKFd8hn"),
            Pubkey.from_string("DYXqC6UGPwsz5W3jaFAJtpbBsvJpBSi34W6cMn7ZiL6m"),
            Pubkey.from_string("2YBnvgCAh6WcXrs5Wz2uhi2nMuEVDXE28mQ5AmHjRaJQ"),
            Pubkey.from_string("wkTZtYAo75bpqqy2J5A6emsLK69EYG8otvJipAbiJF9"),
            Pubkey.from_string("FXgqEhVGX82dsyKMAgR2JCRaC9FNH4ih611bJftmD3tG"),
            Pubkey.from_string("B3iV7Y5S9Xqu6cTECpBCAHtL2nwvZntD2d7F1zbpbQc3"),
            Pubkey.from_string("J7E7gv1iofWZg8b37RVnKy2i1FAnCRBvgk54YpVtZ4WS"),
            Pubkey.from_string("EPf7hymYW7bnwiBYGTRF4Ji2jJ2yTdn4XMTpR6N4zsGA"),
            Pubkey.from_string("DNXXx5yaQm6Kd4embzqHW94kjjypxzZ8zCQthMvmHDq1"),
            Pubkey.from_string("6VUvm4i9T2w9CXzLKaUDNTZ4KmK3xKCWz95xEoyKjjE8"),
            Pubkey.from_string("Dd3K16uKGDa2Xc83NYQE9jpcMNZ9GRqmqggkkpXo4x4y"),
            Pubkey.from_string("FUsWmTk7PaEvXCHFZH6XMbimgqbVkiKPXd35tHWo5vm4"),
            Pubkey.from_string("Fc7FU4VATyYuvkhp6MuPUHWYHC9EBFknN5TTHs3wGjyn"),
            Pubkey.from_string("CW5zwzmhQn9Pqjzxjdzr4AdmVSoehBQ2RdfyppU37uDE"),
            Pubkey.from_string("Cvqd7RtB4bf9SJpmWwNd6GVXvtAX4m4DtSR5u2XahTQf"),
            Pubkey.from_string("67XFnD7YuBfd52qPrD5FuasrQW21jLd4jxnDfozyeSvx"),
            Pubkey.from_string("3H7nvQAJBzsXVPEyzpuL4kB3tPz5rs7XVxuxVLV7YDNy"),
            Pubkey.from_string("JEDqstU8skdUF6bGsMzZaa17Tfuf3asxQPuLVXqmWqyt"),
            Pubkey.from_string("2Ux9NzgadfR2PHyrSauzWLaNr99syCRKriwF4mnEqPUv"),
            Pubkey.from_string("4NEK9db8v9PZC5RnzSEh596jNwfRMH6QcQQG2ZhqkStb"),
            Pubkey.from_string("2mRZPMv67hz1QocPQ7JS5sEp8uD9u9TfdLoZzf8LciiZ"),
            Pubkey.from_string("G3ytGgn7MzH5DpLCSBshkV4xQe1G4JBbTu7c9CCWA9U"),
            Pubkey.from_string("J5t2VsFLSXGTaA1o2qCujduJ9dnHLok9QhYUroN2fc6X"),
            Pubkey.from_string("6UEwXk5ixtC6rDJG7X2X6MLNwiAyjGZZyN6L1JG63n4H"),
            Pubkey.from_string("FkHx7byyFDGheXCcmVxdavTDteotaDJZk8DBNBm2Maeb"),
            Pubkey.from_string("zXEzviQpq8u89oAKdU7r3vHHxXpxC2547AoLzxCKSJ3"),
            Pubkey.from_string("93DGPpMR6w3gqbrbpZrChqw8vihgHibmdejB4Q1p4DbP"),
            Pubkey.from_string("Ag4cqXXAAxa9NCZcFgQuoeDkvtSbxwe6qaEfjw4aRnUH"),
        ],
    ),
    Network.MAINNET: AddressLookupTableAccount(
        key=Pubkey.from_string("7Xjap9vrWush2kY3HV691U2R3b4CZgyafWcCDJiZ1zVR"),
        addresses=[
            Pubkey.from_string("8eExPiLp47xbSDYkbuem4qnLUpbLTfZBeFuEJoh6EUr2"),
            Pubkey.from_string("BbKFezrmKD83PeVh74958MzgFAue1pZptipSNLz5ccpk"),
            Pubkey.from_string("zDEXqXEG7gAyxb1Kg9mK5fPnUdENCGKzWrM21RMdWRq"),
            Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
            Pubkey.from_string("AVNMK6wiGfppdQNg9WKfMRBXefDPGZFh2f3o1fRbgN8n"),
            Pubkey.from_string("SysvarRent111111111111111111111111111111111"),
            Pubkey.from_string("HEvSKofvBgfaexv23kMabbYqxasxU3mQ4ibBMEmJWHny"),
            Pubkey.from_string("H6ARHf6YXhGYeQfUzQNGk6rDNnLBQKrenN712K4AQJEG"),
            Pubkey.from_string("CH31Xns5z3M1cTAbKW34jcxPPciazARpijcHj9rxtemt"),
            Pubkey.from_string("GVXRSBjFk6e6J3NbVPXohDJetcTjaeeuykUpbQF8UoMU"),
            Pubkey.from_string("Cv4T27XbjVoKUYwP72NQQanvZeA7W4YF9L4EnYT9kx5o"),
            Pubkey.from_string("JBu1AL4obBcCMqKBBxhpWCNUt136ijcuMZLFvTP7iWdB"),
            Pubkey.from_string("716hFAECqotxcXcj8Hs8nr7AG6q9dBw2oX3k3M8V7uGq"),
            Pubkey.from_string("FNNvb1AFDnDVPkocEri8mWbJ1952HQZtFLuwPiUjSJQ"),
            Pubkey.from_string("11111111111111111111111111111111"),
            Pubkey.from_string("5HRrdmghsnU3i2u5StaKaydS7eq3vnKVKwXMzCNKsc4C"),
            Pubkey.from_string("11111111111111111111111111111111"),
            Pubkey.from_string("JE6d41JRokZAMUEAznV8JP4h7i6Ain6CyJrQuweRipFU"),
            Pubkey.from_string("EaNR74nCjrYyNDsuoWmq19pH76QSd1nuTzvJSr3RDQ6x"),
            Pubkey.from_string("3rjBffJkFa9zdGr9xmTVxF3y6nL6iL1pASVzym7s5FGr"),
            Pubkey.from_string("HcjrQKnbqKJuxHDLNM9LJPyxcQs237waNZXW7RwgvAps"),
            Pubkey.from_string("Ec4xsLLgLc4wM5c19ZSvazE7M9Rtk2T6RzddNcSQKYGu"),
            Pubkey.from_string("BEjGhNFnKT5weGtpBoFs5Y1mDN47Ntvag5aMV59nZRpk"),
            Pubkey.from_string("CHBUBfU3zscTNsihdK3x44TbpTza1hwcsTUaZfk751b5"),
            Pubkey.from_string("GYm6qTFwkGJx2ywetEuYrjHjhzVFCM2TwayyqS1HUPLG"),
            Pubkey.from_string("7aXkF7AZE2D3h128eNJ7VVp72HCV1izjKFsJ8uNWtCFN"),
            Pubkey.from_string("BKt2FdgBahn77joeawhNidswFxfgasPYCHWghRL4AKBR"),
            Pubkey.from_string("2ZLdhFsrkAtdn9Kud4SZvqchQFvn5jVCHUdJ83vumKyR"),
            Pubkey.from_string("J5DTCqRAjX1FyzoP2A2HVmmaXuG971HJ8X1Z8Rvvd8uT"),
            Pubkey.from_string("6JSdqUr24mBt4MCQrZHRoSfeZbjgALx4MQunZwD8Uarg"),
            Pubkey.from_string("4K1zxqAZn7bGAPN26W5mUaHrLMSpCk45gT4qVXwmfh39"),
            Pubkey.from_string("8JSbFw4YT3bzpbbHs1wKmRCSAmKucAba7XSUWj1p8xK5"),
            Pubkey.from_string("483SmqGQVxw3WDwcewMYHqC3Mu7ENxfTQJQtTR3ttpi7"),
            Pubkey.from_string("DbzL5mT4nBaxuAs8ti4UeT2qougRBdujxa7GhLndM5Jz"),
            Pubkey.from_string("7M9xhY2ARnrkCaBK5SNM3Lyd3FdbTu2EWBwG4TQcqpsv"),
            Pubkey.from_string("5mvaZWcZa4gB3JZptZuFAJnmDFfo1JovhqTkkfEcsryD"),
            Pubkey.from_string("DboTtkWW3KPvT14fag8N6iDUyDXaT8FeBszGV9xdfBx2"),
            Pubkey.from_string("DhMH8oRQoAAb6poHVsvCqq3NCMj6aKUH2tGQG5Lo4bCg"),
            Pubkey.from_string("63DZkAzoDXmzGzn9esoWSYpMLo4YB9oPHXreHKwuu4HA"),
            Pubkey.from_string("J8x6y5G7GmTkuKTbbCAnfhn72vaUU2qsB6je9oKFigHM"),
            Pubkey.from_string("A7D8zuxAmtui3XKz2VcxthAZ5HuwLbN74rrDapMJ3Z5d"),
            Pubkey.from_string("CzK26LWpoU9UjSrZkVu97oZj63abJrNv1zp9Hy2zZdy5"),
            Pubkey.from_string("CaqN8gomPEB1My2czRhetrj5ESKP3VRR3kwKhXtGxohG"),
            Pubkey.from_string("4oAjuVLt5N9au2X3bhYLSi9LRqtk4caBvSPQRwhXuEKP"),
            Pubkey.from_string("9YVE9r9cHFZNwm91p3Js8NBWVznesLSM8FZyswG2MG1B"),
            Pubkey.from_string("DecjLCYjb7jdDp2UqA2MS4xjgDjZfvdgMjvkRW7oWs9L"),
            Pubkey.from_string("8SH6uJe5rV13APZFQvkGdXPwTyeiLv67XTnv3EeYff3B"),
            Pubkey.from_string("DhWWXYK2DSnCdK5rkAxJBkGb1SBR49RHpfHj2u1vobCJ"),
            Pubkey.from_string("5Ehp2LtTRmjug39GphXhFEeguz7hGeg41N1U49wU8Kov"),
            Pubkey.from_string("2Stzi7XE3btUQXaauTVB9brPAtPmGnrEDSJmp3w5VY2j"),
            Pubkey.from_string("J6feTwcYDydW71Dp9qgfW7Mu9qk3qDRrDZAWV8NMVh9x"),
            Pubkey.from_string("EPf7hymYW7bnwiBYGTRF4Ji2jJ2yTdn4XMTpR6N4zsGA"),
            Pubkey.from_string("DNXXx5yaQm6Kd4embzqHW94kjjypxzZ8zCQthMvmHDq1"),
            Pubkey.from_string("6VUvm4i9T2w9CXzLKaUDNTZ4KmK3xKCWz95xEoyKjjE8"),
            Pubkey.from_string("Dd3K16uKGDa2Xc83NYQE9jpcMNZ9GRqmqggkkpXo4x4y"),
            Pubkey.from_string("GqCVQuGMf8YkiaJkSrD98D3WZxFfktcKzAwdBEQsx1th"),
            Pubkey.from_string("2BpEtArGNotp97DjVKwhYZ86WEq2Y5bLtGGDvicuJ9br"),
            Pubkey.from_string("6nkbQueQanrsg2JVvqoZ6zPuZsiL3oLmTk7xgEpRAirD"),
            Pubkey.from_string("7T1qeETZ6ZpbKJ7wmrWoxhewLaJRW9H4EgMnR1tgHYRQ"),
            Pubkey.from_string("6S6WYL1mQFmVxsf3ft5MEH8hzxJA1LcUDzgwdJDj3yxc"),
            Pubkey.from_string("GuNWJSV4k95FZdwhAcjdaPGGoh9cArc27yV4P54QwWdg"),
            Pubkey.from_string("J18LXTGe2cPgpLKSCwXiG6tYkjcqEiaMUznM19Q8faVL"),
            Pubkey.from_string("gP91avgCrV9KB2ATgRtMCNN2AN7oU9hK1frENe17QkR"),
            Pubkey.from_string("DUtwwtnNBzpPTnzUiz23vqH93gd1qwEzGisyC5bLwCBv"),
            Pubkey.from_string("A4SayHehmafd6DNjrzY3L9ddQEGw4UHV3LMcKfmyPcMT"),
            Pubkey.from_string("8if1NcDaif8dxM3Ct6rRTQEj9GFwukadU1MDQHqCnw9h"),
            Pubkey.from_string("GnSRgncxFbtxqZ4HmfnF6daCmgkc8tuQz9i37hUmwV5t"),
            Pubkey.from_string("6JjDgGzqzU6Az7ZmTARAvBSwBxfXsqbVG3Rc9JGU9i4L"),
            Pubkey.from_string("GQXdvh4dHvENTFi2CfVrh77aQD1Y6V7HMNYNCuvgbSuc"),
            Pubkey.from_string("EC2PCjwcuBBFHp6gpAKa3kdpLVrQxdy7kgr7p4wPy8Vw"),
            Pubkey.from_string("7j1N5UiXLFxaxFWq5tzZc5R3sjPHcF7jqfHJgAtE74q8"),
            Pubkey.from_string("Eqt3anUy8nqDvzJaNvWvqBM32Ln4UUnLkfvdd9Ztfj81"),
        ],
    ),
}
