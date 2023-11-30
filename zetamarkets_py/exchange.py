from __future__ import annotations

import logging
import os
from dataclasses import dataclass

from anchorpy import EventParser, Idl, Program, Provider, Wallet
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey

from zetamarkets_py import constants, pda, utils
from zetamarkets_py.market import Market
from zetamarkets_py.types import Asset, Network
from zetamarkets_py.zeta_client.accounts.pricing import Pricing
from zetamarkets_py.zeta_client.accounts.state import State

idl_path = os.path.join(os.path.dirname(__file__), "idl/zeta.json")
with open(idl_path, "r") as f:
    idl = Idl.from_json(f.read())


@dataclass
class Exchange:
    """
    This class represents the Zeta Exchange. It contains all the necessary attributes and methods
    for interacting with the Zeta Exchange, including loading the exchange, fetching state and pricing,
    and handling various market assets.

    Note:
        Loading the exchange is asynchronous, so it is recommended to use :func:`load` to
        initialize the exchange.
    """

    # Initialize
    connection: AsyncClient
    """The connection to the Solana network."""
    program_id: Pubkey
    """The public key of the Zeta program."""
    program: Program
    """The Zeta program."""
    state: State
    """The state account of the Zeta program."""
    pricing: Pricing
    """The pricing account of the Zeta program. Stores mark prices, funding rates etc."""
    markets: dict[Asset, Market]
    """A dictionary mapping assets to their respective markets."""

    _event_parser: EventParser

    _state_address: Pubkey
    _pricing_address: Pubkey
    _serum_authority_address: Pubkey
    _mint_authority_address: Pubkey

    _logger: logging.Logger

    @classmethod
    async def load(
        cls,
        network: Network,
        connection: AsyncClient,
        assets: list[Asset] = Asset.all(),
        log_level: int = logging.CRITICAL,
    ) -> "Exchange":
        """
        Asynchronously load the Zeta Exchange.

        Args:
            network (Network): The network to connect to.
            connection (AsyncClient): The connection to the Solana network.
            assets (list[Asset], optional): The list of assets to load. Defaults to all assets.
            log_level (int, optional): The logging level. Defaults to logging.CRITICAL.

        Returns:
            Exchange: The loaded Zeta Exchange.

        Raises:
            Exception: If the state or pricing is not found at their respective addresses.
        """
        program_id = constants.ZETA_PID[network]
        provider = Provider(connection, Wallet.dummy())
        program = Program(idl, program_id, provider)
        _event_parser = EventParser(program_id, program.coder)

        # Accounts
        state_address = pda.get_state_address(program_id)
        state = await State.fetch(connection, state_address, connection.commitment, program_id=program_id)
        if state is None:
            raise Exception(f"State not found at {state_address}")

        pricing_address = pda.get_pricing_address(program_id)
        pricing = await Pricing.fetch(connection, pricing_address, connection.commitment, program_id=program_id)
        if pricing is None:
            raise Exception(f"Pricing not found at {pricing_address}")

        # Addresses
        _serum_authority_address = pda.get_serum_authority_address(program_id)
        _mint_authority_address = pda.get_mint_authority_address(program_id)

        markets = {
            asset: await Market.load(network, connection, asset, pricing.markets[asset.to_index()]) for asset in assets
        }

        # not currently used
        logger = utils.create_logger(f"{__name__}.{cls.__name__}", log_level)

        instance = cls(
            connection=connection,
            program_id=program_id,
            program=program,
            state=state,
            pricing=pricing,
            markets=markets,
            _event_parser=_event_parser,
            _state_address=state_address,
            _pricing_address=pricing_address,
            _serum_authority_address=_serum_authority_address,
            _mint_authority_address=_mint_authority_address,
            _logger=logger,
        )

        return instance

    @property
    def endpoint(self) -> str:
        """
        Returns the RPC endpoint.

        Returns:
            str: The endpoint URI.
        """
        return self.connection._provider.endpoint_uri

    @property
    def assets(self) -> list[Asset]:
        """
        Returns a list of keys from the markets dictionary.

        Returns:
            list[Asset]: A list of Asset objects.
        """
        return list(self.markets.keys())
