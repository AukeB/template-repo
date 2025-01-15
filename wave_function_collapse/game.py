""" """
from collections import namedtuple
import pygame as pg

Grid = namedtuple('Grid', ['width', 'height'])
Rect = namedtuple('Dimensions', ['width', 'height'])

class WFCVisualizer():
    """ """
    def __init__(
        self,
        grid_dimensions,
        tile_dimensions,
        color_mapping: dict[tuple[int, int, int], str],
        screen_resolution: tuple[int, int] = (1920, 1080),
        margin_size: int=20,
    ) -> None:
        """ """
        pg.init()

        self.screen_resolution = Rect(screen_resolution[0], screen_resolution[1])
        self.grid_dimensions = grid_dimensions
        self.tile_dimensions = tile_dimensions
        self.margin_size = margin_size
        self.color_mapping = {v: k for k, v in color_mapping.items()}
        self.tile_size = self._compute_tile_size()
        self.cell_size = self._compute_cell_size()

        self.screen = pg.display.set_mode(
            (self.screen_resolution.width, self.screen_resolution.height)
        )
    
    def _compute_tile_size(
        self,
    ) -> tuple[int, int]:
        """ """
        return Rect(
            int((self.screen_resolution.height - 2*self.margin_size) / self.grid_dimensions.height),
            int((self.screen_resolution.height - 2*self.margin_size) / self.grid_dimensions.height)
        )
    
    def _compute_cell_size(
        self,
    ) -> tuple[int, int]:
        """ """
        return Rect(
            int(self.tile_size.width / self.tile_dimensions.width),
            int(self.tile_size.height / self.tile_dimensions.height),
        )

    def visualize(
        self,
        output_grid
    ):
        """ """
        #self.screen.fill((0, 0, 0))

        for row_tile_idx in range(self.grid_dimensions.height):
            for col_tile_idex in range(self.grid_dimensions.width):
                x = self.margin_size + col_tile_idex * self.tile_size.width
                y = self.margin_size + row_tile_idx * self.tile_size.height
                tile_value = output_grid[row_tile_idx][col_tile_idex]
                tile_rect = pg.Rect(x, y, self.tile_size.width, self.tile_size.height)
                
                if tile_value is None:
                    pass
                    #color = (200, 200, 200)
                    #pg.draw.rect(self.screen, color, tile_rect)
                else:
                    for cell_row_idx in range(self.tile_dimensions.height):
                        for cell_col_idx in range(self.tile_dimensions.width):
                            cell_index = cell_row_idx * self.tile_dimensions.height + cell_col_idx
                            cell_value = self.color_mapping[tile_value[cell_index]]
                            cell_rect = pg.Rect(
                                x + cell_row_idx*self.cell_size.width,
                                y + cell_col_idx*self.cell_size.height,
                                self.cell_size.width,
                                self.cell_size.height
                            )
                            pg.draw.rect(self.screen, cell_value, cell_rect)

            pg.display.flip()