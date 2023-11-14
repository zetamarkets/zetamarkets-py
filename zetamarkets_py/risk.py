from dataclasses import dataclass

from zetamarkets_py import constants, utils
from zetamarkets_py.types import Asset
from zetamarkets_py.zeta_client.accounts.cross_margin_account import CrossMarginAccount
from zetamarkets_py.zeta_client.accounts.pricing import Pricing


def compute_upnl(margin_account: CrossMarginAccount, pricing_account: Pricing) -> float:
    """
    Compute the unrealized profit and loss (upnl) of the account.

    Args:
        margin_account (CrossMarginAccount): The margin account of the account.
        pricing_account (Pricing): The pricing account of the account.

    Returns:
        float: The upnl of the account.
    """
    positions = [Position.from_margin_account(margin_account, i) for i in range(len(margin_account.product_ledgers))]
    mark_prices = [utils.convert_fixed_int_to_decimal(p) for p in pricing_account.mark_prices]

    upnl = sum(
        [
            (pos.size * mark_price - pos.cost_of_trades)
            if pos.size > 0
            else (pos.size * mark_price + pos.cost_of_trades)
            for pos, mark_price in zip(positions, mark_prices)
        ]
    )
    return upnl


def compute_margin_usage(margin_account: CrossMarginAccount, pricing_account: Pricing) -> float:
    """
    Compute the margin usage of the account.

    Args:
        positions (dict[Asset, Position]): The positions of the account.
        mark_prices (dict[Asset, float]): The mark prices of the assets.

    Returns:
        float: The margin usage of the account.
    """
    positions = [Position.from_margin_account(margin_account, i) for i in range(len(margin_account.product_ledgers))]
    mark_prices = [utils.convert_fixed_int_to_decimal(p) for p in pricing_account.mark_prices]

    return sum([abs(pos.size) * mark_price for pos, mark_price in zip(positions, mark_prices)])


def compute_initial_margin(margin_account: CrossMarginAccount, pricing_account: Pricing) -> float:
    """
    Compute the initial margin of the account.

    Args:
        margin_account (CrossMarginAccount): The margin account of the account.
        mark_prices (dict): The mark prices of the assets.
        margin_params (dict): The margin parameters of the assets.

    Returns:
        float: The initial margin of the account.
    """
    initial_margin = 0
    for ledger, mark_price_raw, params in zip(
        margin_account.product_ledgers, pricing_account.mark_prices, pricing_account.margin_parameters
    ):
        size = utils.convert_fixed_lot_to_decimal(ledger.position.size)
        mark_price = utils.convert_fixed_int_to_decimal(mark_price_raw)
        long_lots = utils.convert_fixed_lot_to_decimal(ledger.order_state.opening_orders[0])
        short_lots = utils.convert_fixed_lot_to_decimal(ledger.order_state.opening_orders[1])
        initial_margin_ratio = params.future_margin_initial / 10**constants.MARGIN_PRECISION

        if size == 0 and long_lots == 0 and short_lots == 0:
            continue

        if size > 0:
            long_lots += abs(size)
        elif size < 0:
            short_lots += abs(size)

        lots = long_lots if long_lots > short_lots else short_lots
        initial_margin += abs(lots) * mark_price * initial_margin_ratio
    return initial_margin


def compute_maintenance_margin(margin_account: CrossMarginAccount, pricing_account: Pricing) -> float:
    """
    Compute the maintenance margin of the account.

    Args:
        positions (dict): The positions of the account.
        mark_prices (dict): The mark prices of the assets.
        margin_params (dict): The margin parameters of the assets.

    Returns:
        float: The maintenance margin of the account.
    """
    positions = [Position.from_margin_account(margin_account, i) for i in range(len(margin_account.product_ledgers))]
    mark_prices = [utils.convert_fixed_int_to_decimal(p) for p in pricing_account.mark_prices]
    maintenance_margin_params = [
        params.future_margin_maintenance / 10**constants.MARGIN_PRECISION
        for params in pricing_account.margin_parameters
    ]
    return sum(
        [
            abs(pos.size) * mark_price * maintenance_margin_ratio
            for pos, mark_price, maintenance_margin_ratio in zip(positions, mark_prices, maintenance_margin_params)
        ]
    )


@dataclass
class Position:
    """Data class for position details."""

    size: float
    cost_of_trades: float

    @property
    def average_price(self) -> float:
        return self.cost_of_trades / self.size

    @classmethod
    def from_margin_account(cls, margin_account: CrossMarginAccount, asset_index: int):
        return cls(
            utils.convert_fixed_lot_to_decimal(margin_account.product_ledgers[asset_index].position.size),
            utils.convert_fixed_int_to_decimal(margin_account.product_ledgers[asset_index].position.cost_of_trades),
        )


@dataclass
class AccountRiskSummary:
    balance: float
    unrealized_pnl: float
    equity: float
    position_value: float
    initial_margin: float
    maintenance_margin: float
    margin_utilization: float
    leverage: float
    positions: dict[Asset, Position]
    mark_prices: dict[Asset, float]

    @classmethod
    def from_margin_and_pricing_accounts(cls, margin_account: CrossMarginAccount, pricing_account: Pricing):
        balance = utils.convert_fixed_int_to_decimal(margin_account.balance)
        upnl = compute_upnl(margin_account, pricing_account)
        equity = balance + upnl
        position_value = compute_margin_usage(margin_account, pricing_account)
        initial_margin = compute_initial_margin(margin_account, pricing_account)
        maintenance_margin = compute_maintenance_margin(margin_account, pricing_account)
        margin_utilization = maintenance_margin / equity
        leverage = position_value / equity

        # TODO: decide on list vs dict representation
        positions = {
            Asset.from_index(i): Position.from_margin_account(margin_account, i)
            for i in range(len(margin_account.product_ledgers))
        }
        mark_prices = {
            a: utils.convert_fixed_int_to_decimal(p) for a, p in zip(Asset.all(), pricing_account.mark_prices)
        }

        return AccountRiskSummary(
            balance,
            upnl,
            equity,
            position_value,
            initial_margin,
            maintenance_margin,
            margin_utilization,
            leverage,
            positions,
            mark_prices,
        )
