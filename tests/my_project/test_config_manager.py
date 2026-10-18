"""Module for testing config_manager.py"""

from my_project.config_model import ConfigModel


# Testing the "load_config_file" method from the "ConfigManager" class.


def test_load_config_file(mock_config):
    """Testing the 'load_config_file' method."""
    assert isinstance(mock_config, ConfigModel)
    assert mock_config.game.fps == 60
    assert mock_config.window.caption == "Test Window"
    assert mock_config.grid.dim == 10
