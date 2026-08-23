"""Module for pygame window setup and rendering."""

import pygame as pg

from src.my_project.config_model import ConfigModel
from src.my_project.utils.utils_pygame import get_window_size_from_screen_resolution
from src.my_project.grid import Grid


class Renderer:
    """Manages the pygame window and draws each frame."""

    def __init__(self, config: ConfigModel) -> None:
        """Initializes the renderer with configuration.

        Args:
            config (ConfigModel): Pydantic-validated configuration model.
        """
        self.window_background_color = config.window.background_color
        self.grid_color_map = config.grid.color_map
        self.cell_size = config.grid.cell_size
        window_caption = config.window.caption

        pg.init()

        width, height = get_window_size_from_screen_resolution()
        self.screen = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()

        pg.display.set_caption(window_caption)

    def tick(self, fps: int) -> float:
        """Advances the frame clock and reports the elapsed time.

        Args:
            fps (int): Target frames per second to cap the loop at.

        Returns:
            dt (float): Time in seconds elapsed since the last frame.
        """
        dt = self.clock.tick(fps) / 1000

        return dt

    def render_grid(
        self,
        grid: Grid,
    ) -> None:
        """Draws every cell of the grid onto the display surface.

        Args:
            grid (Grid): The grid whose cells will be drawn.
        """
        for row in range(grid.num_rows):
            for column in range(grid.num_cols):
                value = grid.cells[row][column]
                color = self.grid_color_map[value]

                rect = pg.Rect(
                    column * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pg.draw.rect(self.screen, color, rect)

    def render(self, grid: Grid) -> None:
        """Draws the current frame and presents it to the display.

        1. Fill the screen with the window background color.
        2. Draw the grid on top.
        3. Flip the display buffer to show the frame.

        Args:
            grid (Grid): The grid whose cells will be drawn.
        """
        self.screen.fill(self.window_background_color)
        self.render_grid(grid=grid)
        pg.display.flip()

    def quit(self) -> None:
        """Shuts down pygame."""
        pg.quit()
