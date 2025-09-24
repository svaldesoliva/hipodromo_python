"""
Pytest configuration and fixtures for Hipodromo tests.
"""
import os
import tempfile
import shutil
import json
from unittest.mock import patch, MagicMock
import pytest


@pytest.fixture
def temp_config_dir():
    """Create a temporary directory for testing configuration files."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_config_file(temp_config_dir):
    """Create a mock config file for testing."""
    config_file = os.path.join(temp_config_dir, "config.json")
    config_data = {
        "balance": 5000,
        "lang": "en",
        "fast": False,
        "horses": 5,
        "seed": None
    }
    with open(config_file, 'w') as f:
        json.dump(config_data, f)
    return config_file


@pytest.fixture
def mock_termcolor():
    """Mock termcolor to avoid terminal color issues in tests."""
    with patch('termcolor.cprint') as mock_cprint:
        mock_cprint.side_effect = lambda text, color=None: print(text)
        yield mock_cprint


@pytest.fixture
def mock_clear_screen():
    """Mock screen clearing to avoid terminal issues in tests."""
    with patch('utils.clear_screen') as mock_clear:
        yield mock_clear


@pytest.fixture
def mock_input():
    """Mock user input for testing interactive functions."""
    with patch('builtins.input') as mock_input_func:
        yield mock_input_func


@pytest.fixture
def mock_random_seed():
    """Set a fixed random seed for reproducible tests."""
    import random
    random.seed(42)
    yield
    random.seed()


@pytest.fixture
def sample_race_profile():
    """Sample race profile for testing."""
    return {
        "weights": [1.2, 0.8, 1.0, 1.1, 0.9],
        "odds": [2.1, 3.2, 2.5, 2.3, 2.8],
        "distance": 100,
        "emoji": "🐴"
    }
