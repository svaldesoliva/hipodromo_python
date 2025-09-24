"""
Debugging-specific tests for common issues and edge cases in the Hipodromo game.
These tests are designed to help identify and reproduce common bugs.
"""
import pytest
import os
import tempfile
import shutil
import json
import random
from unittest.mock import patch, MagicMock, mock_open
from game import _generate_weights, compute_decimal_odds, build_race, animacion
from config import _ensure_and_migrate_config, get_balance, set_balance
from i18n import translator
from utils import input_entero, fzf_select


class TestRaceEngineDebugging:
    """Debug tests for race engine issues."""
    
    def test_race_determinism_issues(self):
        """Debug race determinism problems."""
        # Test that same seed always produces same race
        seed = 12345
        race1 = build_race(5, seed=seed)
        race2 = build_race(5, seed=seed)
        
        assert race1["weights"] == race2["weights"], "Race weights should be deterministic"
        assert race1["odds"] == race2["odds"], "Race odds should be deterministic"
        
        # Test that different seeds produce different races
        race3 = build_race(5, seed=54321)
        assert race1["weights"] != race3["weights"], "Different seeds should produce different races"
    
    def test_odds_calculation_edge_cases(self):
        """Debug odds calculation edge cases."""
        # Test with extreme weight values
        extreme_weights = [0.6, 1.4, 0.6, 1.4, 0.6]
        odds = compute_decimal_odds(extreme_weights)
        
        # Verify odds are reasonable
        assert all(odd >= 1.5 for odd in odds), "All odds should be at least 1.5x"
        assert all(odd < 50 for odd in odds), "Odds should not be unreasonably high"
        
        # Test with all equal weights
        equal_weights = [1.0, 1.0, 1.0, 1.0, 1.0]
        equal_odds = compute_decimal_odds(equal_weights)
        
        # All odds should be similar (within reasonable tolerance)
        max_odd = max(equal_odds)
        min_odd = min(equal_odds)
        assert max_odd - min_odd < 0.5, "Equal weights should produce similar odds"
    
    def test_race_completion_guarantee(self):
        """Debug race completion issues."""
        # Test that races always complete
        for _ in range(10):
            race = build_race(5, seed=random.randint(1, 10000))
            
            with patch('game.clear_screen'), patch('game.cprint'):
                mock_t = MagicMock()
                mock_t.side_effect = lambda key, **kwargs: f"mock_{key}"
                
                winner = animacion(5, 1, mock_t, race_profile=race, fast=True)
                assert isinstance(winner, int), "Race should always return a winner"
                assert 1 <= winner <= 5, f"Winner should be between 1 and 5, got {winner}"
    
    def test_weight_distribution_analysis(self):
        """Debug weight distribution issues."""
        # Generate many weights and analyze distribution
        all_weights = []
        for _ in range(1000):
            weights = _generate_weights(5)
            all_weights.extend(weights)
        
        # Check distribution properties
        assert all(0.6 <= w <= 1.4 for w in all_weights), "All weights should be in valid range"
        
        # Check that we have reasonable variance
        unique_weights = set(round(w, 2) for w in all_weights)
        assert len(unique_weights) > 50, "Should have good weight variety"
        
        # Check mean is reasonable
        mean_weight = sum(all_weights) / len(all_weights)
        assert 0.9 <= mean_weight <= 1.1, f"Weight mean should be around 1.0, got {mean_weight}"


class TestConfigurationDebugging:
    """Debug tests for configuration issues."""
    
    def test_config_file_corruption_recovery(self, temp_config_dir):
        """Debug config file corruption issues."""
        config_file = os.path.join(temp_config_dir, "config.json")
        
        # Test various corruption scenarios
        corruption_scenarios = [
            "invalid json content",
            "{invalid json}",
            '{"balance": "not_a_number"}',
            '{"balance": -1000}',
            '{"horses": 0}',
            '{"lang": "invalid_language"}',
            "",
            None
        ]
        
        for corruption in corruption_scenarios:
            # Create corrupted config
            if corruption is not None:
                with open(config_file, 'w') as f:
                    f.write(corruption)
            else:
                # Test with missing file
                if os.path.exists(config_file):
                    os.remove(config_file)
            
            # Should recover gracefully
            with patch('config.CONFIG_DIR', temp_config_dir):
                config = _ensure_and_migrate_config()
                assert isinstance(config, dict), "Should return valid config dict"
                assert "balance" in config, "Should have balance key"
                assert config["balance"] >= 0, "Balance should be non-negative"
                assert config["horses"] >= 2, "Horses should be at least 2"
    
    def test_config_migration_edge_cases(self, temp_config_dir):
        """Debug config migration edge cases."""
        # Test migration with various legacy file states
        legacy_files = {
            "balance": "7500",
            "lang": "es",
            "old_balance": "5000",
            "old_lang": "en"
        }
        
        for filename, content in legacy_files.items():
            filepath = os.path.join(temp_config_dir, filename)
            with open(filepath, 'w') as f:
                f.write(content)
        
        with patch('config.CONFIG_DIR', temp_config_dir), \
             patch('config.BALANCE_FILE', os.path.join(temp_config_dir, "balance")), \
             patch('config.LANG_FILE', os.path.join(temp_config_dir, "lang")), \
             patch('config.OLD_BALANCE_FILE', os.path.join(temp_config_dir, "old_balance")), \
             patch('config.OLD_LANG_FILE', os.path.join(temp_config_dir, "old_lang")):
            
            config = _ensure_and_migrate_config()
            assert config["balance"] == 7500, "Should use newer balance file"
            assert config["lang"] == "es", "Should use newer lang file"
    
    def test_config_concurrent_access_simulation(self, temp_config_dir):
        """Debug concurrent config access issues."""
        with patch('config.CONFIG_DIR', temp_config_dir):
            # Simulate rapid config changes
            for i in range(100):
                set_balance(1000 + i)
                if i % 2 == 0:
                    set_balance(5000)  # Reset to default occasionally
            
            # Verify final state is consistent
            final_balance = get_balance()
            assert isinstance(final_balance, int), "Balance should be integer"
            assert final_balance >= 0, "Balance should be non-negative"
    
    def test_config_directory_permissions(self, temp_config_dir):
        """Debug config directory permission issues."""
        # Test with read-only directory
        read_only_dir = os.path.join(temp_config_dir, "readonly")
        os.makedirs(read_only_dir, mode=0o444)
        
        with patch('config.CONFIG_DIR', read_only_dir):
            # Should handle permission errors gracefully
            try:
                config = _ensure_and_migrate_config()
                # If it succeeds, config should be valid
                assert isinstance(config, dict)
            except PermissionError:
                # Permission error is acceptable
                pass


