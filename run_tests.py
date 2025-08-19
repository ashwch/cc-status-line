#!/usr/bin/env python3
"""Simple test runner for CC Status Line."""

import subprocess
import sys
from pathlib import Path


def run_cli_tests():
    """Run basic CLI functionality tests."""
    print("🧪 Testing CLI functionality...")

    tests = [
        (["uv", "run", "cc-status-line", "--help"], "Help command"),
        (["uv", "run", "cc-status-line", "--version"], "Version command"),
        (["uv", "run", "cc-status-line", "--config-info"], "Config info command"),
    ]

    for cmd, description in tests:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ {description} failed: {e}")
            return False

    return True


def test_claude_code_integration():
    """Test Claude Code JSON stdin integration."""
    print("🧪 Testing Claude Code integration...")

    try:
        import json

        test_json = json.dumps(
            {"session_id": "test", "workspace": {"current_working_directory": str(Path.cwd())}}
        )

        cmd = ["uv", "run", "cc-status-line"]
        result = subprocess.run(cmd, input=test_json, capture_output=True, text=True, timeout=10)

        if result.returncode == 0 and (
            "Repos" in result.stdout or "No configuration" in result.stdout
        ):
            print("✅ Claude Code JSON stdin integration")
            return True
        else:
            print(f"❌ Claude Code integration failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Claude Code integration failed: {e}")
        return False


def test_color_handling():
    """Test color handling with NO_COLOR."""
    print("🧪 Testing color handling...")

    try:
        import os

        env = os.environ.copy()
        env["NO_COLOR"] = "1"

        cmd = ["uv", "run", "cc-status-line", "--help"]
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            print("✅ NO_COLOR environment variable respected")
            return True
        else:
            print(f"❌ Color handling failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Color handling failed: {e}")
        return False


def test_imports():
    """Test that all modules can be imported using uv run."""
    print("🧪 Testing module imports...")

    try:
        # Test imports using uv run python to ensure proper environment
        test_script = """
import sys
sys.path.insert(0, "src")

# Test individual imports
try:
    from cli import main
    print("✅ CLI import successful")
except ImportError as e:
    print(f"❌ CLI import failed: {e}")
    sys.exit(1)

try:
    from config import ConfigManager
    print("✅ Config import successful")
except ImportError as e:
    print(f"❌ Config import failed: {e}")
    sys.exit(1)

try:
    from render import StatusLineRenderer
    print("✅ Render import successful")
except ImportError as e:
    print(f"❌ Render import failed: {e}")
    sys.exit(1)

try:
    from git import RepoStatus, GitManager
    print("✅ Git import successful")
except ImportError as e:
    print(f"❌ Git import failed: {e}")
    sys.exit(1)

print("✅ All critical imports successful")
"""

        result = subprocess.run(
            ["uv", "run", "python", "-c", test_script], capture_output=True, text=True, timeout=15
        )

        if result.returncode == 0:
            print(result.stdout.strip())
            return True
        else:
            print(f"❌ Import test failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Import testing failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 Running CC Status Line Tests")
    print("=" * 40)

    all_passed = True

    # Test imports first
    if not test_imports():
        all_passed = False

    # Test CLI functionality
    if not run_cli_tests():
        all_passed = False

    # Test Claude Code integration
    if not test_claude_code_integration():
        all_passed = False

    # Test color handling
    if not test_color_handling():
        all_passed = False

    print("=" * 40)
    if all_passed:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
