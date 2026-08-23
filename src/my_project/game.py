"""Module for game logic and orchestration of the main loop."""

import sys

import pygame as pg

from src.my_project.config_model import ConfigModel
from src.my_project.constants import GRID_COLOR_MAP, FPS
from src.my_project.grid import Grid
from src.my_project.renderer import Renderer


class Game:
    """Manages game state and orchestrates the main loop."""

    def __init__(self, config: ConfigModel) -> None:
        """Initializes the game with configuration and state.

        Args:
            config (ConfigModel): Pydantic-validated configuration model.
        """
        self.config = config

        # State
        self.running: bool = False
        self.grid: Grid
        self.renderer: Renderer

    def _setup(self) -> None:
        """Initializes the grid, renderer, and marks the game as running."""
        grid_config = self.config.grid

        self.grid = Grid(rows=grid_config.num_rows, columns=grid_config.num_columns)
        self.grid.randomize([0, 1])

        width = grid_config.num_columns * grid_config.cell_size
        height = grid_config.num_rows * grid_config.cell_size

        self.renderer = Renderer(self.config)
        self.renderer.setup(width, height)

        self.running = True

    def _handle_events(self) -> None:
        """Processes pending pygame events, including quit and key presses."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False

    def _update(self, dt: float) -> None:
        """Advances game state for the current frame.

        Args:
            dt (float): Time in seconds elapsed since the last frame.
        """
        pass

    def _loop(self) -> None:
        """Runs the main loop: handle input, update state, render frame."""
        while self.running:
            dt = self.renderer.tick(FPS)

            self._handle_events()
            self._update(dt)

            self.renderer.clear()
            cell_size = self.config.grid.cell_size
            self.renderer.render_grid(self.grid, cell_size, GRID_COLOR_MAP)
            self.renderer.present()

    def _quit(self) -> None:
        """Shuts down the renderer and exits the process cleanly."""
        self.renderer.quit()
        sys.exit()

    def run(self) -> None:
        """Orchestrates setup, main loop, and clean shutdown.

        1. Initialize the grid, renderer, and game state.
        2. Run the main loop until the game stops running.
        3. Shut down pygame and exit the process cleanly.
        """
        self._setup()
        self._loop()
        self._quit()