class TestInputDebugging:
    """Debug tests for input handling issues."""
    
    @patch('builtins.input')
    def test_input_entero_infinite_loop_prevention(self, mock_input):
        """Debug infinite loop issues in input_entero."""
        # Simulate problematic input patterns
        problematic_inputs = [
            "",  # Empty input
            "   ",  # Whitespace only
            "abc",  # Non-numeric
            "3.14",  # Float
            "999999999999999999999",  # Very large number
            "0" * 1000,  # Very long string
        ]
        
        for problematic_input in problematic_inputs:
            mock_input.side_effect = [problematic_input, "5"]  # Follow with valid input
            
            result = input_entero("Enter a number: ")
            assert result == 5, f"Should handle '{problematic_input}' gracefully"
    
    @patch('builtins.input')
    def test_input_entero_boundary_conditions(self, mock_input):
        """Debug boundary condition issues."""
        # Test exact boundary values
        mock_input.return_value = "1"
        result = input_entero("Enter a number: ", minimo=1, maximo=10)
        assert result == 1, "Should accept exact minimum"
        
        mock_input.return_value = "10"
        result = input_entero("Enter a number: ", minimo=1, maximo=10)
        assert result == 10, "Should accept exact maximum"
        
        # Test just outside boundaries
        mock_input.side_effect = ["0", "11", "5"]
        result = input_entero("Enter a number: ", minimo=1, maximo=10)
        assert result == 5, "Should reject values outside boundaries"
    
    @patch('subprocess.run')
    def test_fzf_select_error_handling(self, mock_run):
        """Debug fzf selection error handling."""
        # Test various error scenarios
        error_scenarios = [
            FileNotFoundError("fzf not found"),
            PermissionError("Permission denied"),
            subprocess.TimeoutExpired("fzf", 30),
            OSError("System error"),
        ]
        
        for error in error_scenarios:
            mock_run.side_effect = error
            
            result = fzf_select(["Option 1", "Option 2"], "Choose:")
            assert result is None, f"Should handle {type(error).__name__} gracefully"


class TestTranslationDebugging:
    """Debug tests for translation issues."""
    
    def test_translation_placeholder_consistency(self):
        """Debug translation placeholder issues."""
        import re
        
        for lang in ["en", "es"]:
            t = translator(lang)
            
            # Test all translation keys
            for key in t.__self__.__dict__.get('TRANSLATIONS', {}).get(lang, {}):
                try:
                    # Try to call translation with common parameters
                    result = t(key, dinero=1000, idx=1, ganancia=500, apuesta=100, 
                              winner=1, minimo=1, maximo=10, n=5)
                    
                    # Check for unresolved placeholders
                    unresolved = re.findall(r'\{[^}]+\}', result)
                    assert not unresolved, f"Unresolved placeholders in {lang}.{key}: {unresolved}"
                    
                except KeyError as e:
                    # Missing parameter is acceptable for some keys
                    pass
    
    def test_translation_unicode_handling(self):
        """Debug unicode handling in translations."""
        t_es = translator("es")
        t_en = translator("en")
        
        # Test unicode characters
        unicode_tests = [
            ("title", "ó"),  # Spanish title should have accented character
            ("horse_name", "1"),  # Should handle numbers
        ]
        
        for key, expected_char in unicode_tests:
            result_es = t_es(key, idx=1)
            result_en = t_en(key, idx=1)
            
            # Should not raise unicode errors
            assert isinstance(result_es, str)
            assert isinstance(result_en, str)
            
            if expected_char == "ó":
                assert expected_char in result_es, "Spanish should contain accented characters"
    
    def test_translation_missing_keys(self):
        """Debug missing translation keys."""
        from i18n import TRANSLATIONS
        
        # Check that all required keys exist in both languages
        required_keys = {
            "title", "menu_play", "menu_exit", "bet_prompt", 
            "you_win", "you_lose", "current_balance", "horse_name"
        }
        
        for lang in ["en", "es"]:
            missing_keys = required_keys - set(TRANSLATIONS[lang].keys())
            assert not missing_keys, f"Missing keys in {lang}: {missing_keys}"


class TestGameStateDebugging:
    """Debug tests for game state issues."""
    
    def test_money_state_consistency(self, temp_config_dir):
        """Debug money state consistency issues."""
        with patch('config.CONFIG_DIR', temp_config_dir):
            # Test various money operations
            set_balance(5000)
            assert get_balance() == 5000
            
            set_balance(0)
            assert get_balance() == 0
            
            set_balance(-1000)
            assert get_balance() == 5000  # Should reset to default
            
            set_balance(999999999)
            assert get_balance() == 999999999
    
    def test_race_state_consistency(self):
        """Debug race state consistency issues."""
        # Test that race state is consistent across multiple calls
        for seed in [None, 42, "test", 12345]:
            race1 = build_race(5, seed=seed)
            race2 = build_race(5, seed=seed)
            
            assert race1 == race2, f"Race state should be consistent for seed {seed}"
            
            # Verify race structure
            assert "weights" in race1
            assert "odds" in race1
            assert "distance" in race1
            assert "emoji" in race1
            
            assert len(race1["weights"]) == 5
            assert len(race1["odds"]) == 5
            assert race1["distance"] == 100
            assert race1["emoji"] == "🐴"


class TestPerformanceDebugging:
    """Debug tests for performance issues."""
    
    def test_race_performance_under_load(self):
        """Debug race performance under load."""
        import time
        
        # Test multiple races in sequence
        start_time = time.time()
        
        for _ in range(100):
            race = build_race(5, seed=random.randint(1, 1000))
            odds = compute_decimal_odds(race["weights"])
            assert len(odds) == 5
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 100 races in reasonable time
        assert duration < 5.0, f"100 races took too long: {duration:.2f}s"
    
    def test_config_performance_under_load(self, temp_config_dir):
        """Debug config performance under load."""
        import time
        
        with patch('config.CONFIG_DIR', temp_config_dir):
            start_time = time.time()
            
            # Rapid config changes
            for i in range(1000):
                set_balance(i)
                get_balance()
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Should handle 1000 operations in reasonable time
            assert duration < 10.0, f"1000 config operations took too long: {duration:.2f}s"
    
    def test_memory_usage_debugging(self):
        """Debug memory usage issues."""
        import gc
        
        # Test memory usage with many race generations
        initial_objects = len(gc.get_objects())
        
        races = []
        for _ in range(1000):
            race = build_race(5)
            races.append(race)
        
        # Clean up
        races.clear()
        gc.collect()
        
        final_objects = len(gc.get_objects())
        object_growth = final_objects - initial_objects
        
        # Should not have excessive object growth
        assert object_growth < 1000, f"Excessive object growth: {object_growth}"


class TestIntegrationDebugging:
    """Debug tests for integration issues."""
    
    @patch('Hipodromo.cargar_dinero')
    @patch('Hipodromo.guardar_dinero')
    def test_game_flow_state_consistency(self, mock_guardar_dinero, mock_cargar_dinero):
        """Debug game flow state consistency."""
        mock_cargar_dinero.return_value = 5000
        
        # Simulate game flow
        with patch('Hipodromo.dinero', 5000):
            # Initial state
            assert getattr(Hipodromo, 'dinero', None) == 5000
            
            # Simulate betting
            guardar_dinero(4000)  # After betting 1000
            mock_guardar_dinero.assert_called_with(4000)
            
            # Simulate winning
            guardar_dinero(6000)  # After winning
            mock_guardar_dinero.assert_called_with(6000)
    
    def test_error_propagation_debugging(self):
        """Debug error propagation issues."""
        # Test that errors in one component don't break others
        with patch('config.get_balance', side_effect=Exception("Config error")):
            # Should handle config error gracefully
            try:
                from Hipodromo import cargar_dinero
                result = cargar_dinero()
                assert result == 5000  # Should use default
            except Exception as e:
                pytest.fail(f"Should handle config error gracefully: {e}")
    
    def test_race_animation_debugging(self):
        """Debug race animation issues."""
        race = build_race(5, seed=42)
        
        with patch('game.clear_screen'), patch('game.cprint'):
            mock_t = MagicMock()
            mock_t.side_effect = lambda key, **kwargs: f"mock_{key}"
            
            # Test animation with various parameters
            for user_horse in range(1, 6):
                winner = animacion(5, user_horse, mock_t, race_profile=race, fast=True)
                assert isinstance(winner, int)
                assert 1 <= winner <= 5
