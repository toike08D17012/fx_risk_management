"""Smoke tests for the FX risk management package."""

from fx_risk_management import __version__


def test_package_version() -> None:
    """Ensure the base package is importable."""
    assert __version__ == "0.1.0"
