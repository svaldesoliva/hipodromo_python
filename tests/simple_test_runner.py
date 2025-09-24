#!/usr/bin/env python3
"""
Simple test runner that doesn't require pytest.
This can be used to run basic tests when pytest is not available.
"""
import sys
import os
import traceback
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_success(self, test_name):
        self.passed += 1
        print(f"✓ {test_name}")
    
    def add_failure(self, test_name, error):
        self.failed += 1
        self.errors.append((test_name, error))
        print(f"✗ {test_name}: {error}")
    
    def print_summary(self):
        print(f"\nTest Results: {self.passed} passed, {self.failed} failed")
        if self.errors:
            print("\nFailures:")
            for test_name, error in self.errors:
                print(f"  {test_name}: {error}")


def run_test(test_func, test_name):
    """Run a single test function."""
    try:
        test_func()
        return True, None
    except Exception as e:
        return False, str(e)


def test_basic_imports():
    """Test that all modules can be imported."""
    import game
    import config
    import i18n
    import utils
    import Hipodromo


def test_game_basic_functionality():
    """Test basic game functionality."""
    from game import _generate_weights, compute_decimal_odds, build_race
    
    # Test weight generation
    weights = _generate_weights(5, seed=42)
    assert len(weights) == 5, f"Expected 5 weights, got {len(weights)}"
    assert all(0.6 <= w <= 1.4 for w in weights), f"Invalid weight range: {weights}"
    
    # Test odds calculation
    odds = compute_decimal_odds(weights)
    assert len(odds) == 5, f"Expected 5 odds, got {len(odds)}"
    assert all(odd >= 1.5 for odd in odds), f"Invalid odds: {odds}"
    
    # Test race building
    race = build_race(5, seed=42)
    assert "weights" in race, "Race missing weights"
    assert "odds" in race, "Race missing odds"
    assert "distance" in race, "Race missing distance"
    assert "emoji" in race, "Race missing emoji"


def test_i18n_basic_functionality():
    """Test basic i18n functionality."""
    from i18n import translator, TRANSLATIONS
    
    # Test translator
    t_en = translator("en")
    assert t_en("title") == "Hippodrome v0.3\n", f"English title incorrect: {t_en('title')}"
    
    t_es = translator("es")
    assert t_es("title") == "Hipódromo v0.3\n", f"Spanish title incorrect: {t_es('title')}"
    
    # Test placeholder substitution
    result = t_en("current_balance", dinero=1000)
    assert "1000" in result, f"Placeholder not substituted: {result}"
    
    # Test translations structure
    assert "en" in TRANSLATIONS, "English translations missing"
    assert "es" in TRANSLATIONS, "Spanish translations missing"
    assert len(TRANSLATIONS["en"]) == len(TRANSLATIONS["es"]), "Translation key count mismatch"


def test_config_basic_functionality():
    """Test basic config functionality."""
    import tempfile
    import shutil
    from config import _ensure_and_migrate_config, get_balance, set_balance
    
    # Test with temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Mock the config directory
        import config
        original_config_dir = config.CONFIG_DIR
        config.CONFIG_DIR = temp_dir
        
        try:
            # Test config creation
            config_data = _ensure_and_migrate_config()
            assert isinstance(config_data, dict), "Config should be a dictionary"
            assert "balance" in config_data, "Config missing balance"
            assert "lang" in config_data, "Config missing lang"
            assert "fast" in config_data, "Config missing fast"
            assert "horses" in config_data, "Config missing horses"
            assert "seed" in config_data, "Config missing seed"
            
            # Test balance operations
            set_balance(7500)
            assert get_balance() == 7500, f"Balance not set correctly: {get_balance()}"
            
        finally:
            config.CONFIG_DIR = original_config_dir


def test_utils_basic_functionality():
    """Test basic utils functionality."""
    from utils import fzf_available, clear_screen
    
    # Test fzf availability (should not raise exception)
    result = fzf_available()
    assert isinstance(result, bool), f"fzf_available should return bool, got {type(result)}"
    
    # Test clear_screen (should not raise exception)
    try:
        clear_screen()
    except Exception as e:
        raise AssertionError(f"clear_screen should not raise exception: {e}")


def test_race_determinism():
    """Test race determinism."""
    from game import build_race
    
    # Test that same seed produces same race
    race1 = build_race(5, seed=12345)
    race2 = build_race(5, seed=12345)
    assert race1["weights"] == race2["weights"], "Race weights should be deterministic"
    assert race1["odds"] == race2["odds"], "Race odds should be deterministic"
    
    # Test that different seeds produce different races
    race3 = build_race(5, seed=54321)
    assert race1["weights"] != race3["weights"], "Different seeds should produce different races"


def test_odds_calculation_edge_cases():
    """Test odds calculation edge cases."""
    from game import compute_decimal_odds
    
    # Test with extreme weights
    extreme_weights = [0.6, 1.4, 0.6, 1.4, 0.6]
    odds = compute_decimal_odds(extreme_weights)
    
    assert len(odds) == 5, f"Expected 5 odds, got {len(odds)}"
    assert all(odd >= 1.5 for odd in odds), f"All odds should be >= 1.5: {odds}"
    assert all(odd < 50 for odd in odds), f"Odds should not be unreasonably high: {odds}"
    
    # Test with equal weights
    equal_weights = [1.0, 1.0, 1.0, 1.0, 1.0]
    equal_odds = compute_decimal_odds(equal_weights)
    
    # All odds should be similar
    max_odd = max(equal_odds)
    min_odd = min(equal_odds)
    assert max_odd - min_odd < 0.5, f"Equal weights should produce similar odds: {equal_odds}"


def main():
    """Run all tests."""
    print("Running Hipodromo Basic Tests...\n")
    
    result = TestResult()
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Game Basic Functionality", test_game_basic_functionality),
        ("i18n Basic Functionality", test_i18n_basic_functionality),
        ("Config Basic Functionality", test_config_basic_functionality),
        ("Utils Basic Functionality", test_utils_basic_functionality),
        ("Race Determinism", test_race_determinism),
        ("Odds Calculation Edge Cases", test_odds_calculation_edge_cases),
    ]
    
    for test_name, test_func in tests:
        success, error = run_test(test_func, test_name)
        if success:
            result.add_success(test_name)
        else:
            result.add_failure(test_name, error)
    
    result.print_summary()
    
    if result.failed > 0:
        print("\nSome tests failed. Check the errors above.")
        return 1
    else:
        print("\nAll tests passed! ✓")
        return 0


if __name__ == "__main__":
    sys.exit(main())
