"""Module conftest.py, reusable code for pytest."""


import pytest
from unittest.mock import patch, mock_open
from pathlib import Path

from src.my_project.config_manager import ConfigManager

@pytest.fixture(scope="function", name="mock_yaml_content")
def mock_yaml_config():
    """Fixture that defines a mock config content"""
    yaml_content = """
        game:
            fps: 60

        window:
            caption: "Test Window"
            background_color: [0, 0, 0]
            margin_size: 200

        grid:
            dim: 10
            color_map:
                0: [0, 0, 0]
                1: [255, 255, 255]
            grid_line_color: [50, 50, 50]
            grid_line_width: 2
    """

    return yaml_content


@pytest.fixture(scope="function", name="mock_config")
def test_load_conig_file(mock_yaml_content):
    """Test loading config using mocked open."""
    m_open = mock_open(read_data=mock_yaml_content)

    with patch("src.my_project.config_manager.open", m_open):
        config_manager = ConfigManager(Path("mock_config_path.yaml"))
        config = config_manager.load_config_file()

    return config