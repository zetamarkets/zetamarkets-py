from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class InitializeMarketNodeArgsJSON(typing.TypedDict):
    nonce: int
    index: int


@dataclass
class InitializeMarketNodeArgs:
    layout: typing.ClassVar = borsh.CStruct("nonce" / borsh.U8, "index" / borsh.U8)
    nonce: int
    index: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "InitializeMarketNodeArgs":
        return cls(nonce=obj.nonce, index=obj.index)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"nonce": self.nonce, "index": self.index}

    def to_json(self) -> InitializeMarketNodeArgsJSON:
        return {"nonce": self.nonce, "index": self.index}

    @classmethod
    def from_json(cls, obj: InitializeMarketNodeArgsJSON) -> "InitializeMarketNodeArgs":
        return cls(nonce=obj["nonce"], index=obj["index"])
