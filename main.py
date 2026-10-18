"""Module for running the main repository workflow."""

import logging

from my_project.config_manager import ConfigManager
from my_project.game import Game


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
