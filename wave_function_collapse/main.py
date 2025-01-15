""" """
from collections import namedtuple
from bitmap import BitmapUtils
from wfc import WaveFunctionCollapse

Grid = namedtuple('Grid', ['width', 'height'])

bitmap_utils = BitmapUtils()

def main():
    bitmap = bitmap_utils.read_bitmap_from_excel(
        relative_dir_path='bitmaps',
        file_name='tile_1.xlsx',
    )

    color_mapping = bitmap_utils.create_color_mapping(rgb_grid=bitmap)
    bitmap = bitmap_utils.apply_color_mapping(rgb_grid=bitmap, color_mapping=color_mapping)

    grid_dim = 50
    grid_dimensions = Grid(grid_dim, grid_dim)
    tile_dim = 3

    wfc = WaveFunctionCollapse(
        bitmap=bitmap,
        grid_size=grid_dimensions,
        tile_size=tile_dim,
        color_mapping=color_mapping,
    )

    wfc_output = wfc.collapse()

if __name__ == "__main__":
    main()