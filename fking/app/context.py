import os.path
import sys
import threading
from dataclasses import dataclass as _dataclass
from typing import Optional as _Optional

import fking.queues as _fkqueues
import fking.scrapers.imagescraper as _fkscrapers


@_dataclass
class _FkSpaghetti:
    scraper_active: bool = False

    _scraper_thread: threading.Thread = None
    active_scraper: _fkscrapers.IScraper = None

    max_attempts: int = 5

    image_download_timeout: int = 5
    scraper_timeout: int = 10

    worker_task_max_attempts: int = max_attempts
    worker_queue_interrupted: bool = False

    max_queue_workers: int = 10

    max_pages_per_term: int = 4
    max_images_per_term: int = sys.maxsize - 1
    max_images_total: int = sys.maxsize - 1

    query_list_path: str = None
    download_directory: str = None

    @property
    def matched_captions_image_dirpath(self) -> str:
        return os.path.join(self.download_directory, "raw")

    @property
    def erroneous_captions_image_dirpath(self) -> str:
        return os.path.join(self.matched_captions_image_dirpath, "__erroneous")

    @property
    def cropped_images_dirpath(self) -> str:
        return os.path.join(self.download_directory, "cropped")

    @property
    def active_scraper_name(self) -> _Optional[str]:
        scraper = self.active_scraper
        return scraper.name if scraper else None

    def read_query_terms(self) -> list[str]:
        terms = []

        with open(self.query_list_path, 'r') as f:
            lines = f.read().splitlines()
            f.close()

            for l in lines:
                l_normalized = l.lower().strip()
                if l_normalized not in terms:
                    terms.append(l_normalized)

        return terms

    def start_scraper_thread(self) -> threading.Thread:
        thread = self._scraper_thread
        if thread is not None:
            if thread.is_alive():
                raise RuntimeError("Scraper thread is busy.")

            def scraper_thread_fn():
                self.scraper_active = True

                _fkqueues.shutdown()
                _fkqueues.start_thread_pool()

                current_search_term_idx = 0

                queries_term = self.read_query_terms()
                queries_length = len(queries_term)

                while self.scraper_active:
                    if current_search_term_idx >= queries_length:
                        break

                    current_search_term = queries_term[current_search_term_idx]
                    image_tasks = self.active_scraper.query(current_search_term)


                    current_search_term_idx += 1

        self._scraper_thread = threading.Thread(target=scraper_thread_fn, daemon=True)
        self._scraper_thread.start()

        return self._scraper_thread
