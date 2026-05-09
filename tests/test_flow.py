"""
Integration / flow tests for the task queue lifecycle, progress synchronization,
and state management logic.
"""
import sys
import os
import time
import random
import threading
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ==============================================================================
# Mock infrastructure
# ==============================================================================

class MockProgressBar:
    """Simulates a QProgressBar for testing."""
    def __init__(self):
        self._value = 0
        self._max = 100

    def value(self):
        return self._value

    def setValue(self, v):
        self._value = max(0, min(self._max, int(v)))

    def reset(self):
        self._value = 0


class MockSignal:
    """Simulates a PySide6 Signal for testing."""
    def __init__(self):
        self._callbacks = []

    def connect(self, callback):
        self._callbacks.append(callback)

    def emit(self, *args, **kwargs):
        for cb in self._callbacks:
            cb(*args, **kwargs)


class MockTask:
    """Full mock of ProcessUnit for flow testing."""
    def __init__(self, index, file="test.mp4"):
        self.index = index
        self.file = file
        self.completed = False
        self.running = False
        self.stopped = False
        self.paused = False
        self.status = 1
        self.statue = "等待中"
        self.progress = 0.0
        self.progress_identify = f"uuid_{index}"
        self.update_progress = MockSignal()
        self.OccurError = MockSignal()
        self.start_time = None
        self.consumed_timer = None
        self.output_path = "./output"
        self.output_format = "mp4"
        self.watermark_method = None
        self.attachment_data = {}
        self.frame_count = 300
        self.process_limit = 16
        self.dump_uuid = f"dump_{index}"
        self.description = "test task"

    def run(self):
        """Simulate task execution."""
        self.running = True
        self.statue = "运行中"
        self.consumed_timer = time.time()
        self.start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            for i in range(1, 11):
                if self.stopped:
                    return
                while self.paused:
                    time.sleep(0.01)
                    if self.stopped:
                        return
                self.progress = i / 10.0
                self.update_progress.emit(
                    self.progress,
                    f"Processing {i}/10",
                    self.progress_identify,
                )
                time.sleep(0.01)
            self.completed = True
            self.status = 1
            self.statue = "已完成"
        except Exception:
            self.completed = "发生错误"
            self.status = 0
            self.statue = "错误"
        finally:
            self.running = False

    def stop(self):
        self.stopped = True
        self.running = False

    def suspend(self):
        self.paused = True
        self.running = False
        self.statue = "已暂停"

    def resume(self):
        self.paused = False
        self.running = True
        self.statue = "运行中"


class MockQueueTable:
    """Simulates the QTableWidget queue list."""
    def __init__(self):
        self._rows = []

    def rowCount(self):
        return len(self._rows)

    def insertRow(self, row):
        self._rows.insert(row, {
            "index": None,
            "name": None,
            "status": None,
            "thumbnail": None,
            "progress_bar": MockProgressBar(),
            "output_path": None,
        })

    def setRowCount(self, count):
        while len(self._rows) < count:
            self.insertRow(len(self._rows))
        self._rows = self._rows[:count]

    def clearContents(self):
        self._rows = []

    def setItem(self, row, col, item):
        pass

    def item(self, row, col):
        if col == 0 and row < len(self._rows):
            class MockItem:
                def text(self):
                    return str(self._index)
            obj = MockItem()
            obj._index = row + 1  # Simple 1:1 mapping for tests
            return obj
        return None

    def cellWidget(self, row, col):
        if col == 4 and row < len(self._rows):
            return self._rows[row]["progress_bar"]
        return None


# ==============================================================================
# Queue management (simulated MainWindow logic)
# ==============================================================================

class MockQueueManager:
    """Simulates the queue management logic from MainWindow."""
    def __init__(self):
        self.task_queue = []
        self.QueueList = MockQueueTable()
        self.QueueProgressBar = MockProgressBar()
        self.progressBar = MockProgressBar()
        self.started = False
        self.played = False
        self.current_selected_task = None
        self.default_detail_show = None
        self.thumbnail_cache = {}

    def add_task(self, task):
        task.index = len(self.task_queue) + 1
        self.task_queue.append(task)
        self.sync_queue()

    def add_tasks(self, tasks):
        for t in tasks:
            t.index = len(self.task_queue) + 1
            self.task_queue.append(t)
        self.sync_queue()

    def remove_task(self, index):
        for t in self.task_queue:
            if t.index == index:
                self.task_queue.remove(t)
                break
        self.sync_queue()

    def sync_queue(self):
        self.QueueList.setRowCount(0)
        self.QueueList.clearContents()
        for i, task in enumerate(self.task_queue):
            self.QueueList.insertRow(i)
            bar = MockProgressBar()
            bar.setValue(0)
            self.QueueList._rows[i]["progress_bar"] = bar

    def start_all(self):
        self.started = True
        self.played = False
        for task in self.task_queue:
            if not task.running and task.status != 0 and not task.completed and not task.stopped:
                task.update_progress.connect(self._on_task_progress)
                threading.Thread(target=task.run, daemon=True).start()

    def _on_task_progress(self, value, msg, uuid):
        for task in self.task_queue:
            if task.progress_identify == uuid:
                task.progress = value
                break

    def queue_stop(self):
        for task in self.task_queue:
            if task.running:
                task.stop()
                task.running = False
                task.stopped = True
                task.statue = "已终止"

    def queue_suspend(self):
        for task in self.task_queue:
            if task.running and task.process_limit != 1:
                task.suspend()
                task.running = False
                task.paused = True

    def update_total_progress(self):
        """Replicates the fixed update_total_progress logic."""
        total_progress = 0
        tpb = 0
        if self.QueueList.rowCount() != 0:
            for task in self.task_queue:
                if not task.completed:
                    total_progress += 1
            for pb in range(self.QueueList.rowCount()):
                if pb < len(self.task_queue) and not self.task_queue[pb].completed:
                    progress_bar = self.QueueList.cellWidget(pb, 4)
                    if progress_bar is not None:
                        tpb += progress_bar.value()
            if total_progress != 0:
                self.QueueProgressBar.setValue(tpb / total_progress)
            else:
                self.QueueProgressBar.setValue(100)
        else:
            self.QueueProgressBar.setValue(0)

    def update_details_progress(self, task):
        """Replicates the fixed update_details progress bar logic."""
        if task is None:
            self.progressBar.setValue(0)
            return
        if task.completed or task.status == 0:
            self.progressBar.setValue(100)
        else:
            self.progressBar.setValue(int(task.progress * 100))

    def wait_all_done(self, timeout=5.0):
        deadline = time.time() + timeout
        while time.time() < deadline:
            all_done = all(t.completed for t in self.task_queue)
            if all_done:
                break
            time.sleep(0.05)
        return all(t.completed for t in self.task_queue)


# ==============================================================================
# Flow Test 1: Single task complete lifecycle
# ==============================================================================

class TestSingleTaskLifecycle:
    """Test: add one task, start, wait for completion, verify all states."""

    def test_single_task_flow(self):
        mgr = MockQueueManager()

        # --- Phase 1: Queue empty ---
        mgr.update_total_progress()
        assert mgr.QueueProgressBar.value() == 0
        assert len(mgr.task_queue) == 0

        # --- Phase 2: Add task ---
        task = MockTask(1)
        mgr.add_task(task)
        assert len(mgr.task_queue) == 1
        assert task.index == 1
        assert task.completed is False
        assert task.running is False

        mgr.update_total_progress()
        # One task, not started, progress=0
        assert mgr.QueueProgressBar.value() == 0

        mgr.update_details_progress(task)
        assert mgr.progressBar.value() == 0

        # --- Phase 3: Start ---
        mgr.start_all()
        assert mgr.started is True
        assert mgr.played is False

        # --- Phase 4: Wait for completion ---
        done = mgr.wait_all_done(timeout=3.0)
        assert done, "Task did not complete in time"

        # --- Phase 5: Verify completed state ---
        assert task.completed is True
        assert task.status == 1
        assert task.running is False

        mgr.update_total_progress()
        assert mgr.QueueProgressBar.value() == 100  # All done

        mgr.update_details_progress(task)
        assert mgr.progressBar.value() == 100  # Completed → 100


# ==============================================================================
# Flow Test 2: Queue progress tracks individual tasks correctly
# ==============================================================================

