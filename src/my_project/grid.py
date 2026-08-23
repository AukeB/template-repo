"""Module for the 2D grid data structure used in cellular automata and grid
visualizations.
"""

import random as rd

from src.my_project.config_model import ConfigModel
from src.my_project.constants import Position

class Grid:
    """Holds and manipulates a 2D grid of cell states."""

    def __init__(self, config: ConfigModel) -> None:
        """Initializes an empty grid filled with a constant value."""

        self.num_rows = config.grid.num_rows
        self.num_cols = config.grid.num_cols
        self.grid_background_color = config.grid.background_color

        self.cells: list[list[int]] = [
            [0 for _ in range(self.num_cols)] for _ in range(self.num_rows)
        ]

    def set_cell(self, position: Position, value: int) -> None:
        """Sets the state of the cell at the given position.

        Args:
            position (Position): Row/column coordinate to write.
            value (int): The new state to store at that position.
        """
        self.cells[position.y][position.x] = value

    def randomize(self, values: list[int]) -> None:
        """Fills the grid with random values drawn from the given options.

        Args:
            values (list[int]): Pool of possible cell states to sample from.
        """
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.cells[row][column] = rd.choice(values)