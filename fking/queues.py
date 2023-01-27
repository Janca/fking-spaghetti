import queue as _queue
import threading as _threading
from abc import ABC as _ABC
from typing import Callable as _Callable

import fking.app as _fkapp


class ITask(_ABC):
    attempts: int = 0
    active: bool = False

    def execute(self):
        raise NotImplementedError()

    def after(self):
        pass

    def failure(self, e: Exception):
        self.after()


class _TaskFn(ITask):
    _fn: _Callable[[], None]

    def __init__(self, fn: _Callable[[], None]) -> None:
        super().__init__()
        self._fn = fn

    def execute(self):
        self._fn()


_shutdown: bool = False
_thread_workers: list[_threading.Thread] = []
_task_queue: _queue.Queue[ITask] = _queue.Queue()


def _task_thread_fn():
    while not _fkapp.worker_queue_interrupted and not _shutdown:
        try:
            next_task = _task_queue.get(block=True, timeout=5)
        except _queue.Empty:
            continue

        try:
            next_task.active = True
            next_task.execute()
            next_task.after()
        except Exception as e:
            if next_task.attempts < _fkapp.worker_task_max_attempts:
                next_task.attempts += 1
                _task_queue.put(next_task)
            else:
                next_task.failure(e)
        finally:
            next_task.active = False


def get_active_workers() -> list[_threading.Thread]:
    return [thread for thread in _thread_workers if thread.is_alive()]


def purge_inactive_workers() -> list[_threading.Thread]:
    active = get_active_workers()

    _thread_workers.clear()
    _thread_workers.extend(active)

    return active


def start_thread_pool():
    global _shutdown

    _shutdown = False
    max_workers = _fkapp.max_queue_workers
    active_workers = purge_inactive_workers()
    worker_diff = max_workers - len(active_workers)

    if worker_diff <= 0:
        return

    for i in range(worker_diff):
        thread = _threading.Thread(target=_task_thread_fn, daemon=True)
        _thread_workers.append(thread)
        thread.start()


def shutdown():
    global _shutdown

    _shutdown = True
    wait_on_queue()


def wait_on_queue():
    active = get_active_workers()
    for thread in active:
        thread.join()


def queue_task(task: ITask):
    _task_queue.put(task)


def queue_fn(target: _Callable[[], None]):
    queue_task(_TaskFn(target))
