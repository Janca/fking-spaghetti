import os.path
import tkinter as _tk
from abc import ABC as _ABC
from typing import Optional

import requests

import fking.app as _fkapp
import fking.network as _fknetwork
import fking.ui as _fkui
import fking.utils as _fkutils
from fking.queues import ITask as _ITask

debug_mode = False


class ImageTask(_ITask):
    _url: str
    _caption_text: str
    _dst_dirname: str

    def __init__(self, search_term: str, dst_dirname: str, url: str, caption_text: str) -> None:
        super().__init__()

        self._search_term = search_term
        self._dst_dirname = dst_dirname
        self._url = url
        self._caption_text = caption_text

    def execute(self):
        if debug_mode:
            return

        next_proxy = _fknetwork.next_proxy()

        try:
            response = requests.get(
                self._url,
                headers=_fknetwork.default_headers,
                proxies=next_proxy,
                timeout=_fkapp.context.image_download_timeout
            )

            status_code = response.status_code
            if status_code == 404:
                return

            if status_code != 200:
                raise IOError()

        except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout) as e:
            _fknetwork.mark_bad_proxy(next_proxy)
            raise e

        image_bytes = response.content
        if not image_bytes:
            return

        if not self._caption_text or not _fkutils.contains_partial(self._caption_text, self._search_term):
            output_dirpath = os.path.join(_fkapp.context.erroneous_captions_image_dirpath, self._dst_dirname)
        else:
            output_dirpath = os.path.join(_fkapp.context.matched_captions_image_dirpath, self._dst_dirname)

        os.makedirs(output_dirpath, exist_ok=True)
        hash_name = _fkutils.sha256_str(self._url)

        image_filename = f"{hash_name}.jpg"
        text_filename = f"{hash_name}.txt"

        image_dirpath = os.path.join(output_dirpath, image_filename)
        _fkutils.write_binary(image_dirpath, image_bytes)

        text_filepath = os.path.join(output_dirpath, text_filename)
        _fkutils.write_text(text_filepath, self._caption_text)

    def after(self):
        _fkui.fire(_fkui.EVENT_DOWNLOAD_TASK_COMPLETE)


class ScraperResult:
    has_next: bool
    next_page_url: str
    image_tasks: list[ImageTask]

    def __init__(self, image_tasks: list[ImageTask], has_next: bool, next_page_url: Optional[str] = None) -> None:
        self.next_page_url = next_page_url
        self.image_tasks = image_tasks
        self.has_next = has_next


class IScraper(_ABC):
    _name: str

    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name

    def query(self, query: str, page: int) -> ScraperResult:
        raise NotImplementedError()

    def generate_query_url(self, search_term: str, page: int) -> str:
        raise NotImplementedError()

    def tkinter_settings(self, parent: _tk.Misc) -> Optional[_tk.Widget]:
        return None

    @property
    def name(self):
        return self._name
