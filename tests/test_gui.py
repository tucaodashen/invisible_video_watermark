"""
Tests for GUI preparation/startup modules (PyAV migration).
Tests the non-UI portions: dependency checks, compatibility functions.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GUI.PrepareRequirements import (
    check_pyav_installed,
    is_pyav_available,
    is_ffmpeg_exist,
    check_ffmpeg_installed,
    FFmpegPrepare,
)


class TestPrepareRequirements:

    def test_check_pyav_installed_returns_true(self):
        """PyAV (av) is installed in our test environment, should return True."""
        assert check_pyav_installed() is True

    def test_is_pyav_available_returns_true(self):
        """Alias function should also return True."""
        assert is_pyav_available() is True

    def test_is_ffmpeg_exist_returns_true_pyav_available(self):
        """Backward-compat: should return True when PyAV is installed."""
        assert is_ffmpeg_exist() is True

    def test_check_ffmpeg_installed_returns_true_pyav_available(self):
        """Backward-compat: should return True when PyAV is installed."""
        assert check_ffmpeg_installed() is True

    def test_check_pyav_installed_mocked(self, monkeypatch):
        """When av is not importable, should return False."""
        import builtins
        original_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == 'av':
                raise ImportError("No module named 'av'")
            return original_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, '__import__', mock_import)
        assert check_pyav_installed() is False

    def test_ffmpeg_prepare_class_exists(self):
        """FFmpegPrepare class exists for backward compatibility."""
        instance = FFmpegPrepare()
        assert instance is not None

    def test_ffmpeg_prepare_run_does_not_crash(self):
        """FFmpegPrepare.run() should not crash (it's a no-op now)."""
        instance = FFmpegPrepare()
        instance.run()

    def test_ffmpeg_prepare_success_signal(self):
        """FFmpegPrepare.success signal can be connected and emitted."""
        instance = FFmpegPrepare()
        captured = []

        def handler(value):
            captured.append(value)

        instance.success.connect(handler)
        instance.run()
        assert len(captured) == 1
        assert captured[0] is False  # run() emits False (deprecated/no-op)
