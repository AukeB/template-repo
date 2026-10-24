"""Module for testing config_manager.py"""

from {{ cookiecutter.package_name }}.config_model import ConfigModel


# Testing the "load_config_file" method from the "ConfigManager" class.


def test_load_config_file(mock_config):
    """Testing the 'load_config_file' method."""
    assert isinstance(mock_config, ConfigModel)
{% if cookiecutter.include_pygame %}    assert mock_config.game.fps == 60
    assert mock_config.window.caption == "Test Window"
{% else %}    assert mock_config.config_category_1.float_param == 1.5
{% endif %}