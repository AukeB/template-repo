"""Module for loading the configuration files."""

import yaml

from pathlib import Path
from pydantic import BaseModel
from src.my_project.constants import CONFIG


class ConfiguredBaseModel(BaseModel):
    class Config:
        extra = "forbid"  # Disallow unexpected keys in config files


class ConfigModel(ConfiguredBaseModel):
    """Config that combines all parameters"""

    class ConfigCategory1(ConfiguredBaseModel):
        """Config for category 1 parameters"""

        float_param: float
        str_param: str

    class ConfigCategory2(ConfiguredBaseModel):
        """Config for category 2 parameters"""

        int_param: int
        bool_param: bool
        list_param: list[str]

    config_category_1: ConfigCategory1
    config_category_two: ConfigCategory2


class ConfigManager:
    def __init__(self, config_path: Path = CONFIG):
        self.config_path = config_path

    def load_config_file(self) -> ConfigModel:
        with self.config_path.open("r") as f:
            data = yaml.safe_load(f)

        return ConfigModel(**data)
