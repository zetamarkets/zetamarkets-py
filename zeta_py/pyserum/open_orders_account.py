from __future__ import annotations

from typing import NamedTuple, Type, TypeVar

from solana.rpc.api import Client
from solders.instruction import Instruction
from solders.pubkey import Pubkey
from solders.system_program import CreateAccountParams, create_account

from ._layouts.open_orders import OPEN_ORDERS_LAYOUT
from .instructions import DEFAULT_DEX_PROGRAM_ID

# from .utils import load_bytes_data


class ProgramAccount(NamedTuple):
    public_key: Pubkey
    data: bytes
    is_executablable: bool
    lamports: int
    owner: Pubkey


_T = TypeVar("_T", bound="_OpenOrdersAccountCore")


class _OpenOrdersAccountCore:  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        address: Pubkey,
        market: Pubkey,
        owner: Pubkey,
        base_token_free: int,
        base_token_total: int,
        quote_token_free: int,
        quote_token_total: int,
        free_slot_bits: int,
        is_bid_bits: int,
        orders: list[int],
        client_ids: list[int],
    ):
        self.address = address
        self.market = market
        self.owner = owner
        self.base_token_free = base_token_free
        self.base_token_total = base_token_total
        self.quote_token_free = quote_token_free
        self.quote_token_total = quote_token_total
        self.free_slot_bits = free_slot_bits
        self.is_bid_bits = is_bid_bits
        self.orders = orders
        self.client_ids = client_ids

    @classmethod
    def from_bytes(cls: Type[_T], address: Pubkey, buffer: bytes) -> _T:
        open_order_decoded = OPEN_ORDERS_LAYOUT.parse(buffer)
        if not open_order_decoded.account_flags.open_orders or not open_order_decoded.account_flags.initialized:
            raise Exception("Not an open order account or not initialized.")

        return cls(
            address=address,
            market=Pubkey(open_order_decoded.market),
            owner=Pubkey(open_order_decoded.owner),
            base_token_free=open_order_decoded.base_token_free,
            base_token_total=open_order_decoded.base_token_total,
            quote_token_free=open_order_decoded.quote_token_free,
            quote_token_total=open_order_decoded.quote_token_total,
            free_slot_bits=int.from_bytes(open_order_decoded.free_slot_bits, "little"),
            is_bid_bits=int.from_bytes(open_order_decoded.is_bid_bits, "little"),
            orders=[int.from_bytes(order, "little") for order in open_order_decoded.orders],
            client_ids=open_order_decoded.client_ids,
        )


# class OpenOrdersAccount(_OpenOrdersAccountCore):
#     @classmethod
#     def load(cls, conn: Client, address: str) -> OpenOrdersAccount:
#         addr_pub_key = Pubkey(address)
#         bytes_data = load_bytes_data(addr_pub_key, conn)
#         return cls.from_bytes(addr_pub_key, bytes_data)


# def make_create_account_instruction(
#     owner_address: Pubkey,
#     new_account_address: Pubkey,
#     lamports: int,
#     program_id: Pubkey = DEFAULT_DEX_PROGRAM_ID,
# ) -> Instruction:
#     return create_account(
#         CreateAccountParams(
#             from_pubkey=owner_address,
#             new_account_pubkey=new_account_address,
#             lamports=lamports,
#             space=OPEN_ORDERS_LAYOUT.sizeof(),
#             program_id=program_id,
#         )
#     )
