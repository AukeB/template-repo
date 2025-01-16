""" """
import math
import pygame as pg
from collections import namedtuple
from constants import Size, screen_resolution

class WFCVisualizer():
    """ """
    def __init__(
        self,
        grid_dimensions,
        tile_dimensions,
        color_mapping: dict[tuple[int, int, int], str],
        screen_resolution: tuple[int, int] = screen_resolution,
        margin_size: int=20,
    ) -> None:
        """ """
        pg.init()

        self.screen_size = Size(screen_resolution[0], screen_resolution[1])
        self.grid_dimensions = grid_dimensions
        self.tile_dimensions = tile_dimensions
        self.margin_size = margin_size
        self.color_mapping = {v: k for k, v in color_mapping.items()}
        self.tile_size, self.cell_size = self._compute_tile_and_cell_size()

        self.screen = pg.display.set_mode(
            (self.screen_size.width, self.screen_size.height)
        )
    
    def _compute_tile_and_cell_size(
        self,
    ) -> tuple[int, int]:
        """ """
        tile_size = Size(
            # To always make the grid a square, use height in both dimensions.
            # Assumes your screen resolution has a larger width than height
            int((self.screen_size.height - 2*self.margin_size) / self.grid_dimensions.height),
            int((self.screen_size.height - 2*self.margin_size) / self.grid_dimensions.height)
        )

        cell_size = Size(
            int(tile_size.width / self.tile_dimensions.width),
            int(tile_size.height / self.tile_dimensions.height),
        )

        return tile_size, cell_size

    def visualize(
        self,
        grid,
        # entropy # for calculating supoer position colour of available cells.
    ):
        """ """
        for row_tile_idx in range(self.grid_dimensions.height):
            for col_tile_idex in range(self.grid_dimensions.width):
                x = self.margin_size + col_tile_idex * self.tile_size.width
                y = self.margin_size + row_tile_idx * self.tile_size.height
                tile_value = grid[row_tile_idx][col_tile_idex]
                #tile_rect = pg.Rect(x, y, self.tile_size.width, self.tile_size.height)
                
                if tile_value is None:
                    # Todo: write code for displaying cells in superposition.
                    # However, it may make the program slower, if pygames draw function is slow.
                    pass
                else:
                    for cell_row_idx in range(self.tile_dimensions.height):
                        for cell_col_idx in range(self.tile_dimensions.width):
                            cell_value = self.color_mapping[tile_value[cell_col_idx][cell_row_idx]]

                            cell_rect = pg.Rect(
                                x + cell_row_idx*self.cell_size.width,
                                y + cell_col_idx*self.cell_size.height,
                                self.cell_size.width,
                                self.cell_size.height
                            )

                            pg.draw.rect(self.screen, cell_value, cell_rect)

            pg.display.flip()

    def show_unique_tiles(self, tile_weights):
        """ """
        inner_margin_size = 10
        tiles = list(tile_weights.keys())
        for tile in tiles:
            for row in tile:
                print(row)
            print('')
        print('\n')

        next_square_number = math.ceil(math.sqrt(len(tiles)))
        self.grid_dimensions = Size(next_square_number, next_square_number)
        self.tile_size, self.cell_size = self._compute_tile_and_cell_size()

        for row_tile_idx in range(self.grid_dimensions.height):
            for col_tile_idex in range(self.grid_dimensions.width):
                x = self.margin_size + col_tile_idex * self.tile_size.width
                y = self.margin_size + row_tile_idx * self.tile_size.height
                index = row_tile_idx*self.grid_dimensions.height + col_tile_idex
                if index < len(tiles):
                    tile_value = tiles[index]
                    #tile_rect = pg.Rect(x, y, self.tile_size.width, self.tile_size.height)
                    
                    if tile_value is None:
                        # Todo: write code for displaying cells in superposition.
                        pass
                    else:
                        for cell_row_idx in range(self.tile_dimensions.height):
                            for cell_col_idx in range(self.tile_dimensions.width):
                                cell_value = self.color_mapping[tile_value[cell_col_idx][cell_row_idx]]

                                cell_rect = pg.Rect(
                                    x + cell_row_idx*self.cell_size.width,
                                    y + cell_col_idx*self.cell_size.height,
                                    self.cell_size.width,
                                    self.cell_size.height
                                )

                                pg.draw.rect(self.screen, cell_value, cell_rect)

                pg.display.flip()
        
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    break