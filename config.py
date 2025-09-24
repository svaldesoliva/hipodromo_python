import os
import json

# Config directory and files
CONFIG_DIR = os.path.expanduser("~/.config/hipodromo")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# Legacy files for migration
OLD_BALANCE_FILE = os.path.expanduser("~/.hipodromo_balance")
OLD_LANG_FILE = os.path.expanduser("~/.hipodromo_lang")
BALANCE_FILE = os.path.join(CONFIG_DIR, "balance")
LANG_FILE = os.path.join(CONFIG_DIR, "lang")


def _read_legacy_value(path, coerce=None):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                value = f.read().strip()
            return coerce(value) if coerce else value
    except Exception:
        return None
    return None


def _load_config_from_disk():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
    except Exception:
        pass
    return {}


def _write_config_to_disk(config):
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _ensure_and_migrate_config():
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
    except Exception:
        pass

    config = _load_config_from_disk()

    if "balance" not in config:
        legacy_balance = None
        legacy_balance = _read_legacy_value(BALANCE_FILE, coerce=int) or legacy_balance
        legacy_balance = _read_legacy_value(OLD_BALANCE_FILE, coerce=int) or legacy_balance
        config["balance"] = legacy_balance if isinstance(legacy_balance, int) and legacy_balance >= 0 else 5000

    if "lang" not in config:
        legacy_lang = None
        legacy_lang = _read_legacy_value(LANG_FILE) or legacy_lang
        legacy_lang = _read_legacy_value(OLD_LANG_FILE) or legacy_lang
        config["lang"] = legacy_lang if legacy_lang in ("en", "es") else None

    _write_config_to_disk(config)
    return config


CONFIG = _ensure_and_migrate_config()


def get_lang(default=None):
    return CONFIG.get("lang", default)


def set_lang(lang):
    CONFIG["lang"] = lang
    _write_config_to_disk(CONFIG)


def get_balance(default=5000):
    try:
        value = int(CONFIG.get("balance", default))
        return value if value >= 0 else default
    except Exception:
        return default


def set_balance(value):
    try:
        CONFIG["balance"] = int(value)
        _write_config_to_disk(CONFIG)
    except Exception:
        pass
