"""
Tests for i18n.py - Internationalization and translation system.
"""
import pytest
from i18n import TRANSLATIONS, translator


class TestTranslations:
    """Test translation data structure and content."""
    
    def test_translations_structure(self):
        """Test that translations have the expected structure."""
        assert isinstance(TRANSLATIONS, dict)
        assert "en" in TRANSLATIONS
        assert "es" in TRANSLATIONS
        
        # Check that both languages have the same keys
        en_keys = set(TRANSLATIONS["en"].keys())
        es_keys = set(TRANSLATIONS["es"].keys())
        assert en_keys == es_keys, "English and Spanish translations should have the same keys"
    
    def test_required_translation_keys(self):
        """Test that all required translation keys are present."""
        required_keys = {
            "title", "menu_header", "menu_play", "menu_change_lang", 
            "menu_show_balance", "menu_exit", "menu_prompt", "invalid_option",
            "current_balance", "language_changed_es", "language_changed_en",
            "enter_number_min", "enter_number_max", "invalid_int",
            "horse_name", "winner_suffix", "winner_announcement",
            "bet_prompt", "thanks", "how_much_to_bet", "you_win",
            "press_enter_continue", "you_lose", "press_enter_continue_alt",
            "out_of_money", "language_prompt", "odds_header", "odds_line",
            "fast_on", "fast_off", "set_horses", "menu_toggle_fast"
        }
        
        for lang in ["en", "es"]:
            lang_keys = set(TRANSLATIONS[lang].keys())
            missing_keys = required_keys - lang_keys
            assert not missing_keys, f"Missing keys in {lang}: {missing_keys}"
    
    def test_translation_content_quality(self):
        """Test translation content quality and consistency."""
        # Check that translations are not empty
        for lang in ["en", "es"]:
            for key, value in TRANSLATIONS[lang].items():
                assert isinstance(value, str), f"{lang}.{key} should be a string"
                assert len(value.strip()) > 0, f"{lang}.{key} should not be empty"
        
        # Check that titles are different between languages
        assert TRANSLATIONS["en"]["title"] != TRANSLATIONS["es"]["title"]
        
        # Check that menu options are different
        assert TRANSLATIONS["en"]["menu_play"] != TRANSLATIONS["es"]["menu_play"]
        assert TRANSLATIONS["en"]["menu_exit"] != TRANSLATIONS["es"]["menu_exit"]
    
    def test_placeholder_consistency(self):
        """Test that placeholders are consistent between languages."""
        # Find all placeholders in both languages
        en_placeholders = set()
        es_placeholders = set()
        
        for key, value in TRANSLATIONS["en"].items():
            import re
            placeholders = re.findall(r'\{(\w+)\}', value)
            en_placeholders.update(placeholders)
        
        for key, value in TRANSLATIONS["es"].items():
            import re
            placeholders = re.findall(r'\{(\w+)\}', value)
            es_placeholders.update(placeholders)
        
        # Placeholders should be the same in both languages
        assert en_placeholders == es_placeholders, f"Placeholder mismatch: EN={en_placeholders}, ES={es_placeholders}"


class TestTranslator:
    """Test translator function functionality."""
    
    def test_translator_english(self):
        """Test English translator."""
        t = translator("en")
        
        # Test basic translation
        assert t("title") == "Hippodrome v0.3\n"
        assert t("menu_play") == "1) Play"
        assert t("menu_exit") == "0) Exit"
    
    def test_translator_spanish(self):
        """Test Spanish translator."""
        t = translator("es")
        
        # Test basic translation
        assert t("title") == "Hipódromo v0.3\n"
        assert t("menu_play") == "1) Jugar"
        assert t("menu_exit") == "0) Salir"
    
    def test_translator_with_placeholders(self):
        """Test translator with placeholder substitution."""
        t = translator("en")
        
        # Test with placeholders
        result = t("current_balance", dinero=1000)
        assert "1000" in result
        assert "$" in result
        
        result = t("horse_name", idx=3)
        assert "3" in result
        assert "Horse" in result
        
        result = t("you_win", ganancia=500, dinero=1500)
        assert "500" in result
        assert "1500" in result
    
    def test_translator_spanish_placeholders(self):
        """Test Spanish translator with placeholders."""
        t = translator("es")
        
        # Test with placeholders
        result = t("current_balance", dinero=1000)
        assert "1000" in result
        assert "$" in result
        
        result = t("horse_name", idx=3)
        assert "3" in result
        assert "Caballo" in result
        
        result = t("you_win", ganancia=500, dinero=1500)
        assert "500" in result
        assert "1500" in result
    
    def test_translator_invalid_key(self):
        """Test translator with invalid key."""
        t = translator("en")
        
        # Should return empty string for invalid key
        result = t("invalid_key")
        assert result == ""
    
    def test_translator_invalid_language(self):
        """Test translator with invalid language."""
        # Should fall back to Spanish for invalid language
        t = translator("invalid_lang")
        result = t("title")
        assert result == "Hipódromo v0.3\n"  # Spanish fallback
    
    def test_translator_missing_placeholders(self):
        """Test translator with missing placeholder values."""
        t = translator("en")
        
        # Should handle missing placeholders gracefully
        result = t("current_balance")  # Missing dinero parameter
        assert "dinero" in result or result == ""  # Either shows placeholder or empty
    
    def test_translator_extra_placeholders(self):
        """Test translator with extra placeholder values."""
        t = translator("en")
        
        # Should ignore extra parameters
        result = t("title", extra_param="ignored")
        assert result == "Hippodrome v0.3\n"


