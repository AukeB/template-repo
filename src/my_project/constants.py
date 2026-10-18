"""Module for storing project constants."""

from pathlib import Path

_PACKAGE_DIRECTORY = Path(__file__).parent

CONFIG_PATH = _PACKAGE_DIRECTORY / "configs" / "config.yaml"
