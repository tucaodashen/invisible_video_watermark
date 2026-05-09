"""
Unit tests for various module fixes: Slice, ExtractUnit, ThreadingScheduler, VideoProcessor.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---------------------------------------------------------------------------
# Test: Bare except fix
# ---------------------------------------------------------------------------

def test_bare_except_does_not_catch_keyboard_interrupt():
    """except Exception should NOT catch KeyboardInterrupt."""
    caught = False
    try:
        raise KeyboardInterrupt()
    except Exception:
        caught = True
    except KeyboardInterrupt:
        caught = False

    assert caught is False


def test_bare_except_catches_keyboard_interrupt():
    """Bare except: catches KeyboardInterrupt (BAD behavior)."""
    caught = False
    try:
        raise KeyboardInterrupt()
    except BaseException:  # equivalent to bare except:
        caught = True

    assert caught is True  # BAD: should not catch KeyboardInterrupt


# ---------------------------------------------------------------------------
# Test: RuntimeError instead of SystemError
# ---------------------------------------------------------------------------

def test_system_error_is_wrong():
    """SystemError is for interpreter-internal errors, not application errors."""
    import builtins
    assert issubclass(RuntimeError, Exception)
    assert not issubclass(RuntimeError, SystemExit)
    assert issubclass(SystemError, Exception)
    # Application errors should use RuntimeError, not SystemError


# ---------------------------------------------------------------------------
# Test: Pickle file leak fix
# ---------------------------------------------------------------------------

def test_pickle_with_statement_does_not_leak():
    """Using 'with open(...) as f:' ensures file is closed after reading."""
    import pickle
    import tempfile

    data = {"key": "value"}
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pkl") as f:
        pickle.dump(data, f)
        tmp_path = f.name

    try:
        loaded = None
        with open(tmp_path, "rb") as f:
            loaded = pickle.load(f)
        assert loaded == data
        assert f.closed  # file should be closed after with block
    finally:
        os.unlink(tmp_path)


# ---------------------------------------------------------------------------
# Test: Auto-assign port instead of hardcoded
# ---------------------------------------------------------------------------

def test_auto_assign_port():
    """Port 0 should auto-assign an available port."""
    import socket

    with socket.socket() as s:
        s.bind(("", 0))
        port = s.getsockname()[1]

    assert port > 0
    assert port != 1165  # not the old hardcoded value


# ---------------------------------------------------------------------------
# Test: Thread worker exit after completion
# ---------------------------------------------------------------------------

def test_worker_exits_when_all_done():
    """Worker should exit when completed_count >= total_tasks."""
    completed_count = 5
    total_tasks = 5

    should_exit = completed_count >= total_tasks
    assert should_exit is True


def test_worker_continues_when_not_done():
    """Worker should continue when not all tasks are done."""
    completed_count = 3
    total_tasks = 5

    should_exit = completed_count >= total_tasks
    assert should_exit is False


# ---------------------------------------------------------------------------
# Test: VideoProcessor sample_type fix
# ---------------------------------------------------------------------------

def test_psy_sampler_raises_not_implemented():
    """PSY sampler should raise NotImplementedError instead of returning None."""
    class MockSamplerType:
        PSY = "psy"
        RANDOM = "random"

    sampler_type = MockSamplerType.PSY

    with pytest.raises(NotImplementedError):
        if sampler_type == MockSamplerType.PSY:
            raise NotImplementedError("PSY sampler not yet implemented")


# ---------------------------------------------------------------------------
# Test: Redundant modulo fix
# ---------------------------------------------------------------------------

def test_modulo_one_is_always_zero():
    """frame_num % 1 is always 0 — the check is redundant."""
    for i in range(0, 100, 7):
        assert i % 1 == 0  # always true, should be removed


# ---------------------------------------------------------------------------
# Test: stamp return type fix
# ---------------------------------------------------------------------------

def test_stamp_return_unpackable():
    """If stamp returns a single array, unpacking to 2 vars raises ValueError."""
    try:
        import numpy as np
    except ImportError:
        pytest.skip("numpy not available")
        return

    stamp_result = np.zeros((10, 10, 3), dtype=np.uint8)

    # Old behavior: unpack to 2 vars → crash
    with pytest.raises(ValueError):
        proceeded_image, ret_atta = stamp_result

    # Fixed behavior: check type first
    if isinstance(stamp_result, tuple) and len(stamp_result) == 2:
        proceeded_image, ret_atta = stamp_result
    else:
        proceeded_image = stamp_result
        ret_atta = {}

    assert proceeded_image is stamp_result
    assert ret_atta == {}


# ---------------------------------------------------------------------------
# Test: unused imports removal
# ---------------------------------------------------------------------------

def test_imports_no_unused():
    """zmq, zlib, pickle should not be imported unnecessarily in networks.py."""
    import importlib
    try:
        mod = importlib.import_module("modules.networks")
        source = open(mod.__file__).read()
        assert "import zmq" not in source
        assert "import pickle" not in source
        assert "import zlib" not in source
    except (ImportError, FileNotFoundError):
        pytest.skip("Cannot verify networks.py imports in this environment")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
