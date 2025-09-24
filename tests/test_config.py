"""
Tests for config.py - Configuration management and persistence.
"""
import os
import json
import tempfile
import shutil
import pytest
from unittest.mock import patch, mock_open
from config import (
    CONFIG_DIR,
    CONFIG_FILE,
    _read_legacy_value,
    _load_config_from_disk,
    _write_config_to_disk,
    _ensure_and_migrate_config,
    get_lang,
    set_lang,
    get_balance,
    set_balance,
    get_fast,
    set_fast,
    get_horses,
    set_horses,
    get_seed,
    set_seed
)


class TestConfigFileOperations:
    """Test basic config file operations."""
    
    def test_read_legacy_value_success(self, temp_config_dir):
        """Test reading legacy value from file."""
        test_file = os.path.join(temp_config_dir, "test_file")
        with open(test_file, 'w') as f:
            f.write("test_value")
        
        result = _read_legacy_value(test_file)
        assert result == "test_value"
    
    def test_read_legacy_value_with_coerce(self, temp_config_dir):
        """Test reading legacy value with type coercion."""
        test_file = os.path.join(temp_config_dir, "test_file")
        with open(test_file, 'w') as f:
            f.write("123")
        
        result = _read_legacy_value(test_file, coerce=int)
        assert result == 123
    
    def test_read_legacy_value_nonexistent(self, temp_config_dir):
        """Test reading from nonexistent file."""
        test_file = os.path.join(temp_config_dir, "nonexistent")
        result = _read_legacy_value(test_file)
        assert result is None
    
    def test_read_legacy_value_invalid_coerce(self, temp_config_dir):
        """Test reading with invalid coercion."""
        test_file = os.path.join(temp_config_dir, "test_file")
        with open(test_file, 'w') as f:
            f.write("not_a_number")
        
        result = _read_legacy_value(test_file, coerce=int)
        assert result is None
    
    def test_load_config_from_disk_success(self, temp_config_dir):
        """Test loading config from disk."""
        config_file = os.path.join(temp_config_dir, "config.json")
        config_data = {"balance": 1000, "lang": "en"}
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        result = _load_config_from_disk()
        assert result == config_data
    
    def test_load_config_from_disk_nonexistent(self, temp_config_dir):
        """Test loading config from nonexistent file."""
        with patch('config.CONFIG_FILE', os.path.join(temp_config_dir, "nonexistent.json")):
            result = _load_config_from_disk()
            assert result == {}
    
    def test_load_config_from_disk_invalid_json(self, temp_config_dir):
        """Test loading config from invalid JSON file."""
        config_file = os.path.join(temp_config_dir, "config.json")
        with open(config_file, 'w') as f:
            f.write("invalid json content")
        
        result = _load_config_from_disk()
        assert result == {}
    
    def test_write_config_to_disk_success(self, temp_config_dir):
        """Test writing config to disk."""
        config_data = {"balance": 1000, "lang": "en"}
        
        with patch('config.CONFIG_DIR', temp_config_dir):
            _write_config_to_disk(config_data)
            
            config_file = os.path.join(temp_config_dir, "config.json")
            assert os.path.exists(config_file)
            
            with open(config_file, 'r') as f:
                loaded_data = json.load(f)
            assert loaded_data == config_data


