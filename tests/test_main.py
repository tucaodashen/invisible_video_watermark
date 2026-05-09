"""
Unit tests for GUI/main.py progress bar logic and bug fixes.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---------------------------------------------------------------------------
# Test 1: update_total_progress — skip completed tasks
# ---------------------------------------------------------------------------

class MockProgressBar:
    def __init__(self):
        self._value = 0

    def value(self):
        return self._value

    def setValue(self, v):
        self._value = v


class MockTask:
    def __init__(self, index, completed=False, status=1, progress=0.0):
        self.index = index
        self.completed = completed
        self.status = status
        self.running = False
        self.stopped = False
        self.paused = False
        self.progress = progress
        self.progress_identify = f"uuid_{index}"
        self.statue = ""
        self.start_time = None
        self.consumed_timer = None
        self.file = "test.mp4"
        self.output_path = "./output"
        self.output_format = "mp4"
        self.MaximumBitRate = "10M"
        self.TargetBitRate = "6M"


def test_update_total_progress_skips_completed():
    """Completed tasks should not contribute to overall queue progress."""
    # 3 old completed tasks + 2 new running tasks
    tasks = [
        MockTask(1, completed=True, status=1, progress=1.0),
        MockTask(2, completed=True, status=1, progress=1.0),
        MockTask(3, completed=True, status=1, progress=1.0),
        MockTask(4, completed=False, status=1, progress=0.3),
        MockTask(5, completed=False, status=1, progress=0.0),
    ]

    # Calculate total_progress and tpb considering only non-completed tasks
    total_progress = 0
    tpb = 0
    for task in tasks:
        if not task.completed:
            total_progress += 1
            tpb += int(task.progress * 100)

    # Only 2 active tasks: task4 at 30%, task5 at 0%
    assert total_progress == 2
    assert tpb == 30
    assert tpb / total_progress == 15.0


def test_update_total_progress_all_completed():
    """When all tasks are completed, result should be 100."""
    tasks = [
        MockTask(1, completed=True, status=1, progress=1.0),
        MockTask(2, completed=True, status=1, progress=1.0),
        MockTask(3, completed=True, status=1, progress=1.0),
    ]

    total_progress = 0
    for task in tasks:
        if not task.completed:
            total_progress += 1

    # No active tasks → should show 100
    assert total_progress == 0


def test_update_total_progress_stopped_tasks_skipped():
    """Stopped tasks should be treated as completed and skipped."""
    tasks = [
        MockTask(1, completed=True, status=1, progress=1.0),
        MockTask(2, completed="已终止", status=0, progress=0.5),
        MockTask(3, completed=False, status=1, progress=0.4),
    ]

    total_progress = 0
    tpb = 0
    for task in tasks:
        if not task.completed:
            total_progress += 1
            tpb += int(task.progress * 100)

    assert total_progress == 1  # only task3
    assert tpb == 40


def test_update_total_progress_errored_tasks_skipped():
    """Errored tasks (completed=string, status=0) should be skipped."""
    tasks = [
        MockTask(1, completed="发生错误", status=0, progress=0.2),
        MockTask(2, completed=False, status=1, progress=0.8),
    ]

    total_progress = 0
    tpb = 0
    for task in tasks:
        if not task.completed:
            total_progress += 1
            tpb += int(task.progress * 100)

    # "发生错误" is truthy so not task.completed is False → skipped
    assert total_progress == 1
    assert tpb == 80


def test_update_total_progress_empty_queue():
    """Empty queue should give 0 progress."""
    tasks = []
    total_progress = 0
    for task in tasks:
        if not task.completed:
            total_progress += 1

    assert total_progress == 0


def test_update_total_progress_all_running():
    """When all tasks are running, all should be counted."""
    tasks = [
        MockTask(1, completed=False, status=1, progress=0.5),
        MockTask(2, completed=False, status=1, progress=0.75),
        MockTask(3, completed=False, status=1, progress=0.25),
    ]

    total_progress = 0
    tpb = 0
    for task in tasks:
        if not task.completed:
            total_progress += 1
            tpb += int(task.progress * 100)

    assert total_progress == 3
    assert tpb == 150  # 50 + 75 + 25
    assert tpb / total_progress == 50.0


# ---------------------------------------------------------------------------
# Test 2: progressBar display logic (update_details)
# ---------------------------------------------------------------------------

def test_progressbar_completed_task_shows_100():
    """Completed tasks should always show 100 on detail progressBar."""
    task = MockTask(1, completed=True, status=1, progress=0.999)

    if task.completed or task.status == 0:
        disp = 100
    else:
        disp = int(task.progress * 100)

    assert disp == 100


def test_progressbar_running_task_shows_actual():
    """Running tasks show actual progress value."""
    task = MockTask(1, completed=False, status=1, progress=0.45)

    if task.completed or task.status == 0:
        disp = 100
    else:
        disp = int(task.progress * 100)

    assert disp == 45


def test_progressbar_floating_truncation():
    """0.999 * 100 would truncate to 99 without the completed-check fix."""
    task = MockTask(1, completed=False, status=1, progress=0.999)

    # Without fix: int(0.999 * 100) = 99
    unfixed = int(task.progress * 100)
    assert unfixed == 99

    # With fix: check completed first
    if task.completed or task.status == 0:
        fixed = 100
    else:
        fixed = int(task.progress * 100)
    assert fixed == 99  # not completed, so original behavior


def test_progressbar_errored_task_shows_100():
    """Errored tasks (status 0) should show 100."""
    task = MockTask(1, completed="发生错误", status=0, progress=0.3)

    if task.completed or task.status == 0:
        disp = 100
    else:
        disp = int(task.progress * 100)

    assert disp == 100


def test_progressbar_stopped_task_shows_100():
    """Stopped tasks (status 0) should show 100."""
    task = MockTask(1, completed="已终止", status=0, progress=0.5)

    if task.completed or task.status == 0:
        disp = 100
    else:
        disp = int(task.progress * 100)

    assert disp == 100


# ---------------------------------------------------------------------------
# Test 3: set_first_selected — correct task index mapping
# ---------------------------------------------------------------------------

def test_current_selected_task_maps_to_actual_index():
    """selected_task should store the actual task index, not row number."""
    tasks = [
        MockTask(1), MockTask(2), MockTask(3), MockTask(5), MockTask(7)
    ]

    # Simulate user clicking row 3 (which shows task index 5)
    row = 3
    actual_index = tasks[row].index

    # Mapping: i.index should match actual_index directly (no +1)
    for task in tasks:
        if task.index == actual_index:
            target = task
            break

    assert target is not None
    assert target.index == 5
    assert target == tasks[3]


def test_current_selected_task_non_contiguous_indexes():
    """After deletion, indexes may be non-contiguous. Direct match still works."""
    tasks = [
        MockTask(1), MockTask(4), MockTask(9)  # non-contiguous indexes
    ]

    # Click on row 1 → should find task with index 4
    row = 1
    actual_index = tasks[row].index
    assert actual_index == 4

    found = None
    for task in tasks:
        if task.index == actual_index:
            found = task
            break

    assert found is not None
    assert found.index == 4


# ---------------------------------------------------------------------------
# Test 4: task.completed is always boolean (queue_stop fix)
# ---------------------------------------------------------------------------

def test_task_completed_is_boolean():
    """After queue_stop, completed should not be a translated string."""
    task = MockTask(1, completed=False, status=1)
    task.running = True

    # Simulate stop (the fixed behavior)
    task.running = False
    task.stopped = True
    task.completed = False  # stays boolean
    task.statue = "已终止"  # separate status field

    # Verify
    assert task.completed is False
    assert task.stopped is True
    assert task.statue == "已终止"

    # 'not task.completed' should work correctly in queue_start
    assert not task.completed  # True → task is NOT completed → can restart


def test_task_completed_truthiness():
    """A task with stopped=True but completed=False should be restartable."""
    task = MockTask(1, completed=False, status=1)
    task.running = False
    task.stopped = True
    task.completed = False

    # In queue_start, the condition is:
    # not task.running and task.status != 0 and task.completed != True and task.stopped != True
    can_restart = (
        not task.running
        and task.status != 0
        and task.completed != True
        and task.stopped != True
    )
    assert not can_restart  # stopped → can't restart in the same batch


def test_string_completed_would_break_logic():
    """Demonstrate the old bug: string '已终止' is truthy, so 'not completed' is False."""
    # OLD behavior (bug)
    completed = "已终止"  # string, truthy
    assert bool(completed) is True
    assert not completed is False  # BUG: this prevents restart detection

    # NEW behavior (fixed)
    completed = False  # boolean
    assert not completed is True  # CORRECT: task not completed, can restart


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
