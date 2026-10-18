"""Module for running the main repository workflow."""

import logging

import yaml

from my_project.config_manager import ConfigManager

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
