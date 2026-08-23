# Module for storing project constants.

from pathlib import Path
from collections import namedtuple

# Relative file paths.
CONFIG_PATH = Path("src/my_project/configs/config.yaml")

# PyGame setup.
WINDOW_SIZE_SCREEN_FRACTION: float = 0.9
WINDOW_CAPTION: str = "My project"
WINDOW_BACKGROUND_COLOR: list[int] = [0, 0, 0]  # RGB-values.
FPS: int = 60

# Grid setup.
GRID_BACKGROUND_COLOR: list[int] = [100, 100, 100]
GRID_COLOR_MAP: dict = {
    0: (0, 0, 0),
    1: (255, 255, 255),
}

"""
- `Dimensions` refers to the structural properties of a grid, matrix, or layout,
  specifying the number of columns and rows into which the grid is partitioned.
- `Size` denotes the physical or spatial extent of an object, characterized by
  its width and height. These measurements are typically expressed in pixels,
  but any unit of physical distance may be employed.
- `Position` specifies a location using `x` and `y` coordinates. These
  coordinates may represent a position on the screen in pixel units, or a
  location within a grid or board, expressed in terms of columns and rows.
"""
Dimensions = namedtuple("Dimensions", "rows cols")
Size = namedtuple("Size", "width height")
Position = namedtuple("Position", "x y")