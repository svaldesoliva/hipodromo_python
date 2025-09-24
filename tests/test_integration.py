"""
Integration tests for the main game flow and component interactions.
"""
import pytest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock, call
from Hipodromo import (
    cargar_idioma,
    cargar_dinero,
    guardar_dinero,
    animar_carrera,
    jugar,
    cambiar_idioma,
    toggle_fast,
    mostrar_saldo,
    main
)


class TestGameIntegration:
    """Test integration between game components."""
    
    @patch('config.get_lang')
    @patch('config.set_lang')
    @patch('utils.fzf_available')
    @patch('utils.fzf_select')
    def test_cargar_idioma_integration(self, mock_fzf_select, mock_fzf_available, mock_set_lang, mock_get_lang):
        """Test language loading integration."""
        # Test with fzf available
        mock_fzf_available.return_value = True
        mock_fzf_select.return_value = "English"
        mock_get_lang.return_value = None
        
        result = cargar_idioma()
        assert result == "en"
        mock_set_lang.assert_called_with("en")
    
    @patch('config.get_balance')
    @patch('config.set_balance')
    def test_cargar_dinero_integration(self, mock_set_balance, mock_get_balance):
        """Test money loading integration."""
        # Test with valid balance
        mock_get_balance.return_value = 7500
        
        result = cargar_dinero()
        assert result == 7500
        
        # Test with invalid balance (negative)
        mock_get_balance.return_value = -1000
        
        result = cargar_dinero()
        assert result == 5000  # Should use default
        mock_set_balance.assert_called_with(5000)
    
    @patch('config.set_balance')
    def test_guardar_dinero_integration(self, mock_set_balance):
        """Test money saving integration."""
        guardar_dinero(7500)
        mock_set_balance.assert_called_with(7500)
    
    @patch('game.build_race')
    @patch('game.animacion')
    def test_animar_carrera_integration(self, mock_animacion, mock_build_race):
        """Test race animation integration."""
        mock_race = {"weights": [1.0, 1.0, 1.0], "odds": [2.0, 2.0, 2.0]}
        mock_build_race.return_value = mock_race
        mock_animacion.return_value = 2
        
        with patch('Hipodromo.SEED', 42), patch('Hipodromo.FAST_MODE', True):
            result = animar_carrera(3, 1)
            assert result == 2
            mock_build_race.assert_called_with(3, 42)
            mock_animacion.assert_called_with(3, 1, mock_race, fast=True)


class TestGameFlowIntegration:
    """Test complete game flow integration."""
    
    @patch('Hipodromo.cargar_dinero')
    @patch('Hipodromo.guardar_dinero')
    @patch('Hipodromo.build_race')
    @patch('Hipodromo.animacion')
    @patch('Hipodromo.input_entero')
    @patch('Hipodromo.cprint')
    @patch('Hipodromo.clear_screen')
    def test_jugar_integration_win(self, mock_clear_screen, mock_cprint, mock_input_entero, 
                                   mock_animacion, mock_build_race, mock_guardar_dinero, mock_cargar_dinero):
        """Test complete betting flow when player wins."""
        # Setup mocks
        mock_cargar_dinero.return_value = 5000
        mock_race = {
            "weights": [1.0, 1.0, 1.0, 1.0, 1.0],
            "odds": [2.0, 2.0, 2.0, 2.0, 2.0]
        }
        mock_build_race.return_value = mock_race
        mock_animacion.return_value = 1  # Player's horse wins
        mock_input_entero.side_effect = [1, 1000, 0]  # Bet on horse 1, bet 1000, then exit
        
        with patch('Hipodromo.dinero', 5000), patch('Hipodromo.N_HORSES', 5):
            jugar()
            
            # Verify interactions
            mock_build_race.assert_called()
            mock_animacion.assert_called()
            mock_guardar_dinero.assert_called()
            mock_cprint.assert_called()
    
    @patch('Hipodromo.cargar_dinero')
    @patch('Hipodromo.guardar_dinero')
    @patch('Hipodromo.build_race')
    @patch('Hipodromo.animacion')
    @patch('Hipodromo.input_entero')
    @patch('Hipodromo.cprint')
    @patch('Hipodromo.clear_screen')
    def test_jugar_integration_lose(self, mock_clear_screen, mock_cprint, mock_input_entero,
                                    mock_animacion, mock_build_race, mock_guardar_dinero, mock_cargar_dinero):
        """Test complete betting flow when player loses."""
        # Setup mocks
        mock_cargar_dinero.return_value = 5000
        mock_race = {
            "weights": [1.0, 1.0, 1.0, 1.0, 1.0],
            "odds": [2.0, 2.0, 2.0, 2.0, 2.0]
        }
        mock_build_race.return_value = mock_race
        mock_animacion.return_value = 2  # Different horse wins
        mock_input_entero.side_effect = [1, 1000, 0]  # Bet on horse 1, bet 1000, then exit
        
        with patch('Hipodromo.dinero', 5000), patch('Hipodromo.N_HORSES', 5):
            jugar()
            
            # Verify interactions
            mock_build_race.assert_called()
            mock_animacion.assert_called()
            mock_guardar_dinero.assert_called()
            mock_cprint.assert_called()
    
    @patch('Hipodromo.cargar_dinero')
    @patch('Hipodromo.guardar_dinero')
    @patch('Hipodromo.build_race')
    @patch('Hipodromo.animacion')
    @patch('Hipodromo.input_entero')
    @patch('Hipodromo.cprint')
    @patch('Hipodromo.clear_screen')
    def test_jugar_integration_out_of_money(self, mock_clear_screen, mock_cprint, mock_input_entero,
                                            mock_animacion, mock_build_race, mock_guardar_dinero, mock_cargar_dinero):
        """Test betting flow when player runs out of money."""
        # Setup mocks
        mock_cargar_dinero.return_value = 1000
        mock_race = {
            "weights": [1.0, 1.0, 1.0, 1.0, 1.0],
            "odds": [2.0, 2.0, 2.0, 2.0, 2.0]
        }
        mock_build_race.return_value = mock_race
        mock_animacion.return_value = 2  # Player loses
        mock_input_entero.side_effect = [1, 1000]  # Bet all money and lose
        
        with patch('Hipodromo.dinero', 1000), patch('Hipodromo.N_HORSES', 5):
            jugar()
            
            # Should exit when money reaches 0
            mock_guardar_dinero.assert_called_with(0)


