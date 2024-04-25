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


class CrossMarginAccountManagerJSON(typing.TypedDict):
    nonce: int
    authority: str
    accounts: list[types.cross_margin_account_info.CrossMarginAccountInfoJSON]
    referrer: str
    airdrop_community: int
    padding: list[int]


@dataclass
class CrossMarginAccountManager:
    discriminator: typing.ClassVar = b"\\\xa2\x1aC1V\xfc\x05"
    layout: typing.ClassVar = borsh.CStruct(
        "nonce" / borsh.U8,
        "authority" / BorshPubkey,
        "accounts" / types.cross_margin_account_info.CrossMarginAccountInfo.layout[20],
        "referrer" / BorshPubkey,
        "airdrop_community" / borsh.U8,
        "padding" / borsh.U8[22],
    )
    nonce: int
    authority: Pubkey
    accounts: list[types.cross_margin_account_info.CrossMarginAccountInfo]
    referrer: Pubkey
    airdrop_community: int
    padding: list[int]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["CrossMarginAccountManager"]:
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
    ) -> typing.List[typing.Optional["CrossMarginAccountManager"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["CrossMarginAccountManager"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "CrossMarginAccountManager":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = CrossMarginAccountManager.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            nonce=dec.nonce,
            authority=dec.authority,
            accounts=list(
                map(
                    lambda item: types.cross_margin_account_info.CrossMarginAccountInfo.from_decoded(item),
                    dec.accounts,
                )
            ),
            referrer=dec.referrer,
            airdrop_community=dec.airdrop_community,
            padding=dec.padding,
        )

    def to_json(self) -> CrossMarginAccountManagerJSON:
        return {
            "nonce": self.nonce,
            "authority": str(self.authority),
            "accounts": list(map(lambda item: item.to_json(), self.accounts)),
            "referrer": str(self.referrer),
            "airdrop_community": self.airdrop_community,
            "padding": self.padding,
        }

    @classmethod
    def from_json(cls, obj: CrossMarginAccountManagerJSON) -> "CrossMarginAccountManager":
        return cls(
            nonce=obj["nonce"],
            authority=Pubkey.from_string(obj["authority"]),
            accounts=list(
                map(
                    lambda item: types.cross_margin_account_info.CrossMarginAccountInfo.from_json(item),
                    obj["accounts"],
                )
            ),
            referrer=Pubkey.from_string(obj["referrer"]),
            airdrop_community=obj["airdrop_community"],
            padding=obj["padding"],
        )