class TestProgressSynchronization:
    """Test: overall queue progress correctly aggregates individual task progress."""

    def test_queue_progress_matches_individual(self):
        mgr = MockQueueManager()
        tasks = [MockTask(i) for i in range(3)]
        mgr.add_tasks(tasks)

        mgr.start_all()
        mgr.wait_all_done(timeout=3.0)

        # After all done, queue should show 100
        mgr.update_total_progress()
        assert mgr.QueueProgressBar.value() == 100

        # Each individual task's detail should show 100
        for t in tasks:
            mgr.update_details_progress(t)
            assert mgr.progressBar.value() == 100

    def test_new_tasks_dont_keep_old_progress(self):
        """Core regression test: new tasks after a completed batch
        should not inherit old progress."""
        mgr = MockQueueManager()

        # Batch 1: 3 tasks, all complete
        batch1 = [MockTask(i) for i in range(3)]
        mgr.add_tasks(batch1)
        mgr.start_all()
        mgr.wait_all_done(timeout=3.0)
        mgr.update_total_progress()
        assert mgr.QueueProgressBar.value() == 100

        # Batch 2: add 2 new tasks
        batch2 = [MockTask(i) for i in range(3, 5)]
        mgr.add_tasks(batch2)

        # Before starting new tasks, queue should show 0
        # (old completed tasks are skipped)
        mgr.update_total_progress()
        assert mgr.QueueProgressBar.value() == 0, (
            f"Expected 0, got {mgr.QueueProgressBar.value()} — "
            f"old completed tasks should not inflate queue progress"
        )

        # New individual tasks should show 0
        for t in batch2:
            mgr.update_details_progress(t)
            assert mgr.progressBar.value() == 0

        # Start new batch → should go to 100
        mgr.start_all()
        mgr.wait_all_done(timeout=3.0)
        mgr.update_total_progress()
        assert mgr.QueueProgressBar.value() == 100


# ==============================================================================
# Flow Test 3: Task state transitions (pause/resume/stop)
# ==============================================================================

class TestTaskStateTransitions:
    """Test: tasks correctly transition through pause/resume/stop states."""

    def test_pause_resume_flow(self):
        mgr = MockQueueManager()
        task = MockTask(1)
        mgr.add_task(task)

        # Start running
        t = threading.Thread(target=task.run, daemon=True)
        t.start()
        time.sleep(0.02)  # Let it start

        assert task.running is True

        # Pause
        task.suspend()
        assert task.paused is True
        assert task.running is False
        assert task.statue == "已暂停"

        progress_before_pause = task.progress

        # Resume
        task.resume()
        assert task.paused is False
        assert task.running is True
        assert task.statue == "运行中"

        t.join(timeout=2.0)
        assert task.completed is True

    def test_stop_flow(self):
        mgr = MockQueueManager()
        task = MockTask(1)
        mgr.add_task(task)

        # Start running
        t = threading.Thread(target=task.run, daemon=True)
        t.start()
        time.sleep(0.02)

        # Stop
        task.stop()
        task.running = False
        task.stopped = True
        task.statue = "已终止"

        t.join(timeout=1.0)

        assert task.stopped is True
        assert task.running is False
        assert task.statue == "已终止"

        # After stop, the queue shows 0 because stopped tasks still
        # have completed=False and contribute to total_progress with 0% progress
        mgr.update_total_progress()
        assert mgr.QueueProgressBar.value() == 0  # 1 stopped task at 0%

    def test_queue_stop_all(self):
        mgr = MockQueueManager()
        tasks = [MockTask(i) for i in range(3)]
        mgr.add_tasks(tasks)

        mgr.start_all()
        time.sleep(0.05)

        mgr.queue_stop()

        for t in tasks:
            assert t.stopped is True
            assert t.running is False
            assert t.statue == "已终止"
            assert t.completed in (True, False)  # boolean, not string

        # Stopped tasks have completed=False → total_progress counts them
        # Their progress is 0 → overall shows 0
        mgr.update_total_progress()
        assert mgr.QueueProgressBar.value() == 0


# ==============================================================================
# Flow Test 4: Task deletion mid-queue
# ==============================================================================

class TestTaskDeletion:
    """Test: removing tasks correctly updates queue state."""

    def test_delete_middle_task(self):
        mgr = MockQueueManager()
        tasks = [MockTask(i) for i in range(5)]
        mgr.add_tasks(tasks)

        assert len(mgr.task_queue) == 5

        # Delete task at index 3 (mid-queue)
        mgr.remove_task(3)
        assert len(mgr.task_queue) == 4

        # Remaining indexes should be: 1, 2, 4, 5 (gap at 3)
        remaining = [t.index for t in mgr.task_queue]
        assert remaining == [1, 2, 4, 5]

        # Non-contiguous indexes should not break progress calculation
        mgr.update_total_progress()
        assert mgr.QueueProgressBar.value() == 0  # 4 tasks at 0%

    def test_delete_all_tasks(self):
        mgr = MockQueueManager()
        tasks = [MockTask(i) for i in range(3)]
        mgr.add_tasks(tasks)

        for t in list(mgr.task_queue):
            mgr.remove_task(t.index)

        assert len(mgr.task_queue) == 0
        mgr.update_total_progress()
        assert mgr.QueueProgressBar.value() == 0