class TestTranslationEdgeCases:
    """Test edge cases in translation system."""
    
    def test_translator_empty_string_key(self):
        """Test translator with empty string key."""
        t = translator("en")
        result = t("")
        assert result == ""
    
    def test_translator_none_key(self):
        """Test translator with None key."""
        t = translator("en")
        result = t(None)
        assert result == ""
    
    def test_translator_special_characters(self):
        """Test translator with special characters in placeholders."""
        t = translator("en")
        
        # Test with special characters
        result = t("you_win", ganancia="500$", dinero="1,500")
        assert "500$" in result or "1,500" in result
    
    def test_translator_unicode_characters(self):
        """Test translator with unicode characters."""
        t = translator("es")
        
        # Spanish should handle unicode characters properly
        result = t("title")
        assert "ó" in result  # Should contain accented character


class TestTranslationDebugging:
    """Debugging-specific tests for translation issues."""
    
    def test_translation_key_coverage(self):
        """Test that all translation keys are used in the codebase."""
        # This test helps identify unused translation keys
        all_keys = set()
        for lang in TRANSLATIONS:
            all_keys.update(TRANSLATIONS[lang].keys())
        
        # Common keys that should definitely exist
        critical_keys = {
            "title", "menu_play", "menu_exit", "bet_prompt", 
            "you_win", "you_lose", "current_balance"
        }
        
        for key in critical_keys:
            assert key in all_keys, f"Critical translation key '{key}' is missing"
    
    def test_translation_placeholder_validation(self):
        """Test that all placeholders in translations are valid."""
        import re
        
        for lang in ["en", "es"]:
            for key, value in TRANSLATIONS[lang].items():
                # Find all placeholders
                placeholders = re.findall(r'\{(\w+)\}', value)
                
                # Check that placeholders are reasonable
                for placeholder in placeholders:
                    assert placeholder.isalnum() or '_' in placeholder, \
                        f"Invalid placeholder '{placeholder}' in {lang}.{key}"
                    assert len(placeholder) > 0, \
                        f"Empty placeholder in {lang}.{key}"
    
    def test_translation_consistency_checks(self):
        """Test translation consistency between languages."""
        # Check that both languages have the same number of placeholders
        for key in TRANSLATIONS["en"]:
            if key in TRANSLATIONS["es"]:
                en_value = TRANSLATIONS["en"][key]
                es_value = TRANSLATIONS["es"][key]
                
                import re
                en_placeholders = re.findall(r'\{(\w+)\}', en_value)
                es_placeholders = re.findall(r'\{(\w+)\}', es_value)
                
                assert len(en_placeholders) == len(es_placeholders), \
                    f"Placeholder count mismatch in '{key}': EN={len(en_placeholders)}, ES={len(es_placeholders)}"
    
    def test_translation_length_consistency(self):
        """Test that translations have reasonable lengths."""
        for lang in ["en", "es"]:
            for key, value in TRANSLATIONS[lang].items():
                # Check minimum length (not just whitespace)
                assert len(value.strip()) >= 1, f"{lang}.{key} is too short"
                
                # Check maximum length (not unreasonably long)
                assert len(value) <= 200, f"{lang}.{key} is too long: {len(value)} chars"
    
    def test_translation_character_encoding(self):
        """Test that translations handle character encoding properly."""
        for lang in ["en", "es"]:
            for key, value in TRANSLATIONS[lang].items():
                try:
                    # Try to encode/decode to check for encoding issues
                    encoded = value.encode('utf-8')
                    decoded = encoded.decode('utf-8')
                    assert decoded == value, f"Encoding issue in {lang}.{key}"
                except UnicodeError:
                    pytest.fail(f"Unicode error in {lang}.{key}: {value}")
    
    def test_translation_placeholder_usage(self):
        """Test that placeholders are used correctly."""
        import re
        
        for lang in ["en", "es"]:
            for key, value in TRANSLATIONS[lang].items():
                # Check for malformed placeholders
                malformed = re.findall(r'\{[^}]*[^a-zA-Z0-9_][^}]*\}', value)
                assert not malformed, f"Malformed placeholders in {lang}.{key}: {malformed}"
                
                # Check for unmatched braces
                open_braces = value.count('{')
                close_braces = value.count('}')
                assert open_braces == close_braces, \
                    f"Unmatched braces in {lang}.{key}: {open_braces} open, {close_braces} close"