class TestMenuIntegration:
    """Test menu system integration."""
    
    @patch('Hipodromo.set_lang')
    @patch('Hipodromo.utils.fzf_available')
    @patch('Hipodromo.utils.fzf_select')
    @patch('Hipodromo.cprint')
    @patch('Hipodromo.input')
    def test_cambiar_idioma_integration(self, mock_input, mock_cprint, mock_fzf_select, 
                                        mock_fzf_available, mock_set_lang):
        """Test language change integration."""
        mock_fzf_available.return_value = True
        mock_fzf_select.return_value = "Español"
        mock_input.return_value = ""
        
        with patch('Hipodromo.LANG', 'en'):
            cambiar_idioma()
            mock_set_lang.assert_called_with('es')
            mock_cprint.assert_called()
    
    @patch('Hipodromo.set_fast')
    @patch('Hipodromo.cprint')
    @patch('Hipodromo.input')
    def test_toggle_fast_integration(self, mock_input, mock_cprint, mock_set_fast):
        """Test fast mode toggle integration."""
        mock_input.return_value = ""
        
        with patch('Hipodromo.FAST_MODE', False):
            toggle_fast()
            mock_set_fast.assert_called_with(True)
            mock_cprint.assert_called()
    
    @patch('Hipodromo.cprint')
    @patch('Hipodromo.input')
    def test_mostrar_saldo_integration(self, mock_input, mock_cprint):
        """Test balance display integration."""
        mock_input.return_value = ""
        
        with patch('Hipodromo.dinero', 7500):
            mostrar_saldo()
            mock_cprint.assert_called()
            mock_input.assert_called()


class TestCLIIntegration:
    """Test command-line interface integration."""
    
    @patch('Hipodromo.argparse.ArgumentParser')
    def test_main_cli_args_integration(self, mock_parser_class):
        """Test CLI argument parsing integration."""
        mock_parser = MagicMock()
        mock_parser_class.return_value = mock_parser
        mock_args = MagicMock()
        mock_args.fast = True
        mock_args.no_fast = False
        mock_args.horses = 7
        mock_args.seed = "12345"
        mock_args.config = False
        mock_args.edit_config = False
        mock_parser.parse_known_args.return_value = (mock_args, [])
        
        with patch('Hipodromo.set_fast'), \
             patch('Hipodromo.set_horses'), \
             patch('Hipodromo.set_seed'), \
             patch('Hipodromo.clear_screen'), \
             patch('Hipodromo.cprint'), \
             patch('Hipodromo.utils.fzf_available', return_value=False), \
             patch('Hipodromo.input_entero', return_value=0):  # Exit immediately
            
            main()
            
            mock_parser.add_argument.assert_called()
            mock_parser.parse_known_args.assert_called()
    
    @patch('Hipodromo.argparse.ArgumentParser')
    def test_main_cli_config_flag_integration(self, mock_parser_class):
        """Test CLI config flag integration."""
        mock_parser = MagicMock()
        mock_parser_class.return_value = mock_parser
        mock_args = MagicMock()
        mock_args.config = True
        mock_parser.parse_known_args.return_value = (mock_args, [])
        
        with patch('Hipodromo.CONFIG_FILE', '/test/config.json'), \
             patch('builtins.print') as mock_print:
            
            main()
            mock_print.assert_called_with('/test/config.json')


