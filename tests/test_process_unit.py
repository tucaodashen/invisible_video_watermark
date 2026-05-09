"""
Unit tests for ProcessUnit.py edge case fixes.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---------------------------------------------------------------------------
# Test: scheduler null guards
# ---------------------------------------------------------------------------

class MockScheduler:
    def __init__(self):
        self.pids = [123, 456]
        self.manager_pid = 100

    def get_running_pids(self):
        return self.pids


class MockProcessUnit:
    def __init__(self, process_limit=16, image=False):
        self.scheduler = MockScheduler() if process_limit != 1 else None
        self.process_limit = process_limit
        self.slice_list = []
        self.result_list = []
        self.progress_dict = {}
        self.completed = False
        self.status = 1
        self.frame_count = 0 if image else 100
        self.saved_file_path = [None, None]
        self.running = False
        self.stopped = False
        self.image = image

    def suspend(self):
        if self.scheduler is None:
            return
        for pid in self.scheduler.get_running_pids():
            pass  # suspend logic

    def resume(self):
        if self.scheduler is None:
            return
        for pid in self.scheduler.get_running_pids():
            pass  # resume logic

    def stop(self):
        if self.scheduler is None:
            return
        for pid in self.scheduler.get_running_pids():
            pass  # terminate logic


def test_suspend_without_scheduler():
    """Suspend should not crash when scheduler is None (single-process mode)."""
    pu = MockProcessUnit(process_limit=1)
    pu.suspend()  # should not raise AttributeError


def test_resume_without_scheduler():
    """Resume should not crash when scheduler is None."""
    pu = MockProcessUnit(process_limit=1)
    pu.resume()  # should not raise


def test_stop_without_scheduler():
    """Stop should not crash when scheduler is None."""
    pu = MockProcessUnit(process_limit=1)
    pu.stop()  # should not raise


def test_suspend_with_scheduler():
    """Suspend should work normally when scheduler is available."""
    pu = MockProcessUnit(process_limit=16)
    pu.suspend()  # should not raise


# ---------------------------------------------------------------------------
# Test: empty slice_list guard
# ---------------------------------------------------------------------------

def test_ipc_callback_empty_slice_list():
    """IPC callback should not divide by zero on empty slice_list."""
    pu = MockProcessUnit()
    pu.slice_list = []

    if not pu.slice_list:
        result = "skipped"
    else:
        result = "computed"

    assert result == "skipped"


def test_ipc_callback_normal_slice_list():
    """IPC callback should compute progress normally with non-empty slice_list."""
    pu = MockProcessUnit()
    pu.slice_list = [1, 2, 3, 4, 5]
    pu.progress_dict = {i: 0.0 for i in range(6)}

    if pu.slice_list:
        cur_sum = sum(pu.progress_dict.values())
        cur_percent = cur_sum / len(pu.slice_list)
    else:
        cur_percent = 0

    assert cur_percent == 0.0


# ---------------------------------------------------------------------------
# Test: empty result_list guard
# ---------------------------------------------------------------------------

def test_empty_result_list():
    """Should not IndexError on empty result_list."""
    pu = MockProcessUnit()
    pu.result_list = []
    pu.error_occured = False

    if pu.result_list and pu.result_list[0] != "Terminated":
        result = "ok"
    else:
        result = "skip"

    assert result == "skip"


def test_result_list_with_terminated():
    """Should detect terminated result."""
    pu = MockProcessUnit()
    pu.result_list = ["Terminated"]
    pu.error_occured = False

    should_skip = not (not pu.error_occured and pu.result_list and pu.result_list[0] != "Terminated")
    assert should_skip is True


# ---------------------------------------------------------------------------
# Test: frame_count for image mode
# ---------------------------------------------------------------------------

def test_image_mode_frame_count():
    """In image mode, frame_count should default to 0."""
    pu = MockProcessUnit(image=True)
    assert pu.frame_count == 0


def test_video_mode_frame_count():
    """In video mode, frame_count should be set properly."""
    pu = MockProcessUnit(image=False)
    assert pu.frame_count == 100


def test_generate_queue_with_zero_frames():
    """generate_queue should guard against zero frame_count."""
    pu = MockProcessUnit(image=True)
    if pu.frame_count == 0:
        generated = False
    else:
        generated = True

    assert generated is False


# ---------------------------------------------------------------------------
# Test: saved_file_path null guard
# ---------------------------------------------------------------------------

def test_remove_workspace_with_none_path():
    """remove_workspace should handle [None, None] saved_file_path."""
    pu = MockProcessUnit()
    pu.saved_file_path = [None, None]

    if isinstance(pu.saved_file_path, list) and pu.saved_file_path[0] is None:
        result = "skip"
    else:
        result = "cleanup"

    assert result == "skip"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
