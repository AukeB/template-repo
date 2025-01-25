""" """

from constants import Size


class DiamondSquare:
    """ """

    def __init__(
        self,
        grid_dimensions: Size,
    ) -> None:
        self.grid_dimensions = grid_dimensions
        self.corner_names = ["top_left", "top_right", "bottom_left", "bottom_right"]
        self.grid = [
            [None for _ in range(grid_dimensions.width)] for _ in range(grid_dimensions.height)
        ]

        self.corner_values = self.determine_corner_values(mode="one_value", value=10)

    def determine_corner_values(self, mode: str, value: int) -> dict[str, float]:
        """ """
        if mode == "one_value":
            if not isinstance(value, (int, float)):
                raise TypeError(
                    f"Expected 'value' to be of type int or float when mode is 'one_value', but got {type(value).__name__}."
                )
            return {key: value for key in self.corner_names}

    def initialise_corners(
        self,
    ) -> None:
        """ """
        if not self.corner_values:
            raise ValueError("Corners can not be initialised. Corners values have not been set yet")

        self.grid[0][0] = self.corner_values[self.corner_names[0]]
        self.grid[0][-1] = self.corner_values[self.corner_names[1]]
        self.grid[-1][0] = self.corner_values[self.corner_names[2]]
        self.grid[-1][-1] = self.corner_values[self.corner_names[3]]

    def find_all_squares(
        self,
    ) -> set[tuple[tuple[int, int]]]:
        """
        Find all valid squares in the grid, regardless of step size. A square is valid
        only if all four corners are not None.

        Args:
            grid (list of list): The 2D grid representing the array.

        Returns:
            set of tuple: A set of unique squares, each represented as a tuple
                of corner coordinates (top-left, top-right, bottom-left, bottom-right).
        """
        square_coordinates = set()
        rows = self.grid_dimensions.height
        cols = self.grid_dimensions.width

        max_step_size = min(rows, cols)

        for step_size in range(1, max_step_size):
            for row in range(0, rows - step_size):
                for col in range(0, cols - step_size):
                    top_left = (row, col)
                    top_right = (row, col + step_size)
                    bottom_left = (row + step_size, col)
                    bottom_right = (row + step_size, col + step_size)

                    if (
                        self.grid[top_left[0]][top_left[1]] is not None
                        and self.grid[top_right[0]][top_right[1]] is not None
                        and self.grid[bottom_left[0]][bottom_left[1]] is not None
                        and self.grid[bottom_right[0]][bottom_right[1]] is not None
                    ):
                        square_coordinates.add((top_left, top_right, bottom_left, bottom_right))

        return square_coordinates

    def calculate_midpoint(
        self,
        square: tuple[tuple[int, int]],
    ) -> tuple[int, int]:
        """
        Calculate the midpoint of a square defined by four corner coordinates.

        Args:
            square (tuple): A tuple containing the four corners of the square.

        Returns:
            tuple: The midpoint (x, y) of the square.
        """
        top_left, top_right, bottom_left, bottom_right = square
        row1, col1 = top_left
        row2, col2 = top_right
        row3, col3 = bottom_left
        row4, col4 = bottom_right

        mid_x = int((row1 + row2 + row3 + row4) / 4)
        mid_y = int((col1 + col2 + col3 + col4) / 4)

        return (mid_x, mid_y)

    def squares_to_midpoints(self, square_coordinates: set[tuple[tuple[int, int]]]):
        """
        Given a set of squares, calculate the midpoint for each and store in a dictionary.

        Args:
            squares (set): A set of squares represented by tuples of four corner coordinates.

        Returns:
            dict: A dictionary where keys are the square coordinates and values are the midpoints.
        """
        midpoint_coordinates = {}

        for square in square_coordinates:
            midpoint = self.calculate_midpoint(square)
            midpoint_coordinates[square] = midpoint

        return midpoint_coordinates

    def compute_midpoint_values(self, square_and_midpoint_coordinates) -> dict:
        """
        Create a dictionary with the midpoint as key and the average of the four corners
        as value for each square.

        Args:
            squares (set): A set of squares represented by tuples of four corner coordinates.
            grid (list of list): The 2D grid representing the array.

        Returns:
            dict: A dictionary with the midpoint as the key and the average value of the corners as the value.
        """
        midpoint_coordinates_and_values = {}

        for square_coordinates, midpoint_coordinates in square_and_midpoint_coordinates.items():
            top_left, top_right, bottom_left, bottom_right = square_coordinates
            values = [
                self.grid[top_left[0]][top_left[1]],
                self.grid[top_right[0]][top_right[1]],
                self.grid[bottom_left[0]][bottom_left[1]],
                self.grid[bottom_right[0]][bottom_right[1]],
            ]

            avg_value = sum(values) / 4
            midpoint_coordinates_and_values[midpoint_coordinates] = avg_value

        return midpoint_coordinates_and_values

    def set_values(self, midpoint_coordinates_and_values: dict[tuple, float]) -> None:
        for midpoint_coordinates, midpoint_value in midpoint_coordinates_and_values.items():
            x, y = midpoint_coordinates[0], midpoint_coordinates[1]
            self.grid[x][y] = midpoint_value

    def perform_diamond_step(
        self,
    ) -> None:
        """ """
        square_coordinates = self.find_all_squares()
        square_and_midpoint_coordinates = self.squares_to_midpoints(square_coordinates)
        midpoint_coordinates_and_values = self.compute_midpoint_values(
            square_and_midpoint_coordinates
        )
        self.set_values(midpoint_coordinates_and_values)

    def execute(
        self,
    ):
        """ """
        self.initialise_corners()

        for row in self.grid:
            print(row)

        self.perform_diamond_step()
        print()

        for row in self.grid:
            print(row)
