"""Module for pygame window setup and rendering."""

import pygame as pg

from src.my_project.config_model import ConfigModel
from src.my_project.constants import WINDOW_CAPTION, BACKGROUND_COLOR
from src.my_project.utils.utils_pygame import get_window_size_from_screen_resolution


class Renderer:
    """Manages the pygame window and draws each frame."""

    def __init__(self, config: ConfigModel) -> None:
        """Initializes the renderer with configuration.

        Args:
            config (ConfigModel): Pydantic-validated configuration model.
        """
        self.config = config

        pg.init()

        width, height = get_window_size_from_screen_resolution()
        self.screen = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()
        self.background_color = BACKGROUND_COLOR

        pg.display.set_caption(WINDOW_CAPTION)

    def tick(self, fps: int) -> float:
        """Advances the frame clock and reports the elapsed time.

        Args:
            fps (int): Target frames per second to cap the loop at.

        Returns:
            delta_time (float): Time in seconds elapsed since the last frame.
        """
        dt = self.clock.tick(fps) / 1000

        return dt

    def render(self) -> None:
        """Draws the current frame to the display surface."""
        self.screen.fill(self.background_color)
        pg.display.flip()

    def quit(self) -> None:
        """Shuts down pygame."""
        pg.quit()
