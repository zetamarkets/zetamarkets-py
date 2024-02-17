import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import BorshPubkey
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class CrossMarginAccountJSON(typing.TypedDict):
    authority: str
    delegated_pubkey: str
    balance: int
    subaccount_index: int
    nonce: int
    force_cancel_flag: bool
    account_type: types.margin_account_type.MarginAccountTypeJSON
    open_orders_nonces: list[int]
    open_orders_nonces_padding: list[int]
    rebalance_amount: int
    last_funding_deltas: list[types.anchor_decimal.AnchorDecimalJSON]
    last_funding_deltas_padding: list[types.anchor_decimal.AnchorDecimalJSON]
    product_ledgers: list[types.product_ledger.ProductLedgerJSON]
    product_ledgers_padding: list[types.product_ledger.ProductLedgerJSON]
    trigger_order_bits: int
    padding: list[int]


@dataclass
class CrossMarginAccount:
    discriminator: typing.ClassVar = b"\xf2^\x8e\x83#\xf4\x93\x1c"
    layout: typing.ClassVar = borsh.CStruct(
        "authority" / BorshPubkey,
        "delegated_pubkey" / BorshPubkey,
        "balance" / borsh.U64,
        "subaccount_index" / borsh.U8,
        "nonce" / borsh.U8,
        "force_cancel_flag" / borsh.Bool,
        "account_type" / types.margin_account_type.layout,
        "open_orders_nonces" / borsh.U8[13],
        "open_orders_nonces_padding" / borsh.U8[12],
        "rebalance_amount" / borsh.I64,
        "last_funding_deltas" / types.anchor_decimal.AnchorDecimal.layout[13],
        "last_funding_deltas_padding" / types.anchor_decimal.AnchorDecimal.layout[12],
        "product_ledgers" / types.product_ledger.ProductLedger.layout[13],
        "product_ledgers_padding" / types.product_ledger.ProductLedger.layout[12],
        "trigger_order_bits" / borsh.U128,
        "padding" / borsh.U8[1984],
    )
    authority: Pubkey
    delegated_pubkey: Pubkey
    balance: int
    subaccount_index: int
    nonce: int
    force_cancel_flag: bool
    account_type: types.margin_account_type.MarginAccountTypeKind
    open_orders_nonces: list[int]
    open_orders_nonces_padding: list[int]
    rebalance_amount: int
    last_funding_deltas: list[types.anchor_decimal.AnchorDecimal]
    last_funding_deltas_padding: list[types.anchor_decimal.AnchorDecimal]
    product_ledgers: list[types.product_ledger.ProductLedger]
    product_ledgers_padding: list[types.product_ledger.ProductLedger]
    trigger_order_bits: int
    padding: list[int]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["CrossMarginAccount"]:
        resp = await conn.get_account_info(address, commitment=commitment)
        info = resp.value
        if info is None:
            return None
        if info.owner != program_id:
            raise ValueError("Account does not belong to this program")
        bytes_data = info.data
        return cls.decode(bytes_data)

    @classmethod
    async def fetch_multiple(
        cls,
        conn: AsyncClient,
        addresses: list[Pubkey],
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.List[typing.Optional["CrossMarginAccount"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["CrossMarginAccount"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "CrossMarginAccount":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = CrossMarginAccount.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            authority=dec.authority,
            delegated_pubkey=dec.delegated_pubkey,
            balance=dec.balance,
            subaccount_index=dec.subaccount_index,
            nonce=dec.nonce,
            force_cancel_flag=dec.force_cancel_flag,
            account_type=types.margin_account_type.from_decoded(dec.account_type),
            open_orders_nonces=dec.open_orders_nonces,
            open_orders_nonces_padding=dec.open_orders_nonces_padding,
            rebalance_amount=dec.rebalance_amount,
            last_funding_deltas=list(
                map(
                    lambda item: types.anchor_decimal.AnchorDecimal.from_decoded(item),
                    dec.last_funding_deltas,
                )
            ),
            last_funding_deltas_padding=list(
                map(
                    lambda item: types.anchor_decimal.AnchorDecimal.from_decoded(item),
                    dec.last_funding_deltas_padding,
                )
            ),
            product_ledgers=list(
                map(
                    lambda item: types.product_ledger.ProductLedger.from_decoded(item),
                    dec.product_ledgers,
                )
            ),
            product_ledgers_padding=list(
                map(
                    lambda item: types.product_ledger.ProductLedger.from_decoded(item),
                    dec.product_ledgers_padding,
                )
            ),
            trigger_order_bits=dec.trigger_order_bits,
            padding=dec.padding,
        )

    def to_json(self) -> CrossMarginAccountJSON:
        return {
            "authority": str(self.authority),
            "delegated_pubkey": str(self.delegated_pubkey),
            "balance": self.balance,
            "subaccount_index": self.subaccount_index,
            "nonce": self.nonce,
            "force_cancel_flag": self.force_cancel_flag,
            "account_type": self.account_type.to_json(),
            "open_orders_nonces": self.open_orders_nonces,
            "open_orders_nonces_padding": self.open_orders_nonces_padding,
            "rebalance_amount": self.rebalance_amount,
            "last_funding_deltas": list(map(lambda item: item.to_json(), self.last_funding_deltas)),
            "last_funding_deltas_padding": list(map(lambda item: item.to_json(), self.last_funding_deltas_padding)),
            "product_ledgers": list(map(lambda item: item.to_json(), self.product_ledgers)),
            "product_ledgers_padding": list(map(lambda item: item.to_json(), self.product_ledgers_padding)),
            "trigger_order_bits": self.trigger_order_bits,
            "padding": self.padding,
        }

    @classmethod
    def from_json(cls, obj: CrossMarginAccountJSON) -> "CrossMarginAccount":
        return cls(
            authority=Pubkey.from_string(obj["authority"]),
            delegated_pubkey=Pubkey.from_string(obj["delegated_pubkey"]),
            balance=obj["balance"],
            subaccount_index=obj["subaccount_index"],
            nonce=obj["nonce"],
            force_cancel_flag=obj["force_cancel_flag"],
            account_type=types.margin_account_type.from_json(obj["account_type"]),
            open_orders_nonces=obj["open_orders_nonces"],
            open_orders_nonces_padding=obj["open_orders_nonces_padding"],
            rebalance_amount=obj["rebalance_amount"],
            last_funding_deltas=list(
                map(
                    lambda item: types.anchor_decimal.AnchorDecimal.from_json(item),
                    obj["last_funding_deltas"],
                )
            ),
            last_funding_deltas_padding=list(
                map(
                    lambda item: types.anchor_decimal.AnchorDecimal.from_json(item),
                    obj["last_funding_deltas_padding"],
                )
            ),
            product_ledgers=list(
                map(
                    lambda item: types.product_ledger.ProductLedger.from_json(item),
                    obj["product_ledgers"],
                )
            ),
            product_ledgers_padding=list(
                map(
                    lambda item: types.product_ledger.ProductLedger.from_json(item),
                    obj["product_ledgers_padding"],
                )
            ),
            trigger_order_bits=obj["trigger_order_bits"],
            padding=obj["padding"],
        )
