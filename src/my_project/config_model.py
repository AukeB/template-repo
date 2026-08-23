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
        margin_size: int  # Units: pixels.

    game: ConfigGame
    window: ConfigWindow
