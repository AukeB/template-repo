# Module for storing project constants.

from pathlib import Path

# Relative file paths.
CONFIG_PATH = Path("src/my_project/configs/config.yaml")

# PyGame setup.
WINDOW_SIZE_SCREEN_FRACTION: float = 0.9
WINDOW_CAPTION: str = "My project"
BACKGROUND_COLOR: list[int] = [0, 0, 0]  # RGB-values.
FPS: int = 60
