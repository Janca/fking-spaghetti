from fking.app.context import _FkSpaghetti

# noinspection PyUnresolvedReferences
__all__ = [
    "worker_task_max_attempts",
    "worker_queue_interrupted",
    "max_queue_workers"
]

_context = _FkSpaghetti()


def __getattr__(name):
    return _context.__getattribute__(name)
