"""A first check that the generated package can be imported."""

import importlib


def test_package_version() -> None:
    """The package exposes a nonempty version string."""
    module = importlib.import_module("travelwhiz_dl")
    assert isinstance(module.__version__, str)
    assert module.__version__