class TestConfigMigration:
    """Test configuration migration from legacy files."""
    
    def test_migrate_legacy_balance(self, temp_config_dir):
        """Test migration of legacy balance file."""
        # Create legacy balance file
        legacy_balance_file = os.path.join(temp_config_dir, "balance")
        with open(legacy_balance_file, 'w') as f:
            f.write("7500")
        
        with patch('config.CONFIG_DIR', temp_config_dir), \
             patch('config.BALANCE_FILE', legacy_balance_file), \
             patch('config.OLD_BALANCE_FILE', os.path.join(temp_config_dir, "nonexistent")):
            
            config = _ensure_and_migrate_config()
            assert config["balance"] == 7500
    
    def test_migrate_legacy_lang(self, temp_config_dir):
        """Test migration of legacy language file."""
        # Create legacy language file
        legacy_lang_file = os.path.join(temp_config_dir, "lang")
        with open(legacy_lang_file, 'w') as f:
            f.write("es")
        
        with patch('config.CONFIG_DIR', temp_config_dir), \
             patch('config.LANG_FILE', legacy_lang_file), \
             patch('config.OLD_LANG_FILE', os.path.join(temp_config_dir, "nonexistent")):
            
            config = _ensure_and_migrate_config()
            assert config["lang"] == "es"
    
    def test_migrate_invalid_legacy_values(self, temp_config_dir):
        """Test migration with invalid legacy values."""
        # Create invalid legacy files
        legacy_balance_file = os.path.join(temp_config_dir, "balance")
        legacy_lang_file = os.path.join(temp_config_dir, "lang")
        
        with open(legacy_balance_file, 'w') as f:
            f.write("invalid_number")
        with open(legacy_lang_file, 'w') as f:
            f.write("invalid_lang")
        
        with patch('config.CONFIG_DIR', temp_config_dir), \
             patch('config.BALANCE_FILE', legacy_balance_file), \
             patch('config.LANG_FILE', legacy_lang_file), \
             patch('config.OLD_BALANCE_FILE', os.path.join(temp_config_dir, "nonexistent")), \
             patch('config.OLD_LANG_FILE', os.path.join(temp_config_dir, "nonexistent")):
            
            config = _ensure_and_migrate_config()
            assert config["balance"] == 5000  # Default value
            assert config["lang"] is None  # Default value
    
    def test_migrate_negative_balance(self, temp_config_dir):
        """Test migration with negative balance."""
        legacy_balance_file = os.path.join(temp_config_dir, "balance")
        with open(legacy_balance_file, 'w') as f:
            f.write("-1000")
        
        with patch('config.CONFIG_DIR', temp_config_dir), \
             patch('config.BALANCE_FILE', legacy_balance_file), \
             patch('config.OLD_BALANCE_FILE', os.path.join(temp_config_dir, "nonexistent")):
            
            config = _ensure_and_migrate_config()
            assert config["balance"] == 5000  # Should use default for negative balance


class TestConfigGettersSetters:
    """Test configuration getter and setter functions."""
    
    def test_lang_operations(self, temp_config_dir):
        """Test language getter and setter."""
        with patch('config.CONFIG_DIR', temp_config_dir):
            # Test default value
            assert get_lang() is None
            
            # Test setting and getting
            set_lang("en")
            assert get_lang() == "en"
            
            set_lang("es")
            assert get_lang() == "es"
    
    def test_balance_operations(self, temp_config_dir):
        """Test balance getter and setter."""
        with patch('config.CONFIG_DIR', temp_config_dir):
            # Test default value
            assert get_balance() == 5000
            
            # Test setting and getting
            set_balance(7500)
            assert get_balance() == 7500
            
            set_balance(0)
            assert get_balance() == 0
    
    def test_fast_operations(self, temp_config_dir):
        """Test fast mode getter and setter."""
        with patch('config.CONFIG_DIR', temp_config_dir):
            # Test default value
            assert get_fast() is False
            
            # Test setting and getting
            set_fast(True)
            assert get_fast() is True
            
            set_fast(False)
            assert get_fast() is False
    
    def test_horses_operations(self, temp_config_dir):
        """Test horses count getter and setter."""
        with patch('config.CONFIG_DIR', temp_config_dir):
            # Test default value
            assert get_horses() == 5
            
            # Test setting and getting
            set_horses(7)
            assert get_horses() == 7
            
            set_horses(3)
            assert get_horses() == 3
    
    def test_seed_operations(self, temp_config_dir):
        """Test seed getter and setter."""
        with patch('config.CONFIG_DIR', temp_config_dir):
            # Test default value
            assert get_seed() is None
            
            # Test setting and getting
            set_seed(12345)
            assert get_seed() == 12345
            
            set_seed("test_seed")
            assert get_seed() == "test_seed"
            
            set_seed(None)
            assert get_seed() is None


