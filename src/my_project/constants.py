# Module for storing project constants.

from pathlib import Path

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
