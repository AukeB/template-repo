{% if cookiecutter.include_pygame -%}
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
{% else -%}
"""Module for Pydantic configuration models."""

from pydantic import BaseModel, ConfigDict


class ConfiguredBaseModel(BaseModel):
    """Config that disallows extra parameters not explicitly defined."""

    model_config = ConfigDict(extra="forbid")


class ConfigModel(ConfiguredBaseModel):
    """Config that combines all parameters.

    Attributes:
        config_category_1 (ConfigCategory1): Parameters of category 1.
        config_category_two (ConfigCategory2): Parameters of category 2.
    """

    class ConfigCategory1(ConfiguredBaseModel):
        """Config for category 1 parameters.

        Attributes:
            float_param (float): A floating-point parameter.
            str_param (str): A string parameter.
        """

        float_param: float
        str_param: str

    class ConfigCategory2(ConfiguredBaseModel):
        """Config for category 2 parameters.

        Attributes:
            int_param (int): An integer parameter.
            bool_param (bool): A boolean parameter.
            list_param (list[str]): A list of strings.
        """

        int_param: int
        bool_param: bool
        list_param: list[str]

    config_category_1: ConfigCategory1
    config_category_two: ConfigCategory2
{% endif -%}