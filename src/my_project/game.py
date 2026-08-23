"""Module for the main game loop and pygame window management."""

import sys

import pygame as pg

from src.my_project.config_model import ConfigModel
from src.my_project.constants import FPS, WINDOW_CAPTION, BACKGROUND_COLOR
from src.my_project.utils.utils_pygame import get_window_size_from_screen_resolution


class Game:
    """Manages the pygame window, event loop, and game state."""

    def __init__(self, config: ConfigModel) -> None:
        """Initializes the game with configuration and pygame state.

        Args:
            config (ConfigModel): Pydantic-validated configuration model.
        """
        self.config = config

        # State
        self.running: bool = False
        self.screen: pg.Surface
        self.clock: pg.time.Clock

    def _setup(self) -> None:
        """Initializes pygame, the display window, and the frame clock."""
        pg.init()
        width, height = get_window_size_from_screen_resolution()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(WINDOW_CAPTION)
        self.clock = pg.time.Clock()
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

    def _render(self) -> None:
        """Draws the current frame to the display surface."""
        self.screen.fill(BACKGROUND_COLOR)
        pg.display.flip()

    def _loop(self) -> None:
        """Runs the event loop, updating and rendering each frame."""
        while self.running:
            # Seconds since last frame, capped at FPS
            delta_time = self.clock.tick(FPS) / 1000

            self._handle_events()
            self._update(dt=delta_time)
            self._render()

    def _quit(self) -> None:
        """Shuts down pygame and exits the process cleanly."""
        pg.quit()
        sys.exit()

    def run(self) -> None:
        """Orchestrates game setup and runs the main loop until exit.

        1. Initialize pygame and create the display surface.
        2. Run the event loop, handling input, updating state, and rendering
           each frame.
        3. Shut down pygame and exit the process cleanly.
        """
        self._setup()
        self._loop()
        self._quit()
