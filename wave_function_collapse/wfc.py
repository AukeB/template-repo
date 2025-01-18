import random as rd
import copy
import time
from collections import Counter, defaultdict
from visualize import WFCVisualizer
from constants import Size


class WaveFunctionCollapse:
    """ """

    def __init__(
        self,
        bitmap: list[list[str]],
        grid_dimensions: Size,
        tile_dimensions: Size,
        color_mapping: dict,
    ) -> None:
        """ """
        self.bitmap = bitmap
        self.bitmap_dimensions = Size(len(self.bitmap[0]), len(self.bitmap))
        self.grid_dimensions = grid_dimensions
        self.tile_dimensions = tile_dimensions
        self.grid = [
            [None for _ in range(grid_dimensions.width)] for _ in range(grid_dimensions.height)
        ]
        self._check_tile_and_bitmap_dimensions()
        self.tile_weights, self.adjacency = self.compute_tile_set_and_rules()
        self.entropy_grid = self.initialize_entropy()
        self.directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1),
        }

        self.wfc_visualizer = WFCVisualizer(
            grid_dimensions=self.grid_dimensions,
            tile_dimensions=tile_dimensions,
            color_mapping=color_mapping,
        )

        # self.wfc_visualizer.show_unique_tiles(self.tile_weights)
        # self.wfc_visualizer.show_adjacency(self.adjacency)

    def _check_tile_and_bitmap_dimensions(self):
        min_bitmap_dim = min(self.bitmap_dimensions.width, self.bitmap_dimensions.height)
        if (
            self.tile_dimensions.width > min_bitmap_dim
            or self.tile_dimensions.height > min_bitmap_dim
        ):
            raise ValueError(
                f"tile_size ({self.tile_size}) must be smaller than or equal to the "
                f"minimum dimension of the bitmap (width: {self.bitmap_dimensions.width}, "
                f"height: {self.bitmap_dimensions.height})"
            )

    def _extract_tile(self, x, y):
        """ """
        return tuple(
            tuple(self.bitmap[y + i][x + j] for j in range(self.tile_dimensions.width))
            for i in range(self.tile_dimensions.height)
        )

    def _compute_weights(self, tile_count):
        total_occurrences = sum(tile_count.values())
        tile_weights = {tile: count / total_occurrences for tile, count in tile_count.items()}
        return tile_weights

    def compute_tile_set_and_rules(
        self,
        step_size: int = 1,
    ) -> None:
        """ """
        tile_count = Counter()
        adjacency = defaultdict(lambda: defaultdict(set))
        rows, cols = self.bitmap_dimensions.width, self.bitmap_dimensions.height

        for y in range(1, rows - self.tile_dimensions.height + 1 - 1, step_size):
            for x in range(1, cols - self.tile_dimensions.width + 1 - 1, step_size):
                tile = self._extract_tile(x, y)
                tile_count[tile] += 1

                if x >= self.tile_dimensions.width:
                    adjacency[tile]["left"].add(
                        self._extract_tile(x - self.tile_dimensions.width, y)
                    )
                if x <= cols - 2 * self.tile_dimensions.width:
                    adjacency[tile]["right"].add(
                        self._extract_tile(x + self.tile_dimensions.width, y)
                    )
                if y >= self.tile_dimensions.height:
                    adjacency[tile]["up"].add(
                        self._extract_tile(x, y - self.tile_dimensions.height)
                    )
                if y <= rows - 2 * self.tile_dimensions.height:
                    adjacency[tile]["down"].add(
                        self._extract_tile(x, y + self.tile_dimensions.height)
                    )

        tile_weights = self._compute_weights(tile_count)

        return tile_weights, adjacency

    def initialize_entropy(
        self,
    ) -> list[list[str]]:
        """ """
        # Initially, every tile is in a superposition of all elements
        # of the set of all posssible tile values.
        tile_set = set(self.tile_weights.keys())
        entropy = [
            [copy.deepcopy(tile_set) for _ in range(self.grid_dimensions.width)]
            for _ in range(self.grid_dimensions.height)
        ]
        return entropy

    def propagate(
        self,
        y: int,
        x: int,
        tile: str,
    ) -> None:
        """ """
        for direction, (dy, dx) in self.directions.items():
            ny, nx = y + dy, x + dx
            if 0 <= nx < self.grid_dimensions.width and 0 <= ny < self.grid_dimensions.height and self.grid[ny][nx] is None:
                self.wfc_visualizer.visualize(self.grid, self.entropy_grid)
                #time.sleep(2)
                valid_tiles = self.adjacency.get(tile, {}).get(direction, set())
                self.entropy_grid[ny][nx] &= valid_tiles


    def collapse(
        self,
    ) -> None:
        """ """
        while True:
            min_entropy = float("inf")
            min_cell = None

            for y in range(self.grid_dimensions.width):
                for x in range(self.grid_dimensions.height):
                    if self.grid[y][x] is None:
                        options = self.entropy_grid[y][x]

                        if len(options) < min_entropy:
                            min_entropy = len(options)
                            min_cell = (y, x)

            if min_cell is None: # Necessary?
               break

            # Collapse the wave function
            y, x = min_cell
            choices = list(self.entropy_grid[y][x])
            weights = [self.tile_weights[tile] for tile in choices]
            chosen_tile = rd.choices(choices, weights)[0]
            self.grid[y][x] = chosen_tile
            self.propagate(y, x, chosen_tile)