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

    game: ConfigGame
    window: ConfigWindow
