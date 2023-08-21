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

from ..program_id import PROGRAM_ID


class ReferrerAccountJSON(typing.TypedDict):
    nonce: int
    has_alias: bool
    referrer: str
    pending_rewards: int
    claimed_rewards: int


@dataclass
class ReferrerAccount:
    discriminator: typing.ClassVar = b"0\x13\xa06L\xdcF\t"
    layout: typing.ClassVar = borsh.CStruct(
        "nonce" / borsh.U8,
        "has_alias" / borsh.Bool,
        "referrer" / BorshPubkey,
        "pending_rewards" / borsh.U64,
        "claimed_rewards" / borsh.U64,
    )
    nonce: int
    has_alias: bool
    referrer: Pubkey
    pending_rewards: int
    claimed_rewards: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["ReferrerAccount"]:
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
    ) -> typing.List[typing.Optional["ReferrerAccount"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["ReferrerAccount"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "ReferrerAccount":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = ReferrerAccount.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            nonce=dec.nonce,
            has_alias=dec.has_alias,
            referrer=dec.referrer,
            pending_rewards=dec.pending_rewards,
            claimed_rewards=dec.claimed_rewards,
        )

    def to_json(self) -> ReferrerAccountJSON:
        return {
            "nonce": self.nonce,
            "has_alias": self.has_alias,
            "referrer": str(self.referrer),
            "pending_rewards": self.pending_rewards,
            "claimed_rewards": self.claimed_rewards,
        }

    @classmethod
    def from_json(cls, obj: ReferrerAccountJSON) -> "ReferrerAccount":
        return cls(
            nonce=obj["nonce"],
            has_alias=obj["has_alias"],
            referrer=Pubkey.from_string(obj["referrer"]),
            pending_rewards=obj["pending_rewards"],
            claimed_rewards=obj["claimed_rewards"],
        )
