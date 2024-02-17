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


class TriggerOrderJSON(typing.TypedDict):
    owner: str
    margin_account: str
    open_orders: str
    order_price: int
    trigger_price: typing.Optional[int]
    trigger_ts: typing.Optional[int]
    size: int
    creation_ts: int
    trigger_direction: typing.Optional[types.trigger_direction.TriggerDirectionJSON]
    side: types.side.SideJSON
    asset: types.asset.AssetJSON
    order_type: types.order_type.OrderTypeJSON
    bit: int
    reduce_only: bool


@dataclass
class TriggerOrder:
    discriminator: typing.ClassVar = b"\xec=*\xbe\x98\x0cjt"
    layout: typing.ClassVar = borsh.CStruct(
        "owner" / BorshPubkey,
        "margin_account" / BorshPubkey,
        "open_orders" / BorshPubkey,
        "order_price" / borsh.U64,
        "trigger_price" / borsh.Option(borsh.U64),
        "trigger_ts" / borsh.Option(borsh.U64),
        "size" / borsh.U64,
        "creation_ts" / borsh.U64,
        "trigger_direction" / borsh.Option(types.trigger_direction.layout),
        "side" / types.side.layout,
        "asset" / types.asset.layout,
        "order_type" / types.order_type.layout,
        "bit" / borsh.U8,
        "reduce_only" / borsh.Bool,
    )
    owner: Pubkey
    margin_account: Pubkey
    open_orders: Pubkey
    order_price: int
    trigger_price: typing.Optional[int]
    trigger_ts: typing.Optional[int]
    size: int
    creation_ts: int
    trigger_direction: typing.Optional[types.trigger_direction.TriggerDirectionKind]
    side: types.side.SideKind
    asset: types.asset.AssetKind
    order_type: types.order_type.OrderTypeKind
    bit: int
    reduce_only: bool

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["TriggerOrder"]:
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
    ) -> typing.List[typing.Optional["TriggerOrder"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["TriggerOrder"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "TriggerOrder":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = TriggerOrder.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            owner=dec.owner,
            margin_account=dec.margin_account,
            open_orders=dec.open_orders,
            order_price=dec.order_price,
            trigger_price=dec.trigger_price,
            trigger_ts=dec.trigger_ts,
            size=dec.size,
            creation_ts=dec.creation_ts,
            trigger_direction=(
                None if dec.trigger_direction is None else types.trigger_direction.from_decoded(dec.trigger_direction)
            ),
            side=types.side.from_decoded(dec.side),
            asset=types.asset.from_decoded(dec.asset),
            order_type=types.order_type.from_decoded(dec.order_type),
            bit=dec.bit,
            reduce_only=dec.reduce_only,
        )

    def to_json(self) -> TriggerOrderJSON:
        return {
            "owner": str(self.owner),
            "margin_account": str(self.margin_account),
            "open_orders": str(self.open_orders),
            "order_price": self.order_price,
            "trigger_price": self.trigger_price,
            "trigger_ts": self.trigger_ts,
            "size": self.size,
            "creation_ts": self.creation_ts,
            "trigger_direction": (None if self.trigger_direction is None else self.trigger_direction.to_json()),
            "side": self.side.to_json(),
            "asset": self.asset.to_json(),
            "order_type": self.order_type.to_json(),
            "bit": self.bit,
            "reduce_only": self.reduce_only,
        }

    @classmethod
    def from_json(cls, obj: TriggerOrderJSON) -> "TriggerOrder":
        return cls(
            owner=Pubkey.from_string(obj["owner"]),
            margin_account=Pubkey.from_string(obj["margin_account"]),
            open_orders=Pubkey.from_string(obj["open_orders"]),
            order_price=obj["order_price"],
            trigger_price=obj["trigger_price"],
            trigger_ts=obj["trigger_ts"],
            size=obj["size"],
            creation_ts=obj["creation_ts"],
            trigger_direction=(
                None
                if obj["trigger_direction"] is None
                else types.trigger_direction.from_json(obj["trigger_direction"])
            ),
            side=types.side.from_json(obj["side"]),
            asset=types.asset.from_json(obj["asset"]),
            order_type=types.order_type.from_json(obj["order_type"]),
            bit=obj["bit"],
            reduce_only=obj["reduce_only"],
        )
