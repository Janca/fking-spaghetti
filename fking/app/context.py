from dataclasses import dataclass as _dataclass


@_dataclass
class _FkSpaghetti:
    worker_task_max_attempts: int = 5
    worker_queue_interrupted: bool = False

    max_queue_workers: int = 10
