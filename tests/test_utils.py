"""
Tests for utils.py - Utility functions for input validation, screen clearing, and fzf integration.
"""
import os
import subprocess
import pytest
from unittest.mock import patch, MagicMock, call
from utils import (
    clear_screen,
    input_entero,
    fzf_available,
    fzf_select
)


class TestClearScreen:
    """Test screen clearing functionality."""
    
    @patch('os.system')
    def test_clear_screen_windows(self, mock_system):
        """Test screen clearing on Windows."""
        with patch('os.name', 'nt'):
            clear_screen()
            mock_system.assert_called_once_with("cls")
    
    @patch('os.system')
    def test_clear_screen_unix(self, mock_system):
        """Test screen clearing on Unix-like systems."""
        with patch('os.name', 'posix'):
            clear_screen()
            mock_system.assert_called_once_with("clear")
    
    @patch('os.system')
    def test_clear_screen_other_os(self, mock_system):
        """Test screen clearing on other operating systems."""
        with patch('os.name', 'java'):  # Some other OS
            clear_screen()
            mock_system.assert_called_once_with("clear")


class TestInputEntero:
    """Test integer input validation."""
    
    @patch('builtins.input')
    def test_input_entero_valid_input(self, mock_input):
        """Test valid integer input."""
        mock_input.return_value = "5"
        result = input_entero("Enter a number: ")
        assert result == 5
    
    @patch('builtins.input')
    def test_input_entero_with_min_max(self, mock_input):
        """Test integer input with min/max constraints."""
        mock_input.return_value = "3"
        result = input_entero("Enter a number: ", minimo=1, maximo=10)
        assert result == 3
    
    @patch('builtins.input')
    def test_input_entero_minimum_violation(self, mock_input):
        """Test input below minimum value."""
        mock_input.side_effect = ["0", "5"]  # First input too low, second valid
        result = input_entero("Enter a number: ", minimo=1, maximo=10)
        assert result == 5
        assert mock_input.call_count == 2
    
    @patch('builtins.input')
    def test_input_entero_maximum_violation(self, mock_input):
        """Test input above maximum value."""
        mock_input.side_effect = ["15", "5"]  # First input too high, second valid
        result = input_entero("Enter a number: ", minimo=1, maximo=10)
        assert result == 5
        assert mock_input.call_count == 2
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_input_entero_invalid_input_with_message(self, mock_print, mock_input):
        """Test invalid input with custom error message."""
        mock_input.side_effect = ["abc", "5"]  # First input invalid, second valid
        result = input_entero("Enter a number: ", invalid_msg="Invalid input!")
        assert result == 5
        mock_print.assert_called_with("Invalid input!")
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_input_entero_min_violation_with_message(self, mock_input, mock_print):
        """Test minimum violation with custom message."""
        mock_input.side_effect = ["0", "5"]
        result = input_entero("Enter a number: ", minimo=1, min_msg="Too low!")
        assert result == 5
        mock_print.assert_called_with("Too low!")
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_input_entero_max_violation_with_message(self, mock_input, mock_print):
        """Test maximum violation with custom message."""
        mock_input.side_effect = ["15", "5"]
        result = input_entero("Enter a number: ", maximo=10, max_msg="Too high!")
        assert result == 5
        mock_print.assert_called_with("Too high!")
    
    @patch('builtins.input')
    def test_input_entero_edge_cases(self, mock_input):
        """Test edge cases for integer input."""
        # Test with no constraints
        mock_input.return_value = "0"
        result = input_entero("Enter a number: ")
        assert result == 0
        
        # Test with negative numbers
        mock_input.return_value = "-5"
        result = input_entero("Enter a number: ")
        assert result == -5
        
        # Test with large numbers
        mock_input.return_value = "999999"
        result = input_entero("Enter a number: ")
        assert result == 999999
    
    @patch('builtins.input')
    def test_input_entero_multiple_invalid_inputs(self, mock_input):
        """Test multiple invalid inputs before valid one."""
        mock_input.side_effect = ["abc", "xyz", "12.5", "5"]
        result = input_entero("Enter a number: ")
        assert result == 5
        assert mock_input.call_count == 4


