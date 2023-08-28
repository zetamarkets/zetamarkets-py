"""Serum specific enums."""

from enum import Enum

from zeta_py.zeta_client.types import side


# class Side(Enum):
#     """Side of the orderbook to trade."""

#     BID = 0
#     """"""
#     ASK = 1
#     """"""

#     def to_program_type(self) -> side.SideKind:
#         return side.from_decoded({self.name.title(): self.value})


# class OrderType(Enum):
#     """Type of order."""

#     LIMIT = 0
#     """"""
#     IOC = 1
#     """"""
#     POST_ONLY = 2
#     """"""


# class SelfTradeBehavior(Enum):
#     DECREMENT_TAKE = 0
#     CANCEL_PROVIDE = 1
#     ABORT_TRANSACTION = 2