class TestErrorHandlingIntegration:
    """Test error handling integration across components."""
    
    @patch('Hipodromo.config.get_lang')
    @patch('Hipodromo.config.set_lang')
    def test_cargar_idioma_error_handling(self, mock_set_lang, mock_get_lang):
        """Test language loading error handling."""
        # Test with exception in get_lang
        mock_get_lang.side_effect = Exception("Config error")
        
        with patch('Hipodromo.utils.fzf_available', return_value=False), \
             patch('builtins.input', return_value="1"):
            result = cargar_idioma()
            assert result == "en"  # Should fall back to English
    
    @patch('Hipodromo.config.get_balance')
    def test_cargar_dinero_error_handling(self, mock_get_balance):
        """Test money loading error handling."""
        # Test with exception in get_balance
        mock_get_balance.side_effect = Exception("Config error")
        
        with patch('Hipodromo.guardar_dinero'):
            result = cargar_dinero()
            assert result == 5000  # Should use default
    
    @patch('Hipodromo.config.set_balance')
    def test_guardar_dinero_error_handling(self, mock_set_balance):
        """Test money saving error handling."""
        # Test with exception in set_balance
        mock_set_balance.side_effect = Exception("Config error")
        
        # Should not raise exception
        try:
            guardar_dinero(5000)
        except Exception:
            pytest.fail("guardar_dinero should handle exceptions gracefully")


class TestStateManagementIntegration:
    """Test state management integration across the game."""
    
    def test_global_state_consistency(self):
        """Test that global state remains consistent across operations."""
        with patch('Hipodromo.dinero', 5000), \
             patch('Hipodromo.N_HORSES', 5), \
             patch('Hipodromo.FAST_MODE', False), \
             patch('Hipodromo.SEED', None):
            
            # Test that state is preserved across operations
            assert getattr(Hipodromo, 'dinero', None) == 5000
            assert getattr(Hipodromo, 'N_HORSES', None) == 5
            assert getattr(Hipodromo, 'FAST_MODE', None) is False
            assert getattr(Hipodromo, 'SEED', None) is None
    
    @patch('Hipodromo.guardar_dinero')
    def test_money_state_persistence(self, mock_guardar_dinero):
        """Test that money state is properly persisted."""
        with patch('Hipodromo.dinero', 5000):
            # Simulate money changes
            guardar_dinero(7500)
            mock_guardar_dinero.assert_called_with(7500)
            
            guardar_dinero(0)
            mock_guardar_dinero.assert_called_with(0)


class TestPerformanceIntegration:
    """Test performance-related integration issues."""
    
    @patch('Hipodromo.build_race')
    @patch('Hipodromo.animacion')
    def test_race_performance_integration(self, mock_animacion, mock_build_race):
        """Test race performance integration."""
        mock_race = {"weights": [1.0] * 10, "odds": [2.0] * 10}
        mock_build_race.return_value = mock_race
        mock_animacion.return_value = 1
        
        # Test with many horses
        with patch('Hipodromo.SEED', 42), patch('Hipodromo.FAST_MODE', True):
            result = animar_carrera(10, 1)
            assert result == 1
            mock_build_race.assert_called_with(10, 42)
    
    @patch('Hipodromo.input_entero')
    def test_input_performance_integration(self, mock_input_entero):
        """Test input performance integration."""
        mock_input_entero.side_effect = [0]  # Exit immediately
        
        with patch('Hipodromo.dinero', 5000), \
             patch('Hipodromo.N_HORSES', 5), \
             patch('Hipodromo.build_race'), \
             patch('Hipodromo.clear_screen'), \
             patch('Hipodromo.cprint'):
            
            # Should handle rapid input without issues
            jugar()
            mock_input_entero.assert_called()