class TestFzfAvailable:
    """Test fzf availability checking."""
    
    @patch('shutil.which')
    def test_fzf_available_true(self, mock_which):
        """Test when fzf is available."""
        mock_which.return_value = "/usr/bin/fzf"
        assert fzf_available() is True
        mock_which.assert_called_once_with("fzf")
    
    @patch('shutil.which')
    def test_fzf_available_false(self, mock_which):
        """Test when fzf is not available."""
        mock_which.return_value = None
        assert fzf_available() is False
        mock_which.assert_called_once_with("fzf")
    
    @patch('shutil.which')
    def test_fzf_available_exception(self, mock_which):
        """Test when shutil.which raises an exception."""
        mock_which.side_effect = Exception("Permission denied")
        assert fzf_available() is False


class TestFzfSelect:
    """Test fzf selection functionality."""
    
    @patch('subprocess.run')
    def test_fzf_select_success(self, mock_run):
        """Test successful fzf selection."""
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "Selected Option\n"
        mock_run.return_value = mock_proc
        
        options = ["Option 1", "Option 2", "Option 3"]
        result = fzf_select(options, "Choose:")
        
        assert result == "Selected Option"
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0] == ["fzf", "--prompt", "Choose: "]
        assert call_args[1]["input"] == "Option 1\nOption 2\nOption 3"
        assert call_args[1]["capture_output"] is True
        assert call_args[1]["text"] is True
        assert call_args[1]["check"] is False
    
    @patch('subprocess.run')
    def test_fzf_select_cancelled(self, mock_run):
        """Test fzf selection when cancelled."""
        mock_proc = MagicMock()
        mock_proc.returncode = 1  # Non-zero return code indicates cancellation
        mock_run.return_value = mock_proc
        
        options = ["Option 1", "Option 2"]
        result = fzf_select(options, "Choose:")
        
        assert result is None
    
    @patch('subprocess.run')
    def test_fzf_select_empty_options(self, mock_run):
        """Test fzf selection with empty options list."""
        result = fzf_select([], "Choose:")
        assert result is None
        mock_run.assert_not_called()
    
    @patch('subprocess.run')
    def test_fzf_select_none_options(self, mock_run):
        """Test fzf selection with None options."""
        result = fzf_select(None, "Choose:")
        assert result is None
        mock_run.assert_not_called()
    
    @patch('subprocess.run')
    def test_fzf_select_exception(self, mock_run):
        """Test fzf selection when subprocess raises exception."""
        mock_run.side_effect = FileNotFoundError("fzf not found")
        
        options = ["Option 1", "Option 2"]
        result = fzf_select(options, "Choose:")
        
        assert result is None
    
    @patch('subprocess.run')
    def test_fzf_select_single_option(self, mock_run):
        """Test fzf selection with single option."""
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "Only Option\n"
        mock_run.return_value = mock_proc
        
        options = ["Only Option"]
        result = fzf_select(options, "Choose:")
        
        assert result == "Only Option"
        call_args = mock_run.call_args
        assert call_args[1]["input"] == "Only Option"
    
    @patch('subprocess.run')
    def test_fzf_select_whitespace_handling(self, mock_run):
        """Test fzf selection with whitespace in options."""
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "  Option with spaces  \n"
        mock_run.return_value = mock_proc
        
        options = ["Option with spaces"]
        result = fzf_select(options, "Choose:")
        
        assert result == "Option with spaces"  # Should strip whitespace
    
    @patch('subprocess.run')
    def test_fzf_select_special_characters(self, mock_run):
        """Test fzf selection with special characters."""
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "Option with émojis 🐎\n"
        mock_run.return_value = mock_proc
        
        options = ["Option with émojis 🐎"]
        result = fzf_select(options, "Choose:")
        
        assert result == "Option with émojis 🐎"


