from zeta_py.constants import Asset


def all_assets():
    all_assets = []
    for a in Asset:
        if isinstance(a.name) == str and a != "UNDEFINED":
            all_assets.append(a.value)
    return all_assets


def asset_to_index(asset: Asset) -> int:
    if asset == Asset.SOL:
        return 0
    elif asset == Asset.BTC:
        return 1
    elif asset == Asset.ETH:
        return 2
    elif asset == Asset.APT:
        return 3
    elif asset == Asset.ARB:
        return 4
    raise Exception("Invalid asset")
