# Hipodromo Debugging Guide

This guide provides comprehensive information for debugging the Hipodromo horse racing game.

## Quick Start

### Run Basic Tests (No Dependencies)
```bash
python3 tests/simple_test_runner.py
```

### Run Full Test Suite (Requires pytest)
```bash
# Install pytest first
pip install pytest

# Run all tests
python tests/run_tests.py

# Run specific test categories
python tests/run_tests.py --module game
python tests/run_tests.py --debugging
python tests/run_tests.py --integration
```

## Test Structure

The test suite is organized into several categories:

### 1. Unit Tests
- **`test_game.py`** - Race engine, odds calculation, animation
- **`test_config.py`** - Configuration management and persistence
- **`test_i18n.py`** - Translation system and internationalization
- **`test_utils.py`** - Utility functions (input, screen clearing, fzf)

### 2. Integration Tests
- **`test_integration.py`** - Component interactions and game flow

### 3. Debugging Tests
- **`test_debugging.py`** - Common issues, edge cases, performance

## Common Debugging Scenarios

### Race Engine Issues

**Problem**: Races are not deterministic
```bash
python tests/run_tests.py --specific "test_race_determinism"
```

**Problem**: Odds calculation seems wrong
```bash
python tests/run_tests.py --specific "test_odds_calculation"
```

**Problem**: Race animation hangs or doesn't complete
```bash
python tests/run_tests.py --specific "test_race_completion"
```

### Configuration Issues

**Problem**: Config file corruption
```bash
python tests/run_tests.py --specific "test_config_corruption"
```

**Problem**: Settings not persisting
```bash
python tests/run_tests.py --specific "test_config_persistence"
```

**Problem**: Migration from old config format
```bash
python tests/run_tests.py --specific "test_migration"
```

### Input Handling Issues

**Problem**: Invalid input causes crashes
```bash
python tests/run_tests.py --specific "test_input_entero"
```

**Problem**: fzf integration not working
```bash
python tests/run_tests.py --specific "test_fzf"
```

**Problem**: Boundary value handling
```bash
python tests/run_tests.py --specific "test_boundary"
```

### Translation Issues

**Problem**: Missing translation keys
```bash
python tests/run_tests.py --specific "test_missing_keys"
```

**Problem**: Placeholder substitution errors
```bash
python tests/run_tests.py --specific "test_placeholder"
```

**Problem**: Unicode character issues
```bash
python tests/run_tests.py --specific "test_unicode"
```

## Debugging Tools

### Test Runners

1. **Simple Test Runner** (`simple_test_runner.py`)
   - No dependencies required
   - Basic functionality verification
   - Quick smoke tests

2. **Full Test Runner** (`run_tests.py`)
   - Requires pytest
   - Comprehensive test suite
   - Advanced debugging features

### Test Categories

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Debugging Tests**: Test edge cases and common issues
- **Performance Tests**: Test under load and memory usage

## Common Issues and Solutions

### Issue: Race Results Not Reproducible

**Symptoms**: Same seed produces different race outcomes

**Debug Steps**:
1. Run determinism tests: `python tests/run_tests.py --specific "test_race_determinism"`
2. Check if random seed is being set correctly
3. Verify no external random calls are interfering

**Solution**: Ensure all random operations use the same seeded random number generator

### Issue: Configuration Not Saving

**Symptoms**: Settings reset after restart

**Debug Steps**:
1. Run config tests: `python tests/run_tests.py --module config`
2. Check file permissions in config directory
3. Verify JSON serialization is working

**Solution**: Check write permissions and JSON format validity

### Issue: Input Validation Failures

**Symptoms**: Game crashes on invalid input

**Debug Steps**:
1. Run input tests: `python tests/run_tests.py --specific "test_input_entero"`
2. Test with various invalid inputs
3. Check error handling in input functions

**Solution**: Add proper input validation and error handling

### Issue: Translation Errors

**Symptoms**: Missing text or placeholder errors

**Debug Steps**:
1. Run i18n tests: `python tests/run_tests.py --module i18n`
2. Check for missing translation keys
3. Verify placeholder syntax

**Solution**: Add missing translations or fix placeholder syntax

### Issue: Performance Problems

**Symptoms**: Game runs slowly or uses too much memory

**Debug Steps**:
1. Run performance tests: `python tests/run_tests.py --specific "test_performance"`
2. Profile memory usage
3. Check for infinite loops

**Solution**: Optimize algorithms and fix memory leaks

## Test Development

### Adding New Tests

1. **Choose appropriate test file** based on component
2. **Follow naming conventions**: `test_*` for test functions
3. **Use fixtures** from `conftest.py` for setup
4. **Mock external dependencies** to avoid side effects
5. **Test both success and failure cases**

### Test Best Practices

- **Use descriptive test names** that explain what is being tested
- **Test edge cases** and boundary conditions
- **Use deterministic seeds** for reproducible tests
- **Mock external dependencies** (file I/O, user input, etc.)
- **Keep tests fast** and isolated
- **Document complex test scenarios**

### Debugging Test Failures

1. **Run with verbose output**: `--verbose` or `-v`
2. **Run in debug mode**: `--debug` for full tracebacks
3. **Run specific tests**: `--specific "test_name"`
4. **Check test fixtures** and setup
5. **Verify mock configurations**

## Performance Monitoring

### Memory Usage
```bash
python tests/run_tests.py --specific "test_memory_usage"
```

### Load Testing
```bash
python tests/run_tests.py --specific "test_performance"
```

### Race Generation Speed
```bash
python tests/run_tests.py --specific "test_race_performance"
```

## Integration Testing

### Game Flow Testing
```bash
python tests/run_tests.py --integration
```

### CLI Testing
```bash
python tests/run_tests.py --specific "test_cli"
```

### State Management Testing
```bash
python tests/run_tests.py --specific "test_state"
```

## Continuous Integration

For automated testing, use:

```bash
# Run all tests
python tests/run_tests.py

# Run with coverage (if available)
python tests/run_tests.py --coverage

# Run specific test categories
python tests/run_tests.py --module game --module config
```

## Troubleshooting

### Common Test Failures

1. **Import Errors**: Ensure you're running from project root
2. **Permission Errors**: Check file system permissions
3. **Mock Failures**: Verify mock setup matches function signatures
4. **Race Conditions**: Use deterministic seeds and proper synchronization

### Environment Issues

1. **Python Version**: Ensure Python 3.8+ is being used
2. **Dependencies**: Install required packages (pytest, etc.)
3. **Path Issues**: Check PYTHONPATH and working directory
4. **File Permissions**: Ensure write access to temp directories

## Getting Help

1. **Check test output** for specific error messages
2. **Run with debug flags** for detailed information
3. **Review test documentation** in individual test files
4. **Check project issues** for known problems
5. **Add new tests** for newly discovered issues

## Contributing

When contributing to the test suite:

1. **Add tests for new features**
2. **Update tests when fixing bugs**
3. **Ensure tests are deterministic**
4. **Document complex test scenarios**
5. **Keep tests fast and isolated**
6. **Follow existing patterns and conventions**
