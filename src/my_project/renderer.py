"""Module for pygame window setup and rendering."""

import logging

import pygame as pg

from my_project.config_model import ConfigModel
from my_project.constants import Size
from my_project.grid import Grid
from my_project.utils.utils_pygame import get_window_size_from_screen_resolution

logger = logging.getLogger(__name__)


class Renderer:
    """Manages the pygame window and draws each frame.

    Attributes:
        window_background_color (list[int]): RGB color that fills the window.
        margin_size (int): Margin around the grid, in pixels.
        grid_color_map (dict[int, list[int]]): RGB color for each cell state.
        show_gridlines (bool): Whether grid lines are drawn over the cells.
        grid_line_color (list[int]): RGB color of the grid lines.
        grid_line_width (int): Width of the grid lines, in pixels.
        grid_dim (int): Number of cells along each side of the grid.
        screen_size (Size): Width and height of the window, in pixels.
        grid_size (int): Side length of the square grid, in pixels.
        cell_size (int): Side length of one cell, in pixels.
        screen (pg.Surface): The display surface that frames are drawn on.
        clock (pg.time.Clock): Clock that caps the frame rate.

    Example:
        renderer = Renderer(config=config) dt = renderer.tick(60)
    """

    def __init__(self, config: ConfigModel) -> None:
        """Initializes the renderer with configuration.

        Args:
            config (ConfigModel): Pydantic-validated configuration model.
        """

        self.window_background_color = config.window.background_color
        self.margin_size = config.window.margin_size
        self.grid_color_map = config.grid.color_map
        self.show_gridlines = config.grid.show_gridlines
        self.grid_line_color = config.grid.grid_line_color
        self.grid_line_width = config.grid.grid_line_width
        self.grid_dim = config.grid.dim
        window_caption = config.window.caption

        pg.init()

        # Get screen size, but don't open the PyGame display yet. Cell size is
        # a function of grid dimensions and window-grid margin, and is rarely
        # a whole number of pixels — pygame's Rect truncates float dimensions,
        # which leaves sub-pixel gaps between cells, visible as thin horizontal
        # and vertical lines. The block below snaps cell size to an integer
        # pixel and rescales window size accordingly before the display opens.
        window_size = get_window_size_from_screen_resolution()
        self.screen_size = Size(*window_size)

        # Grid is always square: sized from the smaller of the two
        # margin-adjusted screen dimensions, and hugs the top-left corner.
        self.grid_size = min(
            self.screen_size.width - 2 * self.margin_size,
            self.screen_size.height - 2 * self.margin_size,
        )

        self.cell_size = self.grid_size / self.grid_dim

        self._snap_to_pixel_grid()

        self.screen = pg.display.set_mode(
            (self.screen_size.width, self.screen_size.height)
        )

        self.clock = pg.time.Clock()

        pg.display.set_caption(window_caption)

    def _snap_to_pixel_grid(self) -> None:
        """Snaps cell size to the nearest integer pixel.

        PyGame's Rect silently truncates float dimensions to integers on
        construction, which causes sub-pixel gaps to accumulate across rows and
        columns during rendering. Window size and margin are rescaled by the
        same ratio so the grid still fills the available space exactly, with no
        leftover gap on any edge. The resulting window size adjustment is logged
        at INFO level.
        """

        original_screen_size = self.screen_size

        snap_ratio = round(self.cell_size) / self.cell_size
        self.cell_size = round(self.cell_size)
        self.margin_size = round(self.margin_size * snap_ratio)

        snapped_width = round(self.screen_size.width * snap_ratio)
        snapped_height = round(self.screen_size.height * snap_ratio)
        self.screen_size = Size(snapped_width, snapped_height)
        self.grid_size = self.cell_size * self.grid_dim

        adjustment_pct = (snap_ratio - 1) * 100

        logger.info(
            "[cell-size snapping] window size adjusted from [%d, %d] to [%d, %d] "
            "(%+.2f%%) to keep cells pixel-aligned",
            original_screen_size.width,
            original_screen_size.height,
            self.screen_size.width,
            self.screen_size.height,
            adjustment_pct,
        )

    def tick(self, fps: int) -> float:
        """Advances the frame clock and reports the elapsed time.

        Args:
            fps (int): Target frames per second to cap the loop at.

        Returns:
            dt (float): Time in seconds elapsed since the last frame.
        """

        dt = self.clock.tick(fps) / 1000

        return dt

    def _draw_grid_lines(self) -> None:
        """Draws horizontal and vertical grid lines across the grid area."""

        grid_end = int(self.margin_size + self.grid_size)

        for row in range(self.grid_dim + 1):
            y = int(self.margin_size + row * self.cell_size)
            start = (self.margin_size, y)
            end = (grid_end, y)

            pg.draw.line(
                self.screen, self.grid_line_color, start, end, self.grid_line_width
            )

        for col in range(self.grid_dim + 1):
            x = int(self.margin_size + col * self.cell_size)
            start = (x, self.margin_size)
            end = (x, grid_end)

            pg.draw.line(
                self.screen, self.grid_line_color, start, end, self.grid_line_width
            )

    def render_grid(self, grid: Grid) -> None:
        """Draws every cell of the grid onto the display surface.

        Args:
            grid (Grid): The grid whose cells will be drawn.
        """

        for row in range(grid.dimensions.rows):
            for col in range(grid.dimensions.cols):
                value = grid.cells[row][col]
                color = self.grid_color_map[value]

                rect = pg.Rect(
                    self.margin_size + col * self.cell_size,
                    self.margin_size + row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )

                pg.draw.rect(self.screen, color, rect)

    def render(self, grid: Grid) -> None:
        """Draws the current frame and presents it to the display.

        1. Fill the screen with the window background color.
        2. Draw the grid cells on top.
        3. Draw the grid lines.
        4. Flip the display buffer to show the frame.

        Args:
            grid (Grid): The grid whose cells will be drawn.
        """

        self.screen.fill(self.window_background_color)
        self.render_grid(grid=grid)

        if self.show_gridlines:
            self._draw_grid_lines()

        pg.display.flip()

    def quit(self) -> None:
        """Shuts down pygame."""

        pg.quit()
