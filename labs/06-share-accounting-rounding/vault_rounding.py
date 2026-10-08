"""Educational share-accounting model; not a deployable ERC-4626 vault."""


class Rejected(ValueError):
    pass


def _positive_int(name, value):
    if type(value) is not int or value <= 0:
        raise Rejected(f"invalid {name}")


def _nonnegative_int(name, value):
    if type(value) is not int or value < 0:
        raise Rejected(f"invalid {name}")


def _ceil_div(numerator, denominator):
    return (numerator + denominator - 1) // denominator


class VulnerableVault:
    """Allows a rounded-to-zero deposit after an exchange-rate donation."""

    def __init__(self):
        self.total_assets = 0
        self.total_shares = 0

    def deposit(self, assets):
        _positive_int("assets", assets)
        if self.total_shares == 0:
            shares = assets
        else:
            shares = assets * self.total_shares // self.total_assets
        self.total_assets += assets
        self.total_shares += shares
        return shares

    def donate(self, assets):
        _positive_int("assets", assets)
        self.total_assets += assets


class OffsetVault:
    """Makes rounding explicit and anchors the empty-vault exchange rate."""

    def __init__(self, decimals_offset=3):
        _nonnegative_int("decimals_offset", decimals_offset)
        if decimals_offset > 18:
            raise Rejected("invalid decimals_offset")
        self.total_assets = 0
        self.total_shares = 0
        self.virtual_assets = 1
        self.virtual_shares = 10**decimals_offset

    def _effective_assets(self):
        return self.total_assets + self.virtual_assets

    def _effective_shares(self):
        return self.total_shares + self.virtual_shares

    def preview_deposit(self, assets):
        _positive_int("assets", assets)
        # Deposits round down so the preview never promises too many shares.
        return assets * self._effective_shares() // self._effective_assets()

    def preview_mint(self, shares):
        _positive_int("shares", shares)
        # Mints round up so the preview never understates required assets.
        return _ceil_div(
            shares * self._effective_assets(), self._effective_shares()
        )

    def deposit(self, assets, *, min_shares=1):
        _nonnegative_int("min_shares", min_shares)
        shares = self.preview_deposit(assets)
        if shares < min_shares:
            raise Rejected("share output is below the caller's bound")
        self.total_assets += assets
        self.total_shares += shares
        return shares

    def mint(self, shares, *, max_assets):
        _positive_int("max_assets", max_assets)
        assets = self.preview_mint(shares)
        if assets > max_assets:
            raise Rejected("asset input exceeds the caller's bound")
        self.total_assets += assets
        self.total_shares += shares
        return assets

    def donate(self, assets):
        _positive_int("assets", assets)
        self.total_assets += assets
