from construct import Bytes, Int8ul, Int16ul, Int64ul, Padding
from construct import Struct as cStruct

from .account_flags import ACCOUNT_FLAGS_LAYOUT

# import borsh_construct as borsh
# from anchorpy.borsh_extension import BorshPubkey


MARKET_LAYOUT = cStruct(
    Padding(5),
    "account_flags" / ACCOUNT_FLAGS_LAYOUT,
    "own_address" / Bytes(32),
    "vault_signer_nonce" / Int64ul,
    "base_mint" / Bytes(32),
    "quote_mint" / Bytes(32),
    "base_vault" / Bytes(32),
    "base_deposits_total" / Int64ul,
    "base_fees_accrued" / Int64ul,
    "quote_vault" / Bytes(32),
    "quote_deposits_total" / Int64ul,
    "quote_fees_accrued" / Int64ul,
    "quote_dust_threshold" / Int64ul,
    "request_queue" / Bytes(32),
    "event_queue" / Bytes(32),
    "bids" / Bytes(32),
    "asks" / Bytes(32),
    "base_lot_size" / Int64ul,
    "quote_lot_size" / Int64ul,
    "fee_rate_bps" / Int64ul,
    "referrer_rebate_accrued" / Int64ul,
    "open_orders_authority" / Bytes(32),
    "prune_authority" / Bytes(32),
    "consume_events_authority" / Bytes(32),
    "epoch_length" / Int16ul,
    "epoch_start_ts" / Int64ul,
    "start_epoch_seq_num" / Int64ul,
    Padding(974),
    Padding(7),
)

MINT_LAYOUT = cStruct(Padding(44), "decimals" / Int8ul, Padding(37))
