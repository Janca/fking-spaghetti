from fking.app.context import _FkSpaghetti

# noinspection PyUnresolvedReferences
__all__ = [
    "context"
    #
    # context properties
    "active_scrapper",
    "active_scraper_name",
    "max_attempts",

    "image_download_timeout",
    "scraper_timeout",

    "worker_task_max_attempts",
    "worker_queue_interrupted",

    "max_queue_workers",

    "max_pages_per_term",
    "max_images_per_term",

    "download_directory"
    # end of context properties
    #
]

context = _FkSpaghetti()


def __getattr__(name):
    return context.__getattribute__(name)
