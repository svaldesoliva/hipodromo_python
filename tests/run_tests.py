#!/usr/bin/env python3
"""
Test runner for Hipodromo debugging tests.
This script provides various ways to run the test suite for debugging purposes.
"""
import sys
import os
import argparse
import subprocess
from pathlib import Path


def run_pytest(test_path=None, verbose=False, debug=False, specific_test=None):
    """Run pytest with appropriate options."""
    cmd = ["python", "-m", "pytest"]
    
    if verbose:
        cmd.append("-v")
    
    if debug:
        cmd.extend(["-s", "--tb=long"])
    
    if specific_test:
        cmd.extend(["-k", specific_test])
    
    if test_path:
        cmd.append(test_path)
    else:
        cmd.append("tests/")
    
    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=Path(__file__).parent.parent)


def run_specific_module(module_name, verbose=False):
    """Run tests for a specific module."""
    test_file = f"tests/test_{module_name}.py"
    if not os.path.exists(test_file):
        print(f"Test file {test_file} not found!")
        return 1
    
    return run_pytest(test_file, verbose=verbose)


def run_debugging_tests(verbose=False):
    """Run only debugging-specific tests."""
    return run_pytest("tests/test_debugging.py", verbose=verbose, debug=True)


def run_integration_tests(verbose=False):
    """Run only integration tests."""
    return run_pytest("tests/test_integration.py", verbose=verbose)


def run_all_tests(verbose=False, debug=False):
    """Run all tests."""
    return run_pytest(verbose=verbose, debug=debug)


def list_available_tests():
    """List all available test files."""
    test_dir = Path(__file__).parent
    test_files = list(test_dir.glob("test_*.py"))
    
    print("Available test files:")
    for test_file in sorted(test_files):
        print(f"  - {test_file.stem}")
    
    print("\nTest categories:")
    print("  - test_game: Race engine and odds calculation")
    print("  - test_config: Configuration management")
    print("  - test_i18n: Translation system")
    print("  - test_utils: Utility functions")
    print("  - test_integration: Component integration")
    print("  - test_debugging: Debugging-specific tests")


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run Hipodromo debugging tests")
    parser.add_argument("--module", "-m", help="Run tests for specific module (game, config, i18n, utils, integration, debugging)")
    parser.add_argument("--debug", "-d", action="store_true", help="Run in debug mode (show output, long tracebacks)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--list", "-l", action="store_true", help="List available tests")
    parser.add_argument("--specific", "-k", help="Run specific test by name pattern")
    parser.add_argument("--integration", action="store_true", help="Run only integration tests")
    parser.add_argument("--debugging", action="store_true", help="Run only debugging tests")
    
    args = parser.parse_args()
    
    if args.list:
        list_available_tests()
        return 0
    
    # Change to project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Add project root to Python path
    sys.path.insert(0, str(project_root))
    
    if args.module:
        return run_specific_module(args.module, verbose=args.verbose)
    elif args.integration:
        return run_integration_tests(verbose=args.verbose)
    elif args.debugging:
        return run_debugging_tests(verbose=args.verbose)
    else:
        return run_all_tests(verbose=args.verbose, debug=args.debug)


if __name__ == "__main__":
    sys.exit(main())
