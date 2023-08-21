from borsh_construct import CStruct, I64, U64


SYSTEM_CLOCK_LAYOUT = CStruct(
    "slot" / U64,
    "epoch_start_timestamp" / I64,
    "epoch" / U64,
    "leader_schedule_epoch" / U64,
    "unix_timestamp" / I64,
)