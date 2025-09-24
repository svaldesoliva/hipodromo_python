"""
Simple test to verify the test setup is working correctly.
"""
import pytest
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def test_imports():
    """Test that all modules can be imported."""
    try:
        import game
        import config
        import i18n
        import utils
        import Hipodromo
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import module: {e}")


def test_basic_functionality():
    """Test basic functionality of core modules."""
    # Test game module
    from game import _generate_weights, compute_decimal_odds, build_race
    weights = _generate_weights(5, seed=42)
    assert len(weights) == 5
    assert all(0.6 <= w <= 1.4 for w in weights)
    
    odds = compute_decimal_odds(weights)
    assert len(odds) == 5
    assert all(odd >= 1.5 for odd in odds)
    
    race = build_race(5, seed=42)
    assert "weights" in race
    assert "odds" in race
    
    # Test i18n module
    from i18n import translator
    t = translator("en")
    assert t("title") == "Hippodrome v0.3\n"
    
    t_es = translator("es")
    assert t_es("title") == "Hipódromo v0.3\n"
    
    # Test utils module
    from utils import fzf_available
    # Should not raise exception
    result = fzf_available()
    assert isinstance(result, bool)


def test_test_environment():
    """Test that the test environment is set up correctly."""
    # Test that we can import pytest
    import pytest
    assert hasattr(pytest, 'fixture')
    
    # Test that we can use temp directories
    import tempfile
    with tempfile.TemporaryDirectory() as temp_dir:
        assert os.path.exists(temp_dir)
        assert os.path.isdir(temp_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