class TestUtilsEdgeCases:
    """Test edge cases in utility functions."""
    
    @patch('builtins.input')
    def test_input_entero_empty_input(self, mock_input):
        """Test input_entero with empty input."""
        mock_input.side_effect = ["", "5"]
        result = input_entero("Enter a number: ")
        assert result == 5
    
    @patch('builtins.input')
    def test_input_entero_whitespace_input(self, mock_input):
        """Test input_entero with whitespace input."""
        mock_input.side_effect = ["   ", "5"]
        result = input_entero("Enter a number: ")
        assert result == 5
    
    @patch('builtins.input')
    def test_input_entero_float_input(self, mock_input):
        """Test input_entero with float input."""
        mock_input.side_effect = ["3.14", "5"]
        result = input_entero("Enter a number: ")
        assert result == 5
    
    @patch('subprocess.run')
    def test_fzf_select_empty_stdout(self, mock_run):
        """Test fzf selection with empty stdout."""
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = ""
        mock_run.return_value = mock_proc
        
        options = ["Option 1"]
        result = fzf_select(options, "Choose:")
        
        assert result == ""


class TestUtilsDebugging:
    """Debugging-specific tests for utility functions."""
    
    @patch('builtins.input')
    def test_input_entero_debugging_loop(self, mock_input):
        """Test input_entero debugging for infinite loops."""
        # Simulate a scenario that could cause infinite loops
        mock_input.side_effect = ["invalid"] * 10 + ["5"]
        result = input_entero("Enter a number: ")
        assert result == 5
        assert mock_input.call_count == 11
    
    @patch('subprocess.run')
    def test_fzf_select_debugging_timeout(self, mock_run):
        """Test fzf selection debugging for timeout issues."""
        # Simulate a timeout scenario
        mock_run.side_effect = subprocess.TimeoutExpired("fzf", 30)
        
        options = ["Option 1", "Option 2"]
        result = fzf_select(options, "Choose:")
        
        assert result is None
    
    @patch('subprocess.run')
    def test_fzf_select_debugging_permission_error(self, mock_run):
        """Test fzf selection debugging for permission errors."""
        # Simulate permission error
        mock_run.side_effect = PermissionError("Permission denied")
        
        options = ["Option 1", "Option 2"]
        result = fzf_select(options, "Choose:")
        
        assert result is None
    
    @patch('builtins.input')
    def test_input_entero_debugging_unicode(self, mock_input):
        """Test input_entero debugging for unicode issues."""
        # Test with unicode characters
        mock_input.side_effect = ["café", "5"]
        result = input_entero("Enter a number: ")
        assert result == 5
    
    @patch('subprocess.run')
    def test_fzf_select_debugging_unicode_options(self, mock_run):
        """Test fzf selection debugging for unicode options."""
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "Café\n"
        mock_run.return_value = mock_proc
        
        options = ["Café", "Español"]
        result = fzf_select(options, "Choose:")
        
        assert result == "Café"
    
    @patch('os.system')
    def test_clear_screen_debugging_error_handling(self, mock_system):
        """Test clear_screen debugging for system errors."""
        # Simulate system command failure
        mock_system.side_effect = OSError("Command not found")
        
        # Should not raise exception
        try:
            clear_screen()
        except OSError:
            pytest.fail("clear_screen should handle OSError gracefully")
    
    @patch('builtins.input')
    def test_input_entero_debugging_boundary_values(self, mock_input):
        """Test input_entero debugging with boundary values."""
        # Test exact boundary values
        mock_input.return_value = "1"
        result = input_entero("Enter a number: ", minimo=1, maximo=10)
        assert result == 1
        
        mock_input.return_value = "10"
        result = input_entero("Enter a number: ", minimo=1, maximo=10)
        assert result == 10
        
        # Test just outside boundaries
        mock_input.side_effect = ["0", "11", "5"]
        result = input_entero("Enter a number: ", minimo=1, maximo=10)
        assert result == 5
        assert mock_input.call_count == 3
