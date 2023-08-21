from construct import BitsInteger, BitsSwapped, BitStruct, Const, Flag

# We will use a bitstruct with 64 bits instead of the widebits implementation in serum-js.
ACCOUNT_FLAGS_LAYOUT = BitsSwapped(  # Swap to little endian
    BitStruct(
        "initialized" / Flag,
        "market" / Flag,
        "open_orders" / Flag,
        "request_queue" / Flag,
        "event_queue" / Flag,
        "bids" / Flag,
        "asks" / Flag,
        "disabled" / Flag,
        "closed" / Flag,
        "permissioned" / Flag,
        "crank_authority_required" / Flag,
        Const(0, BitsInteger(53)),  # zero padding bits
    )
)
