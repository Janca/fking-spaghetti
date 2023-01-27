import os.path
import sys
from dataclasses import dataclass as _dataclass
from typing import Optional as _Optional

import fking.scrapers.imagescraper as _fkscrapers


@_dataclass
class _FkSpaghetti:
    active_scraper: _fkscrapers.IScraper = None

    max_attempts: int = 5

    image_download_timeout: int = 5
    scraper_timeout: int = 10

    worker_task_max_attempts: int = max_attempts
    worker_queue_interrupted: bool = False

    max_queue_workers: int = 10

    max_pages_per_term: int = 4
    max_images_per_term: int = sys.maxsize - 1

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
