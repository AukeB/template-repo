"""Module for testing grid.py"""

from my_project.config_model import ConfigModel
from my_project.constants import Dimensions, Position
from my_project.grid import Grid


def _config(dim):
    """Builds a ConfigModel with a grid of the given size.

    Args:
        dim (int): Number of cells along each side of the grid.
    """

    config_data = {
        "game": {"fps": 60},
        "window": {
            "caption": "Grid Test",
            "background_color": [0, 0, 0],
            "margin_size": 5,
        },
        "grid": {
            "dim": dim,
            "color_map": {0: [0, 0, 0], 1: [255, 255, 255]},
            "show_gridlines": False,
            "grid_line_color": [50, 50, 50],
            "grid_line_width": 2,
        },
    }

    config = ConfigModel.model_validate(config_data)

    return config


# Testing the "__init__" method from the "Grid" class.


def test_init_creates_square_grid_of_zeros():
    """A new grid is square and every cell is zero."""
    config = _config(dim=3)
    grid = Grid(config=config)

    expected = Dimensions(rows=3, cols=3)

    assert grid.dimensions == expected
    assert grid.cells == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


# Testing the "set_cell" method from the "Grid" class.


def test_set_cell_writes_column_and_row_in_the_right_place():
    """The x coordinate maps to the column and the y coordinate maps to the row."""
    config = _config(dim=3)
    grid = Grid(config=config)

    position = Position(x=2, y=1)

    grid.set_cell(position, 5)

    assert grid.cells == [[0, 0, 0], [0, 0, 5], [0, 0, 0]]


# Testing the "randomize" method from the "Grid" class.


def test_randomize_uses_zero_and_one_by_default():
    """Without options, every cell is either zero or one."""
    config = _config(dim=5)
    grid = Grid(config=config)

    grid.randomize()

    assert all(value in (0, 1) for row in grid.cells for value in row)


def test_randomize_draws_from_given_values():
    """Only the given values are used when they are passed in."""
    config = _config(dim=4)
    grid = Grid(config=config)

    grid.randomize(values=[7])

    assert all(value == 7 for row in grid.cells for value in row)
