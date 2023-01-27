import collections
import queue as _queue
import tkinter as _tk
from typing import Callable

_MAX_EVENTS_PER_CYCLE = 20

_Event = collections.namedtuple("_fkTkinterEvent", ["type", "args", "kwargs"])

_listeners = {}
_event_queue: _queue.Queue[_Event] = _queue.Queue()


def bind(event_type: str, listener: Callable[[..., ...], None]):
    if event_type not in _listeners:
        _listeners[event_type] = []
    _listeners[event_type].append(listener)


def unbind(event_type: str, listener: Callable[[..., ...], None]):
    if event_type in _listeners:
        _listeners[event_type].remove(listener)


def fire(event_type: str, *args, **kwargs):
    event = _Event(event_type, args, kwargs)
    _event_queue.put(event)


def process_queue():
    processed = 0
    while not _event_queue.empty() and processed < _MAX_EVENTS_PER_CYCLE:
        try:
            event = _event_queue.get_nowait()
        except _queue.Empty:
            break

        event_type, args, kwargs = event

        if event_type in _listeners:
            for listener in _listeners[event_type]:
                processed += 1

                try:
                    listener(*args, **kwargs)
                except Exception as e:
                    fire("<<EventException>>", event, e)


def start_tkinter_event_bus(tk: _tk.Misc):
    process_queue()
    tk.after(42, lambda _tk=tk: start_tkinter_event_bus(_tk))
