import os.path
import queue
import threading
from typing import Callable

import requests

import fking.proxies
import fking.scraper
import fking.utils
from fking.context import context


class ITask:
    attempts: int = 0
    complete: bool = False

    def execute(self):
        pass


class DownloadImageTask(ITask):
    search_term: str
    url: str
    alt_text: str

    def __init__(self, search_term: str, url: str, alt_text: str):
        self.search_term = search_term
        self.url = url
        self.alt_text = alt_text

    def execute(self):
        next_proxy = fking.proxies.next_best_proxy()

        try:
            response = requests.get(
                    self.url,
                    headers=fking.scraper.default_headers,
                    timeout=30,
                    proxies=next_proxy
            )

            status_code = response.status_code
            if status_code == 404:
                return

            if status_code != 200:
                raise IOError()

        except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout) as e:
            fking.proxies.mark_bad_proxy(next_proxy)
            raise e

        image_bytes = response.content
        if len(image_bytes) <= 0:
            return

        sanitized_dirname = fking.utils.sanitize_dirname(self.search_term)
        normalized_alt_text = fking.utils.normalize_alt_text(self.alt_text)

        if not normalized_alt_text or not fking.utils.contains_partial(normalized_alt_text, self.search_term):
            output_dirpath = os.path.join(context.output_mismatched_captions, sanitized_dirname)
        else:
            output_dirpath = os.path.join(context.output_matching_captions, sanitized_dirname)

        os.makedirs(output_dirpath, exist_ok=True)
        hash_name = fking.utils.sha256_str(f"{sanitized_dirname}.{self.url}")

        image_filename = f"{hash_name}.jpg"
        text_filename = f"{hash_name}.txt"

        image_dirpath = os.path.join(output_dirpath, image_filename)
        fking.utils.write_binary(image_dirpath, image_bytes)

        text_filepath = os.path.join(output_dirpath, text_filename)
        fking.utils.write_text(text_filepath, normalized_alt_text)


_queue_image_download: queue.Queue[DownloadImageTask] = queue.Queue(maxsize=10_000)
_threads_image_download: list[threading.Thread] = []


def image_queue_size() -> int:
    return _queue_image_download.qsize()


def _process_queue_thread_fn(
        _queue: queue.Queue,
        condition: Callable[[], bool],
        on_complete: Callable[[bool], None] = None
):
    def thread_fn():
        while condition():
            try:
                next_item = _queue.get(block=True, timeout=5)
            except queue.Empty:
                continue

            try:
                next_item.execute()
                if on_complete:
                    on_complete(True)

            except:
                if next_item.attempts < context.max_attempts:
                    next_item.attempts = next_item.attempts + 1
                    _queue.put(next_item)

                elif on_complete:
                    on_complete(False)

    return thread_fn


def start_image_download_threads():
    global _threads_image_download

    active_threads = [thread for thread in _threads_image_download if thread.is_alive()]
    active_thread_count = len(active_threads)

    _threads_image_download = active_threads
    diff = context.max_threads - active_thread_count

    _queue_image_download.queue.clear()

    if diff > 0:
        for i in range(diff):
            thread_target = _process_queue_thread_fn(
                    _queue_image_download,
                    lambda: context.scraper_busy or not _queue_image_download.empty(),
                    lambda success: context.increment_images_download()
            )

            thread = threading.Thread(target=thread_target, daemon=True)
            _threads_image_download.append(thread)

            thread.start()


def wait_on_image_download_threads():
    if len(_threads_image_download) > 0:
        for thread in _threads_image_download:
            thread.join()


def is_image_queue_empty() -> bool:
    return _queue_image_download.empty()


def queue_image_download(search_term: str, url: str, alt_text: str) -> DownloadImageTask:
    context.total_queued_images = context.total_queued_images + 1
    task = DownloadImageTask(search_term, url, alt_text)
    _queue_image_download.put(task)
    return task
