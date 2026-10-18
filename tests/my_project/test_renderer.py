"""Module for testing renderer.py"""

import logging

import pygame as pg
import pytest

from my_project.config_model import ConfigModel
from my_project.constants import Position, Size
from my_project.grid import Grid
from my_project.renderer import Renderer


def _config(show_gridlines=False):
    """Builds a ConfigModel with a 4x4 grid and a small margin.

    Args:
        show_gridlines (bool): Whether the grid lines are drawn.
    """

    config_data = {
        "game": {"fps": 60},
        "window": {
            "caption": "Renderer Test",
            "background_color": [10, 20, 30],
            "margin_size": 5,
        },
        "grid": {
            "dim": 4,
            "color_map": {0: [0, 0, 0], 1: [255, 255, 255]},
            "show_gridlines": show_gridlines,
            "grid_line_color": [50, 50, 50],
            "grid_line_width": 2,
        },
    }

    config = ConfigModel.model_validate(config_data)

    return config


def _renderer(monkeypatch, show_gridlines=False):
    """Creates a Renderer with a fixed window size, so the tests do not depend on the desktop.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest's patching helper.
        show_gridlines (bool): Whether the grid lines are drawn.
    """

    def fixed_window_size():
        size = (400, 300)

        return size

    monkeypatch.setattr(
        "my_project.renderer.get_window_size_from_screen_resolution", fixed_window_size
    )

    config = _config(show_gridlines=show_gridlines)

    renderer = Renderer(config=config)

    return renderer


@pytest.fixture(scope="function", name="renderer")
def fixture_renderer(monkeypatch):
    """Creates a renderer with grid lines hidden, and closes the window afterwards."""
    renderer = _renderer(monkeypatch)

    yield renderer

    renderer.quit()


# Testing the "__init__" method from the "Renderer" class.


def test_init_opens_window_with_config_values(renderer):
    """The window has the requested size, caption, and config values."""
    assert isinstance(renderer.screen_size, Size)
    assert renderer.screen.get_size() == tuple(renderer.screen_size)
    assert renderer.window_background_color == [10, 20, 30]
    assert renderer.margin_size == 5
    assert renderer.grid_dim == 4
    assert pg.display.get_caption()[0] == "Renderer Test"


def test_init_snaps_cells_to_whole_pixels_and_logs_it(monkeypatch, caplog):
    """Cell size becomes a whole number of pixels, and the window size change is logged."""
    caplog.set_level(logging.INFO)

    renderer = _renderer(monkeypatch)

    assert isinstance(renderer.cell_size, int)
    assert renderer.grid_size == renderer.cell_size * renderer.grid_dim
    assert "cell-size snapping" in caplog.text

    renderer.quit()


# Testing the "_snap_to_pixel_grid" method from the "Renderer" class.


def test_snap_to_pixel_grid_keeps_whole_pixel_cells_unchanged(renderer):
    """Cells that are already a whole number of pixels are not resized."""
    cell_size = renderer.cell_size
    margin_size = renderer.margin_size

    renderer._snap_to_pixel_grid()

    assert renderer.cell_size == cell_size
    assert renderer.margin_size == margin_size


# Testing the "tick" method from the "Renderer" class.


def test_tick_returns_elapsed_seconds(renderer):
    """The elapsed time is returned in seconds."""
    dt = renderer.tick(60)

    assert isinstance(dt, float)
    assert dt >= 0


# Testing the "render_grid" method from the "Renderer" class.


def test_render_grid_colors_each_cell_by_its_state(renderer):
    """A cell with state one is drawn in its mapped color."""
    config = _config()
    grid = Grid(config=config)
    position = Position(x=0, y=0)
    grid.set_cell(position=position, value=1)

    renderer.render_grid(grid=grid)

    center = int(renderer.margin_size + renderer.cell_size // 2)
    pixel = renderer.screen.get_at((center, center))

    assert tuple(pixel)[:3] == (255, 255, 255)


# Testing the "render" method from the "Renderer" class.


def test_render_fills_screen_with_background(renderer):
    """The frame is filled with the background color around the grid."""
    config = _config()
    grid = Grid(config=config)

    renderer.render(grid=grid)

    pixel = renderer.screen.get_at((0, 0))

    assert tuple(pixel)[:3] == (10, 20, 30)


def test_render_draws_grid_lines_when_enabled(monkeypatch):
    """With grid lines enabled, a line is drawn over the top edge of the grid."""
    renderer = _renderer(monkeypatch, show_gridlines=True)
    config = _config()
    grid = Grid(config=config)

    renderer.render(grid=grid)

    edge_x = int(renderer.margin_size + renderer.cell_size // 2)
    edge_y = int(renderer.margin_size)
    pixel = renderer.screen.get_at((edge_x, edge_y))

    assert tuple(pixel)[:3] == (50, 50, 50)

    renderer.quit()


def test_render_skips_grid_lines_when_disabled(renderer):
    """With grid lines disabled, the top edge of the grid stays the cell color."""
    config = _config()
    grid = Grid(config=config)

    renderer.render(grid=grid)

    edge_x = int(renderer.margin_size + renderer.cell_size // 2)
    edge_y = int(renderer.margin_size)
    pixel = renderer.screen.get_at((edge_x, edge_y))

    assert tuple(pixel)[:3] == (0, 0, 0)


# Testing the "quit" method from the "Renderer" class.


def test_quit_shuts_down_pygame(renderer):
    """Quitting shuts down the pygame display."""
    renderer.quit()

    assert pg.display.get_init() is False
