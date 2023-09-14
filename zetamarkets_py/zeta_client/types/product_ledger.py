from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container

from . import order_state, position


class ProductLedgerJSON(typing.TypedDict):
    position: position.PositionJSON
    order_state: order_state.OrderStateJSON


@dataclass
class ProductLedger:
    layout: typing.ClassVar = borsh.CStruct(
        "position" / position.Position.layout,
        "order_state" / order_state.OrderState.layout,
    )
    position: position.Position
    order_state: order_state.OrderState

    @classmethod
    def from_decoded(cls, obj: Container) -> "ProductLedger":
        return cls(
            position=position.Position.from_decoded(obj.position),
            order_state=order_state.OrderState.from_decoded(obj.order_state),
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "position": self.position.to_encodable(),
            "order_state": self.order_state.to_encodable(),
        }

    def to_json(self) -> ProductLedgerJSON:
        return {
            "position": self.position.to_json(),
            "order_state": self.order_state.to_json(),
        }

    @classmethod
    def from_json(cls, obj: ProductLedgerJSON) -> "ProductLedger":
        return cls(
            position=position.Position.from_json(obj["position"]),
            order_state=order_state.OrderState.from_json(obj["order_state"]),
        )
