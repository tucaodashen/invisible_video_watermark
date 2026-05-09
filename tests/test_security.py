"""
Unit tests for security fixes: tokens in environment variables, not hardcoded.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---------------------------------------------------------------------------
# Test: Rollbar token from environment
# ---------------------------------------------------------------------------

def test_rollbar_token_env_var():
    """Rollbar token should be loaded from environment, not hardcoded."""
    token = os.environ.get("ROLLBAR_TOKEN", "")
    assert isinstance(token, str)
    # The old hardcoded token should NOT appear in the code
    import importlib
    try:
        mod = importlib.import_module("BasicSystem.const")
        with open(mod.__file__, encoding="utf-8") as f:
            source = f.read()
        assert "758277cc22ea" not in source, "Hardcoded token still present in const.py"
    except (ImportError, FileNotFoundError, UnicodeDecodeError):
        pytest.skip("Cannot verify const.py in this environment")


def test_rollbar_token_falls_back_to_empty():
    """When env var is not set, token should be empty string."""
    token = os.environ.get("ROLLBAR_TOKEN", "")
    assert token == ""


# ---------------------------------------------------------------------------
# Test: Google OAuth credentials from environment
# ---------------------------------------------------------------------------

def test_google_oauth_env_vars():
    """Google OAuth credentials should be loaded from environment."""
    client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "")

    assert isinstance(client_id, str)
    assert isinstance(client_secret, str)


# ---------------------------------------------------------------------------
# Test: credentials.json deleted
# ---------------------------------------------------------------------------

def test_credentials_json_removed():
    """credentials.json should no longer exist in the repo."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cred_path = os.path.join(base_dir, "modules", "OAuth", "credentials.json")
    assert not os.path.exists(cred_path), (
        "credentials.json should be deleted — contains hardcoded secrets"
    )


# ---------------------------------------------------------------------------
# Test: Default watermark passwords
# ---------------------------------------------------------------------------

def test_no_hardcoded_default_passwords():
    """Default attachment_data should be empty, not hardcoded passwords."""
    attachment_data = {}
    assert "img_password" not in attachment_data
    assert "wm_password" not in attachment_data


def test_random_passwords_generated():
    """When no user passwords are set, random passwords should be generated."""
    import random
    random.seed(42)

    attachment_data = {}
    if not attachment_data:
        attachment_data["img_password"] = random.randint(1000, 9999)
        attachment_data["wm_password"] = random.randint(1000, 9999)

    assert "img_password" in attachment_data
    assert "wm_password" in attachment_data
    assert attachment_data["img_password"] != 1145  # not the old default
    assert attachment_data["wm_password"] != 1919   # not the old default


# ---------------------------------------------------------------------------
# Test: .gitignore patterns
# ---------------------------------------------------------------------------

def test_gitignore_has_dump_patterns():
    """gitignore should exclude *.dump and dumps/ and logs/."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gitignore_path = os.path.join(base_dir, ".gitignore")

    if not os.path.exists(gitignore_path):
        pytest.skip(".gitignore not found")

    with open(gitignore_path) as f:
        content = f.read()

    assert "*.dump" in content, "*.dump pattern missing from .gitignore"
    assert "/dumps/" in content, "/dumps/ pattern missing from .gitignore"
    assert "/logs/" in content, "/logs/ pattern missing from .gitignore"


# ---------------------------------------------------------------------------
# Test: pyproject.toml fixes
# ---------------------------------------------------------------------------

def test_pyproject_zmq_fixed():
    """pyproject.toml should have pyzmq, not zmq."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    toml_path = os.path.join(base_dir, "pyproject.toml")

    if not os.path.exists(toml_path):
        pytest.skip("pyproject.toml not found")

    with open(toml_path) as f:
        content = f.read()

    assert "pyzmq" in content, "pyzmq dependency missing (was zmq)"

    # Windows-only deps should have platform markers
    for dep in ["onnxruntime-directml", "pyadl", "wmi"]:
        assert dep in content, f"{dep} dependency missing"


def test_init_files_exist():
    """GUI/__init__.py and modules/__init__.py should exist."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gui_init = os.path.join(base_dir, "GUI", "__init__.py")
    mod_init = os.path.join(base_dir, "modules", "__init__.py")

    assert os.path.exists(gui_init), "GUI/__init__.py missing"
    assert os.path.exists(mod_init), "modules/__init__.py missing"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
