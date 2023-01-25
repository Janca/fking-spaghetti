from threading import Lock
from typing import Optional


class _FkContext:
    output_directory: Optional[str] = None
    output_matching_captions: Optional[str] = None
    output_mismatched_captions: Optional[str] = None
    output_focals: Optional[str] = None

    search_terms_path: Optional[str] = None
    search_terms: list[str] = None

    _images_downloaded: int = 0
    total_queued_images = 0

    max_threads = 10

    _mutex: Lock = Lock()

    scraper_busy: bool = False
    interrupted: bool = False

    max_attempts = 5
    max_pages = 4

    @property
    def is_ready(self):
        return self.output_directory and self.search_terms

    @property
    def search_terms_length(self):
        return len(self.search_terms) if self.search_terms else 0

    @property
    def images_downloaded(self):
        with self._mutex:
            return self._images_downloaded

    def increment_images_download(self, v: int = 1):
        with self._mutex:
            value = self._images_downloaded
            self._images_downloaded = value + v

    def reset(self, busy: bool = False):
        self.scraper_busy = busy
        self.interrupted = False
        self._images_downloaded = 0
        self.total_queued_images = 0


context = _FkContext()
