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


class MarginAccountJSON(typing.TypedDict):
    authority: str
    nonce: int
    balance: int
    force_cancel_flag: bool
    open_orders_nonce: list[int]
    series_expiry: list[int]
    series_expiry_padding: int
    product_ledgers: list[types.product_ledger.ProductLedgerJSON]
    product_ledgers_padding: list[types.product_ledger.ProductLedgerJSON]
    perp_product_ledger: types.product_ledger.ProductLedgerJSON
    rebalance_amount: int
    asset: types.asset.AssetJSON
    account_type: types.margin_account_type.MarginAccountTypeJSON
    last_funding_delta: types.anchor_decimal.AnchorDecimalJSON
    delegated_pubkey: str
    padding: list[int]


@dataclass
class MarginAccount:
    discriminator: typing.ClassVar = b"\x85\xdc\xad\xd5\xb3\xd3+\xee"
    layout: typing.ClassVar = borsh.CStruct(
        "authority" / BorshPubkey,
        "nonce" / borsh.U8,
        "balance" / borsh.U64,
        "force_cancel_flag" / borsh.Bool,
        "open_orders_nonce" / borsh.U8[138],
        "series_expiry" / borsh.U64[5],
        "series_expiry_padding" / borsh.U64,
        "product_ledgers" / types.product_ledger.ProductLedger.layout[46],
        "product_ledgers_padding" / types.product_ledger.ProductLedger.layout[91],
        "perp_product_ledger" / types.product_ledger.ProductLedger.layout,
        "rebalance_amount" / borsh.I64,
        "asset" / types.asset.layout,
        "account_type" / types.margin_account_type.layout,
        "last_funding_delta" / types.anchor_decimal.AnchorDecimal.layout,
        "delegated_pubkey" / BorshPubkey,
        "padding" / borsh.U8[338],
    )
    authority: Pubkey
    nonce: int
    balance: int
    force_cancel_flag: bool
    open_orders_nonce: list[int]
    series_expiry: list[int]
    series_expiry_padding: int
    product_ledgers: list[types.product_ledger.ProductLedger]
    product_ledgers_padding: list[types.product_ledger.ProductLedger]
    perp_product_ledger: types.product_ledger.ProductLedger
    rebalance_amount: int
    asset: types.asset.AssetKind
    account_type: types.margin_account_type.MarginAccountTypeKind
    last_funding_delta: types.anchor_decimal.AnchorDecimal
    delegated_pubkey: Pubkey
    padding: list[int]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["MarginAccount"]:
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
    ) -> typing.List[typing.Optional["MarginAccount"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["MarginAccount"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "MarginAccount":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = MarginAccount.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            authority=dec.authority,
            nonce=dec.nonce,
            balance=dec.balance,
            force_cancel_flag=dec.force_cancel_flag,
            open_orders_nonce=dec.open_orders_nonce,
            series_expiry=dec.series_expiry,
            series_expiry_padding=dec.series_expiry_padding,
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
            perp_product_ledger=types.product_ledger.ProductLedger.from_decoded(dec.perp_product_ledger),
            rebalance_amount=dec.rebalance_amount,
            asset=types.asset.from_decoded(dec.asset),
            account_type=types.margin_account_type.from_decoded(dec.account_type),
            last_funding_delta=types.anchor_decimal.AnchorDecimal.from_decoded(dec.last_funding_delta),
            delegated_pubkey=dec.delegated_pubkey,
            padding=dec.padding,
        )

    def to_json(self) -> MarginAccountJSON:
        return {
            "authority": str(self.authority),
            "nonce": self.nonce,
            "balance": self.balance,
            "force_cancel_flag": self.force_cancel_flag,
            "open_orders_nonce": self.open_orders_nonce,
            "series_expiry": self.series_expiry,
            "series_expiry_padding": self.series_expiry_padding,
            "product_ledgers": list(map(lambda item: item.to_json(), self.product_ledgers)),
            "product_ledgers_padding": list(map(lambda item: item.to_json(), self.product_ledgers_padding)),
            "perp_product_ledger": self.perp_product_ledger.to_json(),
            "rebalance_amount": self.rebalance_amount,
            "asset": self.asset.to_json(),
            "account_type": self.account_type.to_json(),
            "last_funding_delta": self.last_funding_delta.to_json(),
            "delegated_pubkey": str(self.delegated_pubkey),
            "padding": self.padding,
        }

    @classmethod
    def from_json(cls, obj: MarginAccountJSON) -> "MarginAccount":
        return cls(
            authority=Pubkey.from_string(obj["authority"]),
            nonce=obj["nonce"],
            balance=obj["balance"],
            force_cancel_flag=obj["force_cancel_flag"],
            open_orders_nonce=obj["open_orders_nonce"],
            series_expiry=obj["series_expiry"],
            series_expiry_padding=obj["series_expiry_padding"],
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
            perp_product_ledger=types.product_ledger.ProductLedger.from_json(obj["perp_product_ledger"]),
            rebalance_amount=obj["rebalance_amount"],
            asset=types.asset.from_json(obj["asset"]),
            account_type=types.margin_account_type.from_json(obj["account_type"]),
            last_funding_delta=types.anchor_decimal.AnchorDecimal.from_json(obj["last_funding_delta"]),
            delegated_pubkey=Pubkey.from_string(obj["delegated_pubkey"]),
            padding=obj["padding"],
        )
