# Module for storing project constants.

from pathlib import Path
from collections import namedtuple

# Project directory and file paths.
CONFIG_PATH = Path("src/my_project/configs/config.yaml")

# PyGame setup.
WINDOW_SIZE_SCREEN_FRACTION: float = 0.9

"""- `Size` denotes the physical or spatial extent of an object, characterized
by its width and height. These measurements are typically expressed in pixels,
but any unit of physical distance may be employed.
"""
Size = namedtuple("Size", "width height")