# ==============================================================================
# Flow Test 5: Error handling
# ==============================================================================

class TestErrorHandlingFlow:
    """Test: tasks that error out correctly update queue state."""

    def test_errored_task_excluded_from_progress(self):
        mgr = MockQueueManager()

        # Task 1: will complete normally
        t1 = MockTask(1)
        mgr.add_task(t1)

        # Task 2: will "error out"
        t2 = MockTask(2)
        t2.completed = "发生错误"
        t2.status = 0
        t2.running = False
        mgr.add_task(t2)

        # Task 3: not started
        t3 = MockTask(3)
        mgr.add_task(t3)

        # Only task1 and task3 are active
        mgr.update_total_progress()
        assert mgr.QueueProgressBar.value() == 0  # all at 0%

        # Task details for errored task should show 100
        mgr.update_details_progress(t2)
        assert mgr.progressBar.value() == 100

        # Start and complete task1
        mgr.start_all()
        t1.progress = 1.0
        t1.completed = True
        t1.running = False
        t1.status = 1

        mgr.update_total_progress()
        # Only task3 is active (at 0%), task1 done, task2 error
        assert mgr.QueueProgressBar.value() == 0

    def test_mixed_completed_error_running(self):
        mgr = MockQueueManager()

        t_complete = MockTask(1)
        t_complete.completed = True
        t_complete.status = 1
        t_complete.progress = 1.0
        mgr.task_queue.append(t_complete)

        t_error = MockTask(2)
        t_error.completed = "发生错误"
        t_error.status = 0
        t_error.progress = 0.3
        mgr.task_queue.append(t_error)

        t_running = MockTask(3)
        t_running.completed = False
        t_running.status = 1
        t_running.progress = 0.6
        mgr.task_queue.append(t_running)

        t_pending = MockTask(4)
        t_pending.completed = False
        t_pending.status = 1
        t_pending.progress = 0.0
        mgr.task_queue.append(t_pending)

        mgr.sync_queue()

        # Simulate what set_is_completed and update_queue_percentage do:
        # set row bars for completed/errored to 100, running to actual progress
        for pb, task in enumerate(mgr.task_queue):
            bar = mgr.QueueList.cellWidget(pb, 4)
            if task.completed or task.status == 0:
                bar.setValue(100)
            else:
                bar.setValue(int(task.progress * 100))

        active = [t for t in mgr.task_queue if not t.completed]
        assert len(active) == 2
        assert active == [t_running, t_pending]

        mgr.update_total_progress()
        expected = (60 + 0) / 2  # 30%
        assert mgr.QueueProgressBar.value() == int(expected)


# ==============================================================================
# Flow Test 6: Progress aggregation calculation
# ==============================================================================

class TestProgressAggregation:
    """Test: verify the math of progress aggregation across multiple tasks."""

    @pytest.mark.parametrize("progresses,expected", [
        ([0.0], 0),
        ([0.5], 50),
        ([1.0], 100),
        ([0.0, 0.0], 0),
        ([0.5, 0.5], 50),
        ([1.0, 1.0], 100),
        ([0.0, 0.5, 1.0], 50),
        ([0.25, 0.75], 50),
        ([0.0, 0.0, 0.0, 0.5], 12),
    ])
    def test_progress_math(self, progresses, expected):
        mgr = MockQueueManager()

        for i, p in enumerate(progresses):
            t = MockTask(i + 1)
            t.progress = p
            t.completed = False
            mgr.task_queue.append(t)

        mgr.sync_queue()

        total_progress = 0
        tpb = 0
        for task in mgr.task_queue:
            if not task.completed:
                total_progress += 1
                tpb += int(task.progress * 100)

        if total_progress > 0:
            result = tpb / total_progress
        else:
            result = 0

        assert int(result) == expected, (
            f"Progresses: {progresses}; tpb={tpb}, total={total_progress}"
        )


# ==============================================================================
# Flow Test 7: thread safety — multiple tasks completing simultaneously
# ==============================================================================

