from fking.eventbus import bind, start_tkinter_event_bus, process_queue, fire, unbind
from fking.ui.primary import show

__all__ = [
    "show",
    "bind",
    "start_tkinter_event_bus",
    "process_queue",
    "fire",
    "unbind",

    "EVENT_DOWNLOAD_TASK_ADDED",
    "EVENT_DOWNLOAD_TASK_COMPLETE",

    "EVENT_SEARCH_TERM_ADDED",
    "EVENT_SEARCH_TERM_COMPLETE",

    "EVENT_STATUS_BAR_TEXT"
]

SCRAPER_STARTED = "<<ScraperStarted>>"
SCRAPER_COMPLETE = "<ScraperComplete>>"
SCRAPER_INTERRUPTED = "<<ScraperInterrupted>>"

EVENT_DOWNLOAD_TASK_ADDED = "<<DownloadTaskAdded>>"
EVENT_DOWNLOAD_TASK_COMPLETE = "<<DownloadTaskComplete>>"

EVENT_SEARCH_TERM_ADDED = "<<SearchTermAdded>>"
EVENT_SEARCH_TERM_COMPLETE = "<<SearchTermComplete>>"

EVENT_STATUS_BAR_TEXT = "<<StatusBarText>>"
