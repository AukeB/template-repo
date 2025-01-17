""" """

from bitmap import BitmapUtils
from wfc import gridFunctionCollapse
from constants import Size

bitmap_utils = BitmapUtils()


def main():
    bitmap = bitmap_utils.read_bitmap_from_excel(
        relative_dir_path="bitmaps",
        file_name="tile_1.xlsx",
    )

    color_mapping = bitmap_utils.create_color_mapping(rgb_size=bitmap)
    bitmap = bitmap_utils.apply_color_mapping(
        rgb_size=bitmap, color_mapping=color_mapping
    )

    grid_dim = 3
    tile_dim = 3

    grid_dimensions = Size(grid_dim, grid_dim)
    tile_dimensions = Size(tile_dim, tile_dim)

    wfc = gridFunctionCollapse(
        bitmap=bitmap,
        grid_dimensions=grid_dimensions,
        tile_dimensions=tile_dimensions,
        color_mapping=color_mapping,
    )

    wfc.collapse()


if __name__ == "__main__":
    main()
