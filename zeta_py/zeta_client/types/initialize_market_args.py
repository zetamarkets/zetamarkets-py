from __future__ import annotations

import typing
from dataclasses import dataclass

import borsh_construct as borsh
from construct import Container

from . import asset


class InitializeMarketArgsJSON(typing.TypedDict):
    asset: asset.AssetJSON
    market_nonce: int
    base_mint_nonce: int
    quote_mint_nonce: int
    zeta_base_vault_nonce: int
    zeta_quote_vault_nonce: int
    dex_base_vault_nonce: int
    dex_quote_vault_nonce: int
    vault_signer_nonce: int


@dataclass
class InitializeMarketArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "asset" / asset.layout,
        "market_nonce" / borsh.U8,
        "base_mint_nonce" / borsh.U8,
        "quote_mint_nonce" / borsh.U8,
        "zeta_base_vault_nonce" / borsh.U8,
        "zeta_quote_vault_nonce" / borsh.U8,
        "dex_base_vault_nonce" / borsh.U8,
        "dex_quote_vault_nonce" / borsh.U8,
        "vault_signer_nonce" / borsh.U64,
    )
    asset: asset.AssetKind
    market_nonce: int
    base_mint_nonce: int
    quote_mint_nonce: int
    zeta_base_vault_nonce: int
    zeta_quote_vault_nonce: int
    dex_base_vault_nonce: int
    dex_quote_vault_nonce: int
    vault_signer_nonce: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "InitializeMarketArgs":
        return cls(
            asset=asset.from_decoded(obj.asset),
            market_nonce=obj.market_nonce,
            base_mint_nonce=obj.base_mint_nonce,
            quote_mint_nonce=obj.quote_mint_nonce,
            zeta_base_vault_nonce=obj.zeta_base_vault_nonce,
            zeta_quote_vault_nonce=obj.zeta_quote_vault_nonce,
            dex_base_vault_nonce=obj.dex_base_vault_nonce,
            dex_quote_vault_nonce=obj.dex_quote_vault_nonce,
            vault_signer_nonce=obj.vault_signer_nonce,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "asset": self.asset.to_encodable(),
            "market_nonce": self.market_nonce,
            "base_mint_nonce": self.base_mint_nonce,
            "quote_mint_nonce": self.quote_mint_nonce,
            "zeta_base_vault_nonce": self.zeta_base_vault_nonce,
            "zeta_quote_vault_nonce": self.zeta_quote_vault_nonce,
            "dex_base_vault_nonce": self.dex_base_vault_nonce,
            "dex_quote_vault_nonce": self.dex_quote_vault_nonce,
            "vault_signer_nonce": self.vault_signer_nonce,
        }

    def to_json(self) -> InitializeMarketArgsJSON:
        return {
            "asset": self.asset.to_json(),
            "market_nonce": self.market_nonce,
            "base_mint_nonce": self.base_mint_nonce,
            "quote_mint_nonce": self.quote_mint_nonce,
            "zeta_base_vault_nonce": self.zeta_base_vault_nonce,
            "zeta_quote_vault_nonce": self.zeta_quote_vault_nonce,
            "dex_base_vault_nonce": self.dex_base_vault_nonce,
            "dex_quote_vault_nonce": self.dex_quote_vault_nonce,
            "vault_signer_nonce": self.vault_signer_nonce,
        }

    @classmethod
    def from_json(cls, obj: InitializeMarketArgsJSON) -> "InitializeMarketArgs":
        return cls(
            asset=asset.from_json(obj["asset"]),
            market_nonce=obj["market_nonce"],
            base_mint_nonce=obj["base_mint_nonce"],
            quote_mint_nonce=obj["quote_mint_nonce"],
            zeta_base_vault_nonce=obj["zeta_base_vault_nonce"],
            zeta_quote_vault_nonce=obj["zeta_quote_vault_nonce"],
            dex_base_vault_nonce=obj["dex_base_vault_nonce"],
            dex_quote_vault_nonce=obj["dex_quote_vault_nonce"],
            vault_signer_nonce=obj["vault_signer_nonce"],
        )
