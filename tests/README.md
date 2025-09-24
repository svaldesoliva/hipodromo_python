# Hipodromo Testing Suite

This directory contains comprehensive tests for debugging the Hipodromo horse racing game. The tests are designed to help identify, reproduce, and fix common issues.

## Test Structure

### Test Files

- **`test_game.py`** - Tests for the race engine, odds calculation, and animation logic
- **`test_config.py`** - Tests for configuration management and persistence
- **`test_i18n.py`** - Tests for the internationalization system
- **`test_utils.py`** - Tests for utility functions (input validation, screen clearing, fzf)
- **`test_integration.py`** - Integration tests for component interactions
- **`test_debugging.py`** - Debugging-specific tests for common issues

### Test Categories

#### Unit Tests
- **Game Logic**: Race engine, odds calculation, weight generation
- **Configuration**: File I/O, migration, validation
- **Internationalization**: Translation system, placeholder handling
- **Utilities**: Input validation, screen clearing, fzf integration

#### Integration Tests
- **Game Flow**: Complete betting and racing flow
- **Menu System**: Language changes, fast mode toggle
- **CLI Integration**: Command-line argument handling
- **State Management**: Global state consistency

#### Debugging Tests
- **Race Determinism**: Reproducible race outcomes
- **Configuration Corruption**: Recovery from invalid config files
- **Input Edge Cases**: Malformed user input handling
- **Performance**: Load testing and memory usage
- **Error Propagation**: Graceful error handling

## Running Tests

### Prerequisites

For full test suite: Install pytest if not already installed:
```bash
pip install pytest
```

For basic tests: No additional dependencies required (uses only standard library).

### Basic Usage

#### Quick Test (No Dependencies)

```bash
# Run basic tests without pytest
python3 tests/simple_test_runner.py
```

This will run essential tests to verify the game is working correctly.

#### Full Test Suite (Requires pytest)

```bash
# Run all tests
python tests/run_tests.py

# Run with verbose output
python tests/run_tests.py --verbose

# Run in debug mode (shows output and long tracebacks)
python tests/run_tests.py --debug

# List available tests
python tests/run_tests.py --list
```

### Running Specific Test Categories

```bash
# Run only game logic tests
python tests/run_tests.py --module game

# Run only configuration tests
python tests/run_tests.py --module config

# Run only integration tests
python tests/run_tests.py --integration

# Run only debugging tests
python tests/run_tests.py --debugging
```

### Running Specific Tests

```bash
# Run tests matching a pattern
python tests/run_tests.py --specific "test_odds"

# Run tests for a specific function
python tests/run_tests.py --specific "test_compute_decimal_odds"
```

### Using pytest directly

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_game.py

# Run with verbose output
pytest tests/ -v

# Run with debugging output
pytest tests/ -s --tb=long

# Run specific test
pytest tests/test_game.py::TestComputeDecimalOdds::test_compute_odds_basic
```

## Test Features

### Fixtures and Mocks

The test suite includes comprehensive fixtures for:
- **Temporary directories** for config file testing
- **Mocked terminal functions** (cprint, clear_screen)
- **Mocked user input** for interactive testing
- **Mocked external dependencies** (fzf, subprocess)

### Edge Case Testing

Tests cover various edge cases:
- **Invalid input handling** (non-numeric, out of range, empty)
- **File corruption recovery** (invalid JSON, missing files)
- **Unicode handling** (accented characters, emojis)
- **Boundary conditions** (minimum/maximum values)
- **Error propagation** (graceful error handling)

### Performance Testing

Debugging tests include performance checks:
- **Race generation speed** (100+ races in reasonable time)
- **Config operation speed** (1000+ operations)
- **Memory usage** (object growth monitoring)
- **Load testing** (rapid successive operations)

## Common Debugging Scenarios

### Race Engine Issues

```bash
# Test race determinism
python tests/run_tests.py --specific "test_race_determinism"

# Test odds calculation
python tests/run_tests.py --specific "test_odds_calculation"

# Test race completion
python tests/run_tests.py --specific "test_race_completion"
```

### Configuration Issues

```bash
# Test config corruption recovery
python tests/run_tests.py --specific "test_config_corruption"

# Test migration issues
python tests/run_tests.py --specific "test_migration"

# Test concurrent access
python tests/run_tests.py --specific "test_concurrent"
```

### Input Handling Issues

```bash
# Test input validation
python tests/run_tests.py --specific "test_input_entero"

# Test fzf integration
python tests/run_tests.py --specific "test_fzf"

# Test boundary conditions
python tests/run_tests.py --specific "test_boundary"
```

### Translation Issues

```bash
# Test placeholder handling
python tests/run_tests.py --specific "test_placeholder"

# Test unicode handling
python tests/run_tests.py --specific "test_unicode"

# Test missing keys
python tests/run_tests.py --specific "test_missing_keys"
```

## Debugging Tips

### When Tests Fail

1. **Check the test output** for specific error messages
2. **Run with `--debug`** to see full tracebacks and output
3. **Run specific tests** to isolate the issue
4. **Check test fixtures** to ensure proper setup

### Common Issues

- **Import errors**: Make sure you're running from the project root
- **File permission errors**: Check write permissions for temp directories
- **Mock failures**: Verify mock setup matches actual function signatures
- **Race conditions**: Use deterministic seeds for reproducible tests

### Adding New Tests

When adding new tests:
1. **Follow naming conventions** (`test_*` for test functions)
2. **Use appropriate fixtures** from `conftest.py`
3. **Mock external dependencies** to avoid side effects
4. **Test both success and failure cases**
5. **Include edge cases and boundary conditions**

## Test Coverage

The test suite aims to cover:
- **All public functions** in each module
- **Error handling paths** and exception cases
- **Edge cases** and boundary conditions
- **Integration points** between components
- **Common debugging scenarios**

## Contributing

When contributing tests:
1. **Add tests for new features**
2. **Update tests when fixing bugs**
3. **Ensure tests are deterministic** (use seeds where appropriate)
4. **Document complex test scenarios**
5. **Keep tests fast and isolated**
