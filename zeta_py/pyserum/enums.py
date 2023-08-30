"""Serum specific enums."""



# class Side(Enum):
#     """Side of the orderbook to trade."""

#     Bid = 0
#     """"""
#     Ask = 1
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
