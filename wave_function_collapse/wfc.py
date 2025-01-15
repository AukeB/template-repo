import pygame as pg
import random as rd
import time
from PIL import Image, ImageDraw
from collections import namedtuple, Counter
from game import WFCVisualizer

Grid = namedtuple('Grid', ['width', 'height'])

class WaveFunctionCollapse():
    """ """
    def __init__(
        self,
        bitmap: list[list[str]],
        grid_size: Grid,
        tile_size: int,
        color_mapping: dict,
    ) -> None:
        """ """
        self.bitmap = bitmap
        self.bitmap_size = Grid(len(self.bitmap), len(self.bitmap[0]))
        self.grid_size = grid_size
        self.tile_size = tile_size
        self.color_mapping = color_mapping
        self.wave = [[None for _ in range(grid_size.width)] for _ in range(grid_size.height)]
        self._check_tile_and_bitmap_size()
        self.tile_set, self.tile_weights, self.adjacency_rules = self.compute_tile_set_and_rules()
        self.entropy_grid = self.initialize_entropy()
        self.directions = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

        self.wfc_visualizer = WFCVisualizer(
            grid_dimensions=self.grid_size,
            tile_dimensions=Grid(self.tile_size, self.tile_size),
            color_mapping=self.color_mapping
        )

    def _check_tile_and_bitmap_size(self):
        if self.tile_size > min(self.bitmap_size.width, self.bitmap_size.height):
            raise ValueError(
                f"tile_size ({self.tile_size}) must be smaller than or equal to the " 
                f"minimum dimension of the bitmap (width: {self.bitmap_size.width}, " 
                f"height: {self.bitmap_size.height})"
            )

    def _extract_tile(self, x, y):
        """ """
        tile = []

        for i in range(self.tile_size):
            for j in range(self.tile_size):
                tile.append(self.bitmap[y + i][x + j])

        return tuple(tile)
    
    def _compute_weights(self, tile_set, tile_count):
        total_occurrences = sum(tile_count.values())
        weights = {}

        for tile in tile_set:
            occurrence = tile_count.get(tile, 0)
            weight = occurrence / total_occurrences
            weights[tile] = weight

        weights[('Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z')] = 0.001
        
        return weights

    def compute_tile_set_and_rules(
        self,
        step_size: int=1,
    ) -> None:
        """ """
        tile_set = set()
        tile_count = Counter()
        adjacency = {}
        rows, cols = self.bitmap_size.width, self.bitmap_size.height

        for y in range(0, rows - self.tile_size + 1, step_size):
            for x in range(0, cols - self.tile_size + 1, step_size):
                tile = self._extract_tile(x, y)
                tile_set.add(tile)
                tile_count[tile] += 1

                if tile not in adjacency:
                    adjacency[tile] = {}

                if x >= self.tile_size:
                    if "left" not in adjacency[tile]:
                        adjacency[tile]["left"] = set()
                    adjacency[tile]["left"].add(self._extract_tile(x-self.tile_size, y))
                if x <= cols - 2*self.tile_size:
                    if "right" not in adjacency[tile]:
                        adjacency[tile]["right"] = set()
                    adjacency[tile]["right"].add(self._extract_tile(x+self.tile_size, y))
                if y >= self.tile_size:
                    if "up" not in adjacency[tile]:
                        adjacency[tile]["up"] = set()
                    adjacency[tile]["up"].add(self._extract_tile(x, y-self.tile_size))
                if y <= rows - 2*self.tile_size:
                    if "down" not in adjacency[tile]:
                        adjacency[tile]["down"] = set()
                    adjacency[tile]["down"].add(self._extract_tile(x, y+self.tile_size))

        tile_weights = self._compute_weights(tile_set, tile_count)

        return tile_set, tile_weights, adjacency

    def initialize_entropy(
        self,
    ) -> list[list[str]]:
        """ """
        # Initially, every tile is in a superposition consisting of the set of all posssible tile values.
        entropy_grid = [[self.tile_set for _ in range(self.grid_size.width)] for _ in range(self.grid_size.height)]
        return entropy_grid
    
    def propagate(
        self,
        y: int,
        x: int,
        tile: str,
    ) -> None:
        """ """
        for direction, (dy, dx) in self.directions.items():
            ny, nx = y + dy, x + dx
            if 0 <= nx < self.grid_size.width and 0 <= ny < self.grid_size.height:
                valid_tiles = self.adjacency_rules.get(tile, {}).get(direction, set())

                if len(valid_tiles) == 0:
                    self.entropy_grid[ny][nx] = {('A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A')}
                else:
                    self.entropy_grid[ny][nx] = valid_tiles

    def collapse(
        self,
    ) -> None:
        """ """
        i = 0
        running = True
        while running:
            min_entropy = float('inf')
            min_cell = None

            for y in range(self.grid_size.width):
                for x in range(self.grid_size.height):
                    if self.wave[y][x] is None:
                        options = self.entropy_grid[y][x]

                        if len(options) < min_entropy:
                            min_entropy = len(options)
                            min_cell = (y, x)
            
            if min_cell is None:
                break

            # Collapse the weight function
            y, x = min_cell
            #print('y, x')
            #print(y,x)
            #print(self.entropy_grid[y][x])
            choices = list(self.entropy_grid[y][x])
            #print('choices')
            #print(choices)
            weights = [self.tile_weights[tile] for tile in choices]
            #print('weights')
            #print(weights)
            #print(choices, weights)
            chosen_tile = rd.choices(choices, weights)[0]
            #print('chosen_tile')
            #print(chosen_tile)
            self.wave[y][x] = chosen_tile
            #print('self.wave')
            #print(self.wave)
            #print(self.color_mapping)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            self.wfc_visualizer.visualize(self.wave)           
            #time.sleep(0.01)
            self.propagate(y, x, chosen_tile)
            #print('self.entropy_grid')
            #for hoi in self.entropy_grid:
            #    print(hoi)
            i += 1

        return self.wave