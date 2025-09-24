"""
Tests for game.py - Race engine, odds calculation, and animation logic.
"""
import pytest
import random
from unittest.mock import patch, MagicMock
from game import (
    _generate_weights,
    compute_decimal_odds,
    build_race,
    animacion
)


class TestGenerateWeights:
    """Test weight generation for horses."""
    
    def test_generate_weights_basic(self):
        """Test basic weight generation."""
        weights = _generate_weights(5)
        assert len(weights) == 5
        assert all(0.6 <= w <= 1.4 for w in weights)
    
    def test_generate_weights_with_seed(self):
        """Test weight generation with seed for reproducibility."""
        weights1 = _generate_weights(5, seed=42)
        weights2 = _generate_weights(5, seed=42)
        assert weights1 == weights2
    
    def test_generate_weights_different_seeds(self):
        """Test that different seeds produce different weights."""
        weights1 = _generate_weights(5, seed=42)
        weights2 = _generate_weights(5, seed=123)
        assert weights1 != weights2
    
    def test_generate_weights_edge_cases(self):
        """Test edge cases for weight generation."""
        # Test with 1 horse
        weights = _generate_weights(1)
        assert len(weights) == 1
        assert 0.6 <= weights[0] <= 1.4
        
        # Test with many horses
        weights = _generate_weights(20)
        assert len(weights) == 20
        assert all(0.6 <= w <= 1.4 for w in weights)


class TestComputeDecimalOdds:
    """Test odds calculation logic."""
    
    def test_compute_odds_basic(self):
        """Test basic odds calculation."""
        weights = [1.0, 1.0, 1.0]
        odds = compute_decimal_odds(weights)
        assert len(odds) == 3
        assert all(odd >= 1.5 for odd in odds)  # Minimum odds check
    
    def test_compute_odds_house_edge(self):
        """Test that house edge is applied correctly."""
        weights = [1.0, 1.0, 1.0]  # Equal weights
        odds = compute_decimal_odds(weights)
        # With equal weights, each horse should have ~3.0 fair odds
        # With 10% house edge: 3.0 * 0.9 = 2.7, but clamped to 1.5 minimum
        expected_odds = [2.7, 2.7, 2.7]
        for i, (actual, expected) in enumerate(zip(odds, expected_odds)):
            assert abs(actual - expected) < 0.1, f"Odds {i}: expected ~{expected}, got {actual}"
    
    def test_compute_odds_favorite(self):
        """Test odds calculation with a clear favorite."""
        weights = [2.0, 0.5, 0.5]  # First horse is favorite
        odds = compute_decimal_odds(weights)
        # Favorite should have lower odds (higher probability)
        assert odds[0] < odds[1]
        assert odds[0] < odds[2]
        assert all(odd >= 1.5 for odd in odds)
    
    def test_compute_odds_empty_weights(self):
        """Test odds calculation with empty weights."""
        odds = compute_decimal_odds([])
        assert odds == []
    
    def test_compute_odds_zero_weights(self):
        """Test odds calculation with zero weights."""
        weights = [0.0, 0.0, 0.0]
        odds = compute_decimal_odds(weights)
        # Should handle zero weights gracefully
        assert len(odds) == 3
        assert all(odd >= 1.5 for odd in odds)


class TestBuildRace:
    """Test race profile building."""
    
    def test_build_race_basic(self):
        """Test basic race building."""
        race = build_race(5)
        assert "weights" in race
        assert "odds" in race
        assert "distance" in race
        assert "emoji" in race
        
        assert len(race["weights"]) == 5
        assert len(race["odds"]) == 5
        assert race["distance"] == 100
        assert race["emoji"] == "🐴"
    
    def test_build_race_with_seed(self):
        """Test race building with seed."""
        race1 = build_race(5, seed=42)
        race2 = build_race(5, seed=42)
        assert race1["weights"] == race2["weights"]
        assert race1["odds"] == race2["odds"]
    
    def test_build_race_consistency(self):
        """Test that weights and odds are consistent."""
        race = build_race(5, seed=42)
        # Recalculate odds from weights
        expected_odds = compute_decimal_odds(race["weights"])
        assert race["odds"] == expected_odds


class TestAnimacion:
    """Test race animation logic."""
    
    @patch('game.clear_screen')
    @patch('game.cprint')
    def test_animacion_basic(self, mock_cprint, mock_clear_screen, sample_race_profile):
        """Test basic animation functionality."""
        # Mock the translator function
        mock_t = MagicMock()
        mock_t.side_effect = lambda key, **kwargs: f"mock_{key}"
        
        # Test with fast mode to avoid timing issues
        winner = animacion(5, 1, mock_t, race_profile=sample_race_profile, fast=True)
        
        assert isinstance(winner, int)
        assert 1 <= winner <= 5
        mock_clear_screen.assert_called()
        mock_cprint.assert_called()
    
    @patch('game.clear_screen')
    @patch('game.cprint')
    def test_animacion_user_horse_highlighting(self, mock_cprint, mock_clear_screen, sample_race_profile):
        """Test that user's horse is highlighted correctly."""
        mock_t = MagicMock()
        mock_t.side_effect = lambda key, **kwargs: f"mock_{key}"
        
        # Test with different user horse selections
        for user_horse in range(1, 6):
            winner = animacion(5, user_horse, mock_t, race_profile=sample_race_profile, fast=True)
            assert isinstance(winner, int)
            assert 1 <= winner <= 5
    
    @patch('game.clear_screen')
    @patch('game.cprint')
    def test_animacion_race_completion(self, mock_cprint, mock_clear_screen, sample_race_profile):
        """Test that race completes and returns a winner."""
        mock_t = MagicMock()
        mock_t.side_effect = lambda key, **kwargs: f"mock_{key}"
        
        # Run multiple races to ensure completion
        for _ in range(10):
            winner = animacion(5, 1, mock_t, race_profile=sample_race_profile, fast=True)
            assert isinstance(winner, int)
            assert 1 <= winner <= 5
    
    @patch('game.clear_screen')
    @patch('game.cprint')
    def test_animacion_different_horse_counts(self, mock_cprint, mock_clear_screen):
        """Test animation with different numbers of horses."""
        mock_t = MagicMock()
        mock_t.side_effect = lambda key, **kwargs: f"mock_{key}"
        
        for num_horses in [2, 3, 5, 7, 10]:
            race = build_race(num_horses, seed=42)
            winner = animacion(num_horses, 1, mock_t, race_profile=race, fast=True)
            assert isinstance(winner, int)
            assert 1 <= winner <= num_horses
    
    @patch('game.clear_screen')
    @patch('game.cprint')
    def test_animacion_no_race_profile(self, mock_cprint, mock_clear_screen):
        """Test animation without providing race profile."""
        mock_t = MagicMock()
        mock_t.side_effect = lambda key, **kwargs: f"mock_{key}"
        
        winner = animacion(5, 1, mock_t, race_profile=None, fast=True)
        assert isinstance(winner, int)
        assert 1 <= winner <= 5


class TestGameDebugging:
    """Debugging-specific tests for common game issues."""
    
    def test_odds_calculation_debugging(self):
        """Test odds calculation for debugging edge cases."""
        # Test with extreme weights
        extreme_weights = [0.6, 1.4, 0.6, 1.4, 0.6]
        odds = compute_decimal_odds(extreme_weights)
        
        # Verify all odds are valid
        assert len(odds) == 5
        assert all(isinstance(odd, (int, float)) for odd in odds)
        assert all(odd >= 1.5 for odd in odds)
        assert all(odd < 100 for odd in odds)  # Reasonable upper bound
        
        # Verify favorites have lower odds
        favorite_indices = [1, 3]  # Indices with weight 1.4
        underdog_indices = [0, 2, 4]  # Indices with weight 0.6
        
        for fav_idx in favorite_indices:
            for under_idx in underdog_indices:
                assert odds[fav_idx] < odds[under_idx], f"Favorite {fav_idx} should have lower odds than underdog {under_idx}"
    
    def test_race_determinism_debugging(self):
        """Test race determinism for debugging reproducible issues."""
        # Test that same seed produces same race
        race1 = build_race(5, seed=12345)
        race2 = build_race(5, seed=12345)
        assert race1 == race2
        
        # Test that different seeds produce different races
        race3 = build_race(5, seed=54321)
        assert race1 != race3
    
    def test_weight_distribution_debugging(self):
        """Test weight distribution for debugging balance issues."""
        # Generate many weights and check distribution
        all_weights = []
        for _ in range(100):
            weights = _generate_weights(5, seed=None)  # Random seed
            all_weights.extend(weights)
        
        # Check that weights are within expected range
        assert all(0.6 <= w <= 1.4 for w in all_weights)
        
        # Check that we have reasonable distribution (not all same values)
        unique_weights = set(all_weights)
        assert len(unique_weights) > 10  # Should have variety
    
    def test_race_completion_debugging(self):
        """Test race completion for debugging infinite loops."""
        race = build_race(5, seed=42)
        
        # Test that race completes in reasonable time
        import time
        start_time = time.time()
        
        with patch('game.clear_screen'), patch('game.cprint'):
            mock_t = MagicMock()
            mock_t.side_effect = lambda key, **kwargs: f"mock_{key}"
            winner = animacion(5, 1, mock_t, race_profile=race, fast=True)
        
        end_time = time.time()
        duration = end_time - start_time
        
        assert duration < 1.0  # Should complete quickly in fast mode
        assert isinstance(winner, int)
        assert 1 <= winner <= 5
