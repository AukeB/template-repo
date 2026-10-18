"""Module for Pydantic configuration models."""

from pydantic import BaseModel, ConfigDict


class ConfiguredBaseModel(BaseModel):
    """Config that disallows extra parameters not explicitly defined."""

    model_config = ConfigDict(extra="forbid")


class ConfigModel(ConfiguredBaseModel):
    """Config that combines all parameters.

    Attributes:
        game (ConfigGame): Parameters of the game loop.
        window (ConfigWindow): Parameters of the game window.
        grid (ConfigGrid): Parameters of the grid.
    """

    class ConfigGame(ConfiguredBaseModel):
        """Config for general game loop parameters.

        Attributes:
            fps (int): Target frames per second of the game loop.
        """

        fps: int

    class ConfigWindow(ConfiguredBaseModel):
        """Config for window appearance.

        Attributes:
            caption (str): Title shown in the window bar.
            background_color (list[int]): RGB color that fills the window.
            margin_size (int): Margin around the drawing area, in pixels.
        """

        caption: str
        background_color: list[int]
        margin_size: int  # Units: pixels.

    class ConfigGrid(ConfiguredBaseModel):
        """Config for grid dimensions and appearance.

        Attributes:
            dim (int): Number of cells in width as well as height direction.
            color_map (dict[int, list[int]]): RGB color for each cell state.
            show_gridlines (bool): Whether grid lines are drawn over the cells.
            grid_line_color (list[int]): RGB color of the grid lines.
            grid_line_width (int): Width of the grid lines, in pixels.
        """

        dim: int
        color_map: dict[int, list[int]]
        show_gridlines: bool
        grid_line_color: list[int]
        grid_line_width: int  # Units: pixels.

    game: ConfigGame
    window: ConfigWindow
    grid: ConfigGrid
