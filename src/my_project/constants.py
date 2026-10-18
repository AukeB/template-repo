"""Module for storing project constants."""

from pathlib import Path
from typing import NamedTuple

_PACKAGE_DIRECTORY = Path(__file__).parent

CONFIG_PATH = _PACKAGE_DIRECTORY / "configs" / "config.yaml"

# PyGame setup.
WINDOW_SIZE_SCREEN_FRACTION: float = 0.9


class Size(NamedTuple):
    """Physical or spatial extent of an object, given by its width and height.

    These measurements are typically expressed in pixels, but any unit of
    physical distance may be employed.

    Attributes:
        width (int): Horizontal extent.
        height (int): Vertical extent.
    """

    width: int
    height: int
