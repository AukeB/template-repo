"""Module for Pydantic configuration models."""

from pydantic import BaseModel, ConfigDict


class ConfiguredBaseModel(BaseModel):
    """Config that disallows extra parameters not explicitly defined"""

    model_config = ConfigDict(extra="forbid")


class ConfigModel(ConfiguredBaseModel):
    """Config that combines all parameters"""

    class ConfigGrid(ConfiguredBaseModel):
        """Config for grid dimensions and appearance."""

        num_rows: int
        num_columns: int
        cell_size: int  # Units: pixels.

    grid: ConfigGrid
