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


class GreeksJSON(typing.TypedDict):
    nonce: int
    mark_prices: list[int]
    mark_prices_padding: list[int]
    perp_mark_price: int
    product_greeks: list[types.product_greeks.ProductGreeksJSON]
    product_greeks_padding: list[types.product_greeks.ProductGreeksJSON]
    update_timestamp: list[int]
    update_timestamp_padding: list[int]
    retreat_expiration_timestamp: list[int]
    retreat_expiration_timestamp_padding: list[int]
    interest_rate: list[int]
    interest_rate_padding: list[int]
    nodes: list[int]
    volatility: list[int]
    volatility_padding: list[int]
    node_keys: list[str]
    halt_force_pricing: list[bool]
    perp_update_timestamp: int
    perp_funding_delta: types.anchor_decimal.AnchorDecimalJSON
    perp_latest_funding_rate: types.anchor_decimal.AnchorDecimalJSON
    perp_latest_midpoint: int
    padding: list[int]


@dataclass
class Greeks:
    discriminator: typing.ClassVar = b"\xf7\xd5\xaa\x9a+\xf3\x92\xfe"
    layout: typing.ClassVar = borsh.CStruct(
        "nonce" / borsh.U8,
        "mark_prices" / borsh.U64[46],
        "mark_prices_padding" / borsh.U64[91],
        "perp_mark_price" / borsh.U64,
        "product_greeks" / types.product_greeks.ProductGreeks.layout[22],
        "product_greeks_padding" / types.product_greeks.ProductGreeks.layout[44],
        "update_timestamp" / borsh.U64[2],
        "update_timestamp_padding" / borsh.U64[4],
        "retreat_expiration_timestamp" / borsh.U64[2],
        "retreat_expiration_timestamp_padding" / borsh.U64[4],
        "interest_rate" / borsh.I64[2],
        "interest_rate_padding" / borsh.I64[4],
        "nodes" / borsh.U64[5],
        "volatility" / borsh.U64[10],
        "volatility_padding" / borsh.U64[20],
        "node_keys" / BorshPubkey[138],
        "halt_force_pricing" / borsh.Bool[6],
        "perp_update_timestamp" / borsh.U64,
        "perp_funding_delta" / types.anchor_decimal.AnchorDecimal.layout,
        "perp_latest_funding_rate" / types.anchor_decimal.AnchorDecimal.layout,
        "perp_latest_midpoint" / borsh.U64,
        "padding" / borsh.U8[1593],
    )
    nonce: int
    mark_prices: list[int]
    mark_prices_padding: list[int]
    perp_mark_price: int
    product_greeks: list[types.product_greeks.ProductGreeks]
    product_greeks_padding: list[types.product_greeks.ProductGreeks]
    update_timestamp: list[int]
    update_timestamp_padding: list[int]
    retreat_expiration_timestamp: list[int]
    retreat_expiration_timestamp_padding: list[int]
    interest_rate: list[int]
    interest_rate_padding: list[int]
    nodes: list[int]
    volatility: list[int]
    volatility_padding: list[int]
    node_keys: list[Pubkey]
    halt_force_pricing: list[bool]
    perp_update_timestamp: int
    perp_funding_delta: types.anchor_decimal.AnchorDecimal
    perp_latest_funding_rate: types.anchor_decimal.AnchorDecimal
    perp_latest_midpoint: int
    padding: list[int]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["Greeks"]:
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
    ) -> typing.List[typing.Optional["Greeks"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["Greeks"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "Greeks":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = Greeks.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            nonce=dec.nonce,
            mark_prices=dec.mark_prices,
            mark_prices_padding=dec.mark_prices_padding,
            perp_mark_price=dec.perp_mark_price,
            product_greeks=list(
                map(
                    lambda item: types.product_greeks.ProductGreeks.from_decoded(item),
                    dec.product_greeks,
                )
            ),
            product_greeks_padding=list(
                map(
                    lambda item: types.product_greeks.ProductGreeks.from_decoded(item),
                    dec.product_greeks_padding,
                )
            ),
            update_timestamp=dec.update_timestamp,
            update_timestamp_padding=dec.update_timestamp_padding,
            retreat_expiration_timestamp=dec.retreat_expiration_timestamp,
            retreat_expiration_timestamp_padding=dec.retreat_expiration_timestamp_padding,
            interest_rate=dec.interest_rate,
            interest_rate_padding=dec.interest_rate_padding,
            nodes=dec.nodes,
            volatility=dec.volatility,
            volatility_padding=dec.volatility_padding,
            node_keys=dec.node_keys,
            halt_force_pricing=dec.halt_force_pricing,
            perp_update_timestamp=dec.perp_update_timestamp,
            perp_funding_delta=types.anchor_decimal.AnchorDecimal.from_decoded(dec.perp_funding_delta),
            perp_latest_funding_rate=types.anchor_decimal.AnchorDecimal.from_decoded(dec.perp_latest_funding_rate),
            perp_latest_midpoint=dec.perp_latest_midpoint,
            padding=dec.padding,
        )

    def to_json(self) -> GreeksJSON:
        return {
            "nonce": self.nonce,
            "mark_prices": self.mark_prices,
            "mark_prices_padding": self.mark_prices_padding,
            "perp_mark_price": self.perp_mark_price,
            "product_greeks": list(map(lambda item: item.to_json(), self.product_greeks)),
            "product_greeks_padding": list(map(lambda item: item.to_json(), self.product_greeks_padding)),
            "update_timestamp": self.update_timestamp,
            "update_timestamp_padding": self.update_timestamp_padding,
            "retreat_expiration_timestamp": self.retreat_expiration_timestamp,
            "retreat_expiration_timestamp_padding": self.retreat_expiration_timestamp_padding,
            "interest_rate": self.interest_rate,
            "interest_rate_padding": self.interest_rate_padding,
            "nodes": self.nodes,
            "volatility": self.volatility,
            "volatility_padding": self.volatility_padding,
            "node_keys": list(map(lambda item: str(item), self.node_keys)),
            "halt_force_pricing": self.halt_force_pricing,
            "perp_update_timestamp": self.perp_update_timestamp,
            "perp_funding_delta": self.perp_funding_delta.to_json(),
            "perp_latest_funding_rate": self.perp_latest_funding_rate.to_json(),
            "perp_latest_midpoint": self.perp_latest_midpoint,
            "padding": self.padding,
        }

    @classmethod
    def from_json(cls, obj: GreeksJSON) -> "Greeks":
        return cls(
            nonce=obj["nonce"],
            mark_prices=obj["mark_prices"],
            mark_prices_padding=obj["mark_prices_padding"],
            perp_mark_price=obj["perp_mark_price"],
            product_greeks=list(
                map(
                    lambda item: types.product_greeks.ProductGreeks.from_json(item),
                    obj["product_greeks"],
                )
            ),
            product_greeks_padding=list(
                map(
                    lambda item: types.product_greeks.ProductGreeks.from_json(item),
                    obj["product_greeks_padding"],
                )
            ),
            update_timestamp=obj["update_timestamp"],
            update_timestamp_padding=obj["update_timestamp_padding"],
            retreat_expiration_timestamp=obj["retreat_expiration_timestamp"],
            retreat_expiration_timestamp_padding=obj["retreat_expiration_timestamp_padding"],
            interest_rate=obj["interest_rate"],
            interest_rate_padding=obj["interest_rate_padding"],
            nodes=obj["nodes"],
            volatility=obj["volatility"],
            volatility_padding=obj["volatility_padding"],
            node_keys=list(map(lambda item: Pubkey.from_string(item), obj["node_keys"])),
            halt_force_pricing=obj["halt_force_pricing"],
            perp_update_timestamp=obj["perp_update_timestamp"],
            perp_funding_delta=types.anchor_decimal.AnchorDecimal.from_json(obj["perp_funding_delta"]),
            perp_latest_funding_rate=types.anchor_decimal.AnchorDecimal.from_json(obj["perp_latest_funding_rate"]),
            perp_latest_midpoint=obj["perp_latest_midpoint"],
            padding=obj["padding"],
        )
