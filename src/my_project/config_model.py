"""Module for Pydantic configuration models."""

from pydantic import BaseModel, ConfigDict


class ConfiguredBaseModel(BaseModel):
    """Config that disallows extra parameters not explicitly defined"""

    model_config = ConfigDict(extra="forbid")


class ConfigModel(ConfiguredBaseModel):
    """Config that combines all parameters"""

    class ConfigGame(ConfiguredBaseModel):
        """Config for general game loop parameters."""

        fps: int

    class ConfigWindow(ConfiguredBaseModel):
        """Config for window appearance."""

        caption: str
        background_color: list[int]

    class ConfigGrid(ConfiguredBaseModel):
        """Config for grid dimensions and appearance."""

        num_rows: int
        num_cols: int
        cell_size: int  # Units: pixels.
        background_color: list[int]
        color_map: dict[int, list[int]]

    game: ConfigGame
    window: ConfigWindow
    grid: ConfigGrid
