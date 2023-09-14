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
