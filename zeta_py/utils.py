from zeta_py import constants

"""
Converts a native lot size where 1 unit = 0.001 lots to human readable decimal
@param amount
"""


def convert_native_lot_size_to_decimal(amount: int) -> float:
    return amount / 10**constants.POSITION_PRECISION
