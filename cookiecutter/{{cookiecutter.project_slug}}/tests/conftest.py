"""Module conftest.py, reusable code for pytest."""

{% if cookiecutter.include_pygame %}import os
{% endif %}from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from {{ cookiecutter.package_name }}.config_manager import ConfigManager
{% if cookiecutter.include_pygame %}
# Run pygame without a real display so the tests work headless.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
{% endif %}

@pytest.fixture(scope="function", name="mock_yaml_content")
def fixture_mock_yaml_content():
    """Defines the mock config content."""
    yaml_content = """
{% if cookiecutter.include_pygame %}        game:
            fps: 60

        window:
            caption: "Test Window"
            background_color: [0, 0, 0]
            margin_size: 200
{% else %}        config_category_1:
            float_param: 1.5
            str_param: 'hello'

        config_category_two:
            int_param: 1
            bool_param: true
            list_param:
                - 'item1'
                - 'item2'
                - 'item3'
{% endif %}    """

    return yaml_content


@pytest.fixture(scope="function", name="mock_config")
def fixture_mock_config(mock_yaml_content):
    """Loads the mock config through a mocked open."""
    m_open = mock_open(read_data=mock_yaml_content)

    with patch("{{ cookiecutter.package_name }}.config_manager.open", m_open):
        config_path = Path("mock_config_path.yaml")
        config_manager = ConfigManager(config_path)
        config = config_manager.load_config_file()

    return config
