import tkinter as _tk
import tkinter.ttk as _ttk
import urllib.parse as _urllib_parse
from typing import Optional

import bs4 as _bs4
import requests as _requests

import fking.app as _fkapp
import fking.network as _fknetwork
import fking.utils as _fkutils
from fking.scrapers.imagescraper import IScraper as _IScraper, \
    ImageTask as _ImageTask


class GettyImages(_IScraper):
    _sort_by_values = ["Best Match", "Newest", "Most Popular"]
    _color_and_mood_values = ["All", "Black & White", "Bold", "Cool", "Dramatic", "Natural", "Vivid", "Warm"]

    _sort_by = _sort_by_values[2]
    _color_and_mood = _color_and_mood_values[0]

    def __init__(self) -> None:
        super().__init__("GettyImages")

    def query(self, search_query: str, _page: int = 1, _current_length: int = 0) -> list[_ImageTask]:
        next_proxy = _fknetwork.next_proxy()

        try:
            url = self.generate_query_url(search_query, _page)
            response = _requests.get(
                    url,
                    headers=_fknetwork.default_headers,
                    proxies=next_proxy,
                    timeout=_fkapp.context.image_download_timeout
            )

            if response.status_code != 200:
                raise IOError(f"Invalid response code [{response.status_code}] for '{url}'")

            document_html = response.text
            document_soup = _bs4.BeautifulSoup(document_html, "html.parser")

            document_title = document_soup.find("h1")
            if document_title and document_title.text == "Oops! We can't find the page you are looking for.":
                return []

            image_tasks: list[_ImageTask] = []
            gallery_images = document_soup.find_all("img", {"class": "MosaicAsset-module__thumb___yvFP5"})

            def is_full() -> bool:
                return _current_length + len(image_tasks) >= _fkapp.context.max_images_per_term

            if gallery_images:
                query_dirname = _fkutils.sanitize_dirname(search_query)

                for gallery_image in gallery_images:
                    if is_full():
                        return image_tasks

                    image_url = gallery_image["src"]
                    image_alt_text = gallery_image["alt"]

                    caption_text = self._normalize_alt_text(image_alt_text)
                    image_task = _ImageTask(search_query, query_dirname, image_url, caption_text)
                    image_tasks.append(image_task)

            next_button_class = "PaginationRow-module__button___QQbMu PaginationRow-module__nextButton___gH3HZ"
            next_button = document_soup.find("button", {"class": next_button_class})

            if next_button and _page < _fkapp.context.max_pages_per_term and not is_full():
                child_image_tasks = self.query(search_query, _page + 1, _current_length + len(image_tasks))
                if child_image_tasks:
                    image_tasks.extend(child_image_tasks)

            return image_tasks

        except (_requests.exceptions.ProxyError, _requests.exceptions.ConnectTimeout) as e:
            _fknetwork.mark_bad_proxy(next_proxy)
            raise e

        except IOError as e:
            raise e

    def generate_query_url(self, search_term: str, page: int) -> str:
        sort_by = self._sort_by.lower().replace(' ', '')

        url_term = ''.join([ch if ch.isalnum() else '-' if ch == ' ' else '' for ch in search_term])
        phrase_term = _urllib_parse.quote(search_term)
        url = f"https://www.gettyimages.com/photos/{url_term}" \
              f"?assettype=image" \
              f"&license=rf" \
              f"&alloweduse=availableforalluses" \
              f"&family=creative" \
              f"&phrase={phrase_term}" \
              f"&sort={sort_by}" \
              f"&numberofpeople=none" \
              f"&page={page}"

        color_and_mood = self._color_and_mood.lower()
        if color_and_mood != 'all':
            if color_and_mood == 'natural':
                color_and_mood = 'neutral'
            elif color_and_mood == 'bold':
                color_and_mood = 'dramatic'
            elif color_and_mood == 'dramatic':
                color_and_mood = 'moody'
            elif color_and_mood == 'black & white':
                color_and_mood = 'bandw'
            url += f"&mood={color_and_mood}"

        return url

    def tkinter_settings(self, parent: _tk.Misc) -> Optional[_tk.Widget]:
        wrapper = _tk.Frame(parent)
        wrapper.grid_columnconfigure(0, weight=1)

        combobox_sort_by = _ttk.Combobox(wrapper, justify=_tk.LEFT, values=self._sort_by_values, state="readonly")
        combobox_color_and_mood = _ttk.Combobox(wrapper, justify=_tk.LEFT, values=self._color_and_mood_values,
                                                state="readonly")

        combobox_sort_by.current(2)
        combobox_color_and_mood.current(0)

        label_sort_by = _ttk.Label(wrapper, text="Sort By")
        label_color_and_mood = _ttk.Label(wrapper, text="Color & Mood")

        def update_sort_by(*args):
            current_idx = combobox_sort_by.current()
            self._sort_by = self._sort_by_values[current_idx]

        def update_mood(*args):
            current_idx = combobox_color_and_mood.current()
            self._color_and_mood = self._color_and_mood_values[current_idx]

            print(self.generate_query_url("test term", 1))

        combobox_sort_by.bind("<<ComboboxSelected>>", update_sort_by)
        combobox_color_and_mood.bind("<<ComboboxSelected>>", update_mood)

        label_sort_by.grid(row=0, column=0, sticky=_tk.NSEW)
        combobox_sort_by.grid(row=1, column=0, sticky=_tk.NSEW, pady=(0, 3))
        label_color_and_mood.grid(row=2, column=0, sticky=_tk.NSEW, pady=(3, 0))
        combobox_color_and_mood.grid(row=3, column=0, sticky=_tk.NSEW)

        return wrapper

    @staticmethod
    def _normalize_alt_text(alt_text: str) -> str:
        tags_text = alt_text
        if " - " in alt_text and ("stock picture" in alt_text or "royalty-free" in alt_text):
            _alt_text = alt_text[:alt_text.rindex(" - ")].strip()
            _alt_text = _fkutils.normalize_tags(_alt_text)
            if len(_alt_text) > 0:
                tags_text = _alt_text

        return _fkutils.normalize_tags(tags_text)
