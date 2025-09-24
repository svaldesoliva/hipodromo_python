# Hipodromo 🐎

A fun terminal horse racing betting game. Place bets, watch horses race, and see if you can win some money. Simple, colorful, and addictive.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## Features

- 🏁 **Horse Racing**: Watch animated horses race with different odds
- 💰 **Betting**: Place bets and win (or lose) money
- 🌍 **Two Languages**: English and Spanish
- ⚡ **Fast Mode**: Skip the slow animations
- 🎲 **Seeded Races**: Use the same seed to get the same race
- 🎨 **Colorful Terminal**: Horse emojis and colored text
- ⚙️ **Configurable**: Change number of horses, language, etc.
- 📱 **CLI Options**: Command-line flags for quick setup

## Quick Start

### Installation

**Recommended (via pipx):**
```bash
pipx install git+https://github.com/svaldesoliva/hipodromo_python
```

**From source:**
```bash
git clone https://github.com/svaldesoliva/hipodromo_python.git
cd hipodromo_python
./scripts/install.sh
```

**Using pip:**
```bash
python3 -m pip install --user git+https://github.com/svaldesoliva/hipodromo_python
```

### Play Now!

```bash
hipodromo
```

## How to Play

1. Run `hipodromo` in your terminal
2. Pick a horse (1-5 by default)
3. Bet some money
4. Watch the race
5. Win or lose money

### Game Details

- **Starting Money**: $5,000
- **Odds**: Each horse has different odds (house keeps ~10%)
- **Min Payout**: 1.5x your bet

## Configuration

Your settings are stored in `~/.config/hipodromo/config.json`:

```json
{
  "balance": 7500,
  "lang": "en",
  "fast": false,
  "horses": 5,
  "seed": null
}
```

### CLI Options

```bash
# Enable fast mode for this session
hipodromo --fast

# Disable fast mode (overrides config)
hipodromo --no-fast

# Set number of horses and seed
hipodromo --horses 7 --seed 12345

# Show config file location
hipodromo --config

# Edit config file with your editor
hipodromo -e
```

## Development

### Setup Development Environment

```bash
git clone https://github.com/svaldesoliva/hipodromo_python.git
cd hipodromo_python
./scripts/install.sh dev
```

Or with pipx:
```bash
pipx install --force --editable .
```

### Project Structure

```
hipodromo_python/
├── Hipodromo.py      # Main game logic and CLI
├── game.py           # Race animation and odds calculation
├── config.py         # Configuration management
├── i18n.py           # Internationalization
├── utils.py          # Utility functions
├── scripts/          # Installation scripts
└── termcolor/        # Bundled terminal colors
```

### Key Components

- **Race Engine**: Weighted random system for realistic horse performance
- **Odds Calculator**: Fair odds with house edge for balanced gameplay
- **Animation System**: Terminal-based race visualization
- **Config Management**: JSON-based settings with legacy migration
- **i18n System**: Simple but effective translation framework

## How It Works

### Odds System

- Each horse gets a random weight (0.6-1.4)
- Weights determine win probability
- House keeps ~10% edge
- Min payout is 1.5x

### Race Animation

- Terminal animation with horse emojis
- Horses move based on their weights
- Fast mode skips the animation
- Shows winner at the end

### Languages

- English and Spanish
- Switch languages anytime
- Saves your preference

## Requirements

- Python 3.8+
- Terminal with Unicode support
- Optional: `fzf` for enhanced menu selection

## Contributing

Feel free to contribute:

1. Report bugs
2. Suggest features
3. Add translations
4. Improve the code
5. Submit pull requests

## License

MIT License - see [LICENSE](LICENSE) file for details.









