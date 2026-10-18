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
