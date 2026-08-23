"""Module for the 2D grid data structure used in cellular automata and grid
visualizations.
"""

from collections import namedtuple

import random as rd

Position = namedtuple("Position", ["row", "column"])


class Grid:
    """Holds and manipulates a 2D grid of cell states."""

    def __init__(self, rows: int, columns: int, fill_value: int = 0) -> None:
        """Initializes an empty grid filled with a constant value.

        Args:
            rows (int): Number of rows in the grid.
            columns (int): Number of columns in the grid.
            fill_value (int): Initial value assigned to every cell.
        """
        self.rows = rows
        self.columns = columns

        cells: list[list[int]] = [
            [fill_value for _ in range(columns)] for _ in range(rows)
        ]
        self.cells = cells

    def get_cell(self, position: Position) -> int:
        """Returns the state of the cell at the given position.

        Args:
            position (Position): Row/column coordinate to read.

        Returns:
            value (int): The state stored at that position.
        """
        value = self.cells[position.row][position.column]

        return value

    def set_cell(self, position: Position, value: int) -> None:
        """Sets the state of the cell at the given position.

        Args:
            position (Position): Row/column coordinate to write.
            value (int): The new state to store at that position.
        """
        self.cells[position.row][position.column] = value

    def randomize(self, values: list[int]) -> None:
        """Fills the grid with random values drawn from the given options.

        Args:
            values (list[int]): Pool of possible cell states to sample from.
        """
        for row in range(self.rows):
            for column in range(self.columns):
                self.cells[row][column] = rd.choice(values)

    def get_neighbors(self, position: Position) -> list[Position]:
        """Returns the in-bounds Moore neighborhood of a position.

        Args:
            position (Position): Row/column coordinate to inspect.

        Returns:
            neighbors (list[Position]): Up to eight surrounding positions.
        """
        neighbors: list[Position] = []

        for row_offset in (-1, 0, 1):
            for column_offset in (-1, 0, 1):
                if row_offset == 0 and column_offset == 0:
                    continue

                neighbor_row = position.row + row_offset
                neighbor_column = position.column + column_offset

                is_in_bounds = (
                    0 <= neighbor_row < self.rows
                    and 0 <= neighbor_column < self.columns
                )

                if is_in_bounds:
                    neighbors.append(Position(neighbor_row, neighbor_column))

        return neighbors
