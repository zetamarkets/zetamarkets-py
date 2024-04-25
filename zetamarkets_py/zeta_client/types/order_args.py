from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class OrderArgsJSON(typing.TypedDict):
    price: int
    size: int
    client_order_id: typing.Optional[int]
    tif_offset: typing.Optional[int]


@dataclass
class OrderArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "price" / borsh.U64,
        "size" / borsh.U64,
        "client_order_id" / borsh.Option(borsh.U64),
        "tif_offset" / borsh.Option(borsh.U16),
    )
    price: int
    size: int
    client_order_id: typing.Optional[int]
    tif_offset: typing.Optional[int]

    @classmethod
    def from_decoded(cls, obj: Container) -> "OrderArgs":
        return cls(
            price=obj.price,
            size=obj.size,
            client_order_id=obj.client_order_id,
            tif_offset=obj.tif_offset,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "price": self.price,
            "size": self.size,
            "client_order_id": self.client_order_id,
            "tif_offset": self.tif_offset,
        }

    def to_json(self) -> OrderArgsJSON:
        return {
            "price": self.price,
            "size": self.size,
            "client_order_id": self.client_order_id,
            "tif_offset": self.tif_offset,
        }

    @classmethod
    def from_json(cls, obj: OrderArgsJSON) -> "OrderArgs":
        return cls(
            price=obj["price"],
            size=obj["size"],
            client_order_id=obj["client_order_id"],
            tif_offset=obj["tif_offset"],
        )
