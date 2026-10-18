"""Module for testing renderer.py"""

import pygame as pg
import pytest

from my_project.config_model import ConfigModel
from my_project.constants import Size
from my_project.renderer import Renderer


@pytest.fixture(scope="function", name="renderer")
def fixture_renderer(monkeypatch):
    """Creates a Renderer with a fixed window size, so the tests do not depend on the desktop."""

    def fixed_window_size():
        size = (400, 300)

        return size

    monkeypatch.setattr(
        "my_project.renderer.get_window_size_from_screen_resolution", fixed_window_size
    )

    config_data = {
        "game": {"fps": 60},
        "window": {
            "caption": "Renderer Test",
            "background_color": [10, 20, 30],
            "margin_size": 5,
        },
    }

    config = ConfigModel.model_validate(config_data)

    renderer = Renderer(config=config)

    yield renderer

    renderer.quit()


# Testing the "__init__" method from the "Renderer" class.


def test_init_opens_window_with_config_values(renderer):
    """The window has the requested size, caption, and config values."""
    assert renderer.screen_size == Size(400, 300)
    assert renderer.screen.get_size() == (400, 300)
    assert renderer.window_background_color == [10, 20, 30]
    assert renderer.margin_size == 5
    assert pg.display.get_caption()[0] == "Renderer Test"


# Testing the "tick" method from the "Renderer" class.


def test_tick_returns_elapsed_seconds(renderer):
    """The elapsed time is returned in seconds."""
    dt = renderer.tick(60)

    assert isinstance(dt, float)
    assert dt >= 0


# Testing the "render" method from the "Renderer" class.


def test_render_fills_screen_with_background(renderer):
    """The frame is filled with the background color."""
    renderer.render()

    pixel = renderer.screen.get_at((0, 0))

    assert tuple(pixel)[:3] == (10, 20, 30)


# Testing the "quit" method from the "Renderer" class.


def test_quit_shuts_down_pygame(renderer):
    """Quitting shuts down the pygame display."""
    renderer.quit()

    assert pg.display.get_init() is False