class TestConcurrentTaskCompletion:
    """Test: multiple tasks completing in parallel update queue correctly."""

    def test_concurrent_completion(self):
        mgr = MockQueueManager()
        tasks = [MockTask(i) for i in range(10)]
        mgr.add_tasks(tasks)
        mgr.start_all()
        done = mgr.wait_all_done(timeout=5.0)
        assert done

        mgr.update_total_progress()
        assert mgr.QueueProgressBar.value() == 100


# ==============================================================================
# Flow Test 8: Old-completed tasks don't affect new batch progress
# ==============================================================================

class TestBatchIsolation:
    """Test: completed tasks from batch 1 don't affect batch 2 progress."""

    def test_three_batches_independent(self):
        mgr = MockQueueManager()

        for batch_num in range(3):
            tasks = [MockTask(i) for i in range(3)]
            mgr.add_tasks(tasks)

            # Before start
            mgr.update_total_progress()
            assert mgr.QueueProgressBar.value() == 0, (
                f"Batch {batch_num}: should start at 0%"
            )

            mgr.start_all()
            mgr.wait_all_done(timeout=3.0)

            mgr.update_total_progress()
            assert mgr.QueueProgressBar.value() == 100, (
                f"Batch {batch_num}: should end at 100%"
            )

        # Total: 9 tasks (3 batches × 3)
        assert len(mgr.task_queue) == 9

        # All completed
        completed = sum(1 for t in mgr.task_queue if t.completed)
        assert completed == 9

        # QueueProgressBar should be 100 (no active tasks)
        mgr.update_total_progress()
        assert mgr.QueueProgressBar.value() == 100


# ==============================================================================
# Flow Test 9: Current selected task updates correctly
# ==============================================================================

class TestCurrentTaskSelection:
    """Test: selecting a task shows correct info in detail panel."""

    def test_select_completed_task_shows_100(self):
        mgr = MockQueueManager()
        task = MockTask(1)
        task.completed = True
        task.status = 1
        task.progress = 1.0
        mgr.add_task(task)

        mgr.update_details_progress(task)
        assert mgr.progressBar.value() == 100

    def test_select_running_task_shows_actual(self):
        mgr = MockQueueManager()
        task = MockTask(1)
        task.completed = False
        task.status = 1
        task.progress = 0.67
        mgr.add_task(task)

        mgr.update_details_progress(task)
        assert mgr.progressBar.value() == 67

    def test_select_none_task_shows_0(self):
        mgr = MockQueueManager()
        mgr.update_details_progress(None)
        assert mgr.progressBar.value() == 0

    def test_select_task_with_non_contiguous_index(self):
        """After deleting task 2, clicking row for task 3 should find it."""
        mgr = MockQueueManager()

        t1 = MockTask(1, file="a.mp4")
        t2 = MockTask(2, file="b.mp4")
        t3 = MockTask(3, file="c.mp4")
        mgr.add_tasks([t1, t2, t3])

        # Simulate deleting t2
        mgr.remove_task(2)

        # Now indexes are [1, 3]
        remaining = [t.index for t in mgr.task_queue]
        assert remaining == [1, 3]

        # The matching logic: find task by index
        target_index = 3
        found = None
        for t in mgr.task_queue:
            if t.index == target_index:
                found = t
                break

        assert found is not None
        assert found.file == "c.mp4"


# ==============================================================================
# Flow Test 10: Queue sync preserves task order
# ==============================================================================

class TestQueueSync:
    """Test: sync_queue correctly rebuilds the table in task_queue order."""

    def test_sync_preserves_order(self):
        mgr = MockQueueManager()
        tasks = [MockTask(i) for i in range(5)]
        mgr.add_tasks(tasks)

        for i, task in enumerate(mgr.task_queue):
            assert task.index == i + 1

        # Delete middle task and re-sync
        mgr.remove_task(3)
        assert len(mgr.task_queue) == 4
        assert [t.index for t in mgr.task_queue] == [1, 2, 4, 5]

    def test_sync_resets_progress_bars(self):
        mgr = MockQueueManager()

        t = MockTask(1)
        t.completed = True
        t.progress = 1.0
        mgr.add_task(t)

        # After sync_queue, the table row progress bars are rebuilt from scratch
        mgr.sync_queue()
        for row in range(mgr.QueueList.rowCount()):
            bar = mgr.QueueList.cellWidget(row, 4)
            assert bar.value() == 0  # Sync resets to 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
