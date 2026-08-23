"""Module for pygame window setup and rendering."""

import pygame as pg

from src.my_project.config_model import ConfigModel
from src.my_project.constants import GRID_BACKGROUND_COLOR, WINDOW_CAPTION
from src.my_project.grid import Grid


class Renderer:
    """Manages the pygame window and draws each frame."""

    def __init__(self, config: ConfigModel) -> None:
        """Initializes the renderer with configuration.

        Args:
            config (ConfigModel): Pydantic-validated configuration model.
        """
        self.config = config

        # State
        self.screen: pg.Surface
        self.clock: pg.time.Clock

    def setup(self, width: int, height: int) -> None:
        """Initializes pygame and creates the display window.

        Args:
            width (int): Window width in pixels.
            height (int): Window height in pixels.
        """
        pg.init()

        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(WINDOW_CAPTION)
        self.clock = pg.time.Clock()

    def tick(self, fps: int) -> float:
        """Advances the frame clock and reports the elapsed time.

        Args:
            fps (int): Target frames per second to cap the loop at.

        Returns:
            dt (float): Time in seconds elapsed since the last frame.
        """
        dt = self.clock.tick(fps) / 1000

        return dt

    def clear(self) -> None:
        """Fills the display surface with the background color."""
        self.screen.fill(GRID_BACKGROUND_COLOR)

    def render_grid(
        self,
        grid: Grid,
        cell_size: int,
        color_map: dict[int, tuple[int, int, int]],
    ) -> None:
        """Draws every cell of the grid onto the display surface.

        Args:
            grid (Grid): The grid whose cells will be drawn.
            cell_size (int): Width and height in pixels of each cell.
            color_map (dict[int, tuple[int, int, int]]): Maps cell states to RGB
                colors.
        """
        for row in range(grid.rows):
            for column in range(grid.columns):
                value = grid.cells[row][column]
                color = color_map[value]

                rect = pg.Rect(
                    column * cell_size,
                    row * cell_size,
                    cell_size,
                    cell_size,
                )
                pg.draw.rect(self.screen, color, rect)

    def present(self) -> None:
        """Flips the display buffer, showing the current frame."""
        pg.display.flip()

    def quit(self) -> None:
        """Shuts down pygame."""
        pg.quit()
