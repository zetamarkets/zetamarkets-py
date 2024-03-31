from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class AnchorDecimalJSON(typing.TypedDict):
    flags: int
    hi: int
    lo: int
    mid: int


@dataclass
class AnchorDecimal:
    layout: typing.ClassVar = borsh.CStruct("flags" / borsh.U32, "hi" / borsh.U32, "lo" / borsh.U32, "mid" / borsh.U32)
    flags: int
    hi: int
    lo: int
    mid: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "AnchorDecimal":
        return cls(flags=obj.flags, hi=obj.hi, lo=obj.lo, mid=obj.mid)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"flags": self.flags, "hi": self.hi, "lo": self.lo, "mid": self.mid}

    def to_json(self) -> AnchorDecimalJSON:
        return {"flags": self.flags, "hi": self.hi, "lo": self.lo, "mid": self.mid}

    @classmethod
    def from_json(cls, obj: AnchorDecimalJSON) -> "AnchorDecimal":
        return cls(flags=obj["flags"], hi=obj["hi"], lo=obj["lo"], mid=obj["mid"])


class Decimal:
    def __init__(self, flags: int, hi: int, lo: int, mid: int):
        self._flags = flags
        self._hi = hi
        self._lo = lo
        self._mid = mid
        self.SCALE_MASK = 0x00FF0000
        self.SCALE_SHIFT = 16
        self.SIGN_MASK = 0x80000000

    @classmethod
    def from_anchor_decimal(cls, decimal: AnchorDecimal) -> "Decimal":
        return cls(decimal.flags, decimal.hi, decimal.lo, decimal.mid)

    def scale(self) -> int:
        return (self._flags & self.SCALE_MASK) >> self.SCALE_SHIFT

    def is_sign_negative(self) -> bool:
        return (self._flags & self.SIGN_MASK) != 0

    def is_sign_positive(self) -> bool:
        return (self._flags & self.SIGN_MASK) == 0

    def to_bn(self):
        bytes_ = bytes(
            [
                (self._hi >> 24) & 0xFF,
                (self._hi >> 16) & 0xFF,
                (self._hi >> 8) & 0xFF,
                self._hi & 0xFF,
                (self._mid >> 24) & 0xFF,
                (self._mid >> 16) & 0xFF,
                (self._mid >> 8) & 0xFF,
                self._mid & 0xFF,
                (self._lo >> 24) & 0xFF,
                (self._lo >> 16) & 0xFF,
                (self._lo >> 8) & 0xFF,
                self._lo & 0xFF,
            ]
        )

        return -1 * int.from_bytes(bytes_, "big") if self.is_sign_negative() else int.from_bytes(bytes_, "big")

    def is_unset(self) -> bool:
        return self._hi == 0 and self._mid == 0 and self._lo == 0 and self._flags == 0

    def to_number(self) -> float:
        if self.is_unset():
            return 0.0

        scale = self.scale()
        if scale == 0:
            raise ValueError("Scale 0 is not handled.")

        bn = self.to_bn()
        # We use str because only 53 bits can be stored for floats.
        return bn / (10**scale)
