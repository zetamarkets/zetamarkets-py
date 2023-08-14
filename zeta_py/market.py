from __future__ import annotations

from dataclasses import dataclass

# https://www.attrs.org/en/stable/examples.html#defaults
from attr import define

from zeta_py.constants import Asset


@dataclass
class Market:
    asset: Asset
    exchange: Exchange

    async def load(self):
        pass
