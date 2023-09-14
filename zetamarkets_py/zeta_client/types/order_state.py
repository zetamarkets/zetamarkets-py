from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container


class OrderStateJSON(typing.TypedDict):
    closing_orders: int
    opening_orders: list[int]


@dataclass
class OrderState:
    layout: typing.ClassVar = borsh.CStruct("closing_orders" / borsh.U64, "opening_orders" / borsh.U64[2])
    closing_orders: int
    opening_orders: list[int]

    @classmethod
    def from_decoded(cls, obj: Container) -> "OrderState":
        return cls(closing_orders=obj.closing_orders, opening_orders=obj.opening_orders)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "closing_orders": self.closing_orders,
            "opening_orders": self.opening_orders,
        }

    def to_json(self) -> OrderStateJSON:
        return {
            "closing_orders": self.closing_orders,
            "opening_orders": self.opening_orders,
        }

    @classmethod
    def from_json(cls, obj: OrderStateJSON) -> "OrderState":
        return cls(closing_orders=obj["closing_orders"], opening_orders=obj["opening_orders"])
