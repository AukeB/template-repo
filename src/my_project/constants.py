"""Module for storing project constants."""

from pathlib import Path
from typing import NamedTuple

_PACKAGE_DIRECTORY = Path(__file__).parent

CONFIG_PATH = _PACKAGE_DIRECTORY / "configs" / "config.yaml"

# PyGame setup.
WINDOW_SIZE_SCREEN_FRACTION: float = 0.9


class Dimensions(NamedTuple):
    """Structural properties of a grid, matrix, or layout.

    Specifies the number of columns and rows into which the grid is partitioned.

    Attributes:
        rows (int): Number of rows.
        cols (int): Number of columns.
    """

    rows: int
    cols: int


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


class Position(NamedTuple):
    """A location using x and y coordinates.

    These coordinates may represent a position on the screen in pixel units, or
    a location within a grid or board, expressed in terms of columns and rows.

    Attributes:
        x (int): Horizontal coordinate, which maps to the column in a grid.
        y (int): Vertical coordinate, which maps to the row in a grid.
    """

    x: int
    y: int
