"""Module for testing config_manager.py"""


from src.my_project.config_manager import ConfigModel


def test_load_config_file(mock_config):
    """Testing the 'load_config_file' method."""
    assert isinstance(mock_config, ConfigModel)
    assert mock_config.game.fps == 60