{% if cookiecutter.include_pygame -%}
"""Module for running the main repository workflow."""

import logging

from {{ cookiecutter.package_name }}.config_manager import ConfigManager
from {{ cookiecutter.package_name }}.game import Game


def main() -> None:
    """Load configuration and launch the pygame game window.

    1. Configure logging.
    2. Instantiate ConfigManager and load the config file.
    3. Create the Game and run it until the window closes.
    """
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    config_manager = ConfigManager()
    config = config_manager.load_config_file()

    game = Game(config=config)
    game.run()


if __name__ == "__main__":
    main()
{% else -%}
"""Module for running the main repository workflow."""

import logging

import yaml

from {{ cookiecutter.package_name }}.config_manager import ConfigManager

logger = logging.getLogger(__name__)


def main() -> None:
    """Load configuration and log the loaded settings.

    1. Configure logging.
    2. Instantiate ConfigManager and load the config file.
    3. Log the loaded configuration as YAML.
    """
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    config_manager = ConfigManager()
    config = config_manager.load_config_file()
    config_data = config.model_dump()
    config_yaml = yaml.safe_dump(config_data, sort_keys=False, default_flow_style=False)

    logger.info("Loaded config:\n%s", config_yaml)


if __name__ == "__main__":
    main()
{% endif -%}