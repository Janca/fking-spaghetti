import threading as _threading

import fking.queues as _fkqueues
from fking.app.context import _FkSpaghetti

# noinspection PyUnresolvedReferences
__all__ = [
    "context",
    "start_scraper",
    "stop_scraper"
]

context = _FkSpaghetti()


def start_scraper() -> _threading.Thread:
    return context.start_scraper_thread()


def stop_scraper(clear: bool = False):
    context.worker_queue_interrupted = True
    _fkqueues.shutdown(clear)