class TestConfigEdgeCases:
    """Test edge cases and error handling in configuration."""
    
    def test_balance_edge_cases(self, temp_config_dir):
        """Test balance edge cases."""
        with patch('config.CONFIG_DIR', temp_config_dir):
            # Test negative balance handling
            set_balance(-1000)
            assert get_balance() == 5000  # Should return default
            
            # Test very large balance
            set_balance(999999999)
            assert get_balance() == 999999999
    
    def test_horses_edge_cases(self, temp_config_dir):
        """Test horses count edge cases."""
        with patch('config.CONFIG_DIR', temp_config_dir):
            # Test minimum horses
            set_horses(2)
            assert get_horses() == 2
            
            # Test invalid horses count
            set_horses(1)
            assert get_horses() == 5  # Should return default
            
            set_horses(0)
            assert get_horses() == 5  # Should return default
    
    def test_lang_edge_cases(self, temp_config_dir):
        """Test language edge cases."""
        with patch('config.CONFIG_DIR', temp_config_dir):
            # Test invalid language
            set_lang("invalid")
            assert get_lang() == "invalid"  # Should accept any string
            
            # Test None language
            set_lang(None)
            assert get_lang() is None
    
    def test_seed_edge_cases(self, temp_config_dir):
        """Test seed edge cases."""
        with patch('config.CONFIG_DIR', temp_config_dir):
            # Test integer seed
            set_seed(42)
            assert get_seed() == 42
            
            # Test string seed
            set_seed("test")
            assert get_seed() == "test"
            
            # Test float seed
            set_seed(3.14)
            assert get_seed() == 3.14


class TestConfigDebugging:
    """Debugging-specific tests for configuration issues."""
    
    def test_config_file_corruption_recovery(self, temp_config_dir):
        """Test recovery from corrupted config file."""
        config_file = os.path.join(temp_config_dir, "config.json")
        
        # Create corrupted config file
        with open(config_file, 'w') as f:
            f.write("corrupted json content")
        
        with patch('config.CONFIG_DIR', temp_config_dir):
            # Should recover gracefully
            config = _ensure_and_migrate_config()
            assert isinstance(config, dict)
            assert "balance" in config
            assert "lang" in config
            assert "fast" in config
            assert "horses" in config
            assert "seed" in config
    
    def test_config_directory_creation(self, temp_config_dir):
        """Test config directory creation."""
        # Use a non-existent subdirectory
        config_subdir = os.path.join(temp_config_dir, "nonexistent", "config")
        
        with patch('config.CONFIG_DIR', config_subdir):
            config = _ensure_and_migrate_config()
            assert os.path.exists(config_subdir)
            assert isinstance(config, dict)
    
    def test_config_persistence_across_sessions(self, temp_config_dir):
        """Test that config persists across multiple sessions."""
        with patch('config.CONFIG_DIR', temp_config_dir):
            # First session
            set_balance(7500)
            set_lang("es")
            set_fast(True)
            set_horses(7)
            set_seed(12345)
            
            # Simulate new session by reloading
            config = _ensure_and_migrate_config()
            assert config["balance"] == 7500
            assert config["lang"] == "es"
            assert config["fast"] is True
            assert config["horses"] == 7
            assert config["seed"] == 12345
    
    def test_config_concurrent_access(self, temp_config_dir):
        """Test config access patterns that might cause issues."""
        with patch('config.CONFIG_DIR', temp_config_dir):
            # Rapid successive changes
            for i in range(10):
                set_balance(1000 + i)
                set_fast(i % 2 == 0)
                set_horses(5 + (i % 3))
            
            # Verify final state
            assert get_balance() == 1009
            assert get_fast() is False
            assert get_horses() == 7
    
    def test_config_migration_priority(self, temp_config_dir):
        """Test migration priority between different legacy files."""
        # Create both old and new legacy files
        old_balance_file = os.path.join(temp_config_dir, "old_balance")
        new_balance_file = os.path.join(temp_config_dir, "new_balance")
        
        with open(old_balance_file, 'w') as f:
            f.write("1000")
        with open(new_balance_file, 'w') as f:
            f.write("2000")
        
        with patch('config.CONFIG_DIR', temp_config_dir), \
             patch('config.BALANCE_FILE', new_balance_file), \
             patch('config.OLD_BALANCE_FILE', old_balance_file):
            
            config = _ensure_and_migrate_config()
            # Should prefer the newer file
            assert config["balance"] == 2000
