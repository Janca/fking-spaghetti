import tkinter as _tk
import tkinter.simpledialog as _tksimpledialog
import tkinter.ttk as _ttk
from typing import Optional

import bs4 as _bs4
import requests as _requests

import fking.app as _fkapp
import fking.network as _fknetwork
import fking.ui.widgets as _fkwidgets
import fking.utils as _fkutils
from fking.scrapers.imagescraper import IScraper as _IScraper, \
    ImageTask as _ImageTask


class GettyImages(_IScraper):
    _sort_by_values = ["Best Match", "Newest", "Most Popular"]
    _color_and_mood_values = ["Black & White", "Bold", "Cool", "Dramatic", "Natural", "Vivid", "Warm"]
    _orientation_values = ["Vertical", "Horizontal", "Square", "Panoramic Horizontal", "Panoramic Vertical"]
    _style_values = [
        "Abstract", "Close-up", "Cut Out",
        "Copy Space", "Full Frame", "Macro",
        "Portrait", "Sparse", "Still Life"
    ]

    _sort_by = _sort_by_values[2]
    _color_and_mood = _color_and_mood_values[0]

    def __init__(self) -> None:
        super().__init__("Getty Images")

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

        url_term = _fkutils.kebab_case(search_term)
        phrase_term = _fkutils.url_encode(search_term)
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

        frame_orientations_wrapper, mood_toggles, = _fkwidgets.create_toggle_buttons_panel(
                wrapper,
                self._color_and_mood_values
        )

        def update_sort_by(*args):
            current_idx = combobox_sort_by.current()
            self._sort_by = self._sort_by_values[current_idx]

        def update_mood(*args):
            current_idx = combobox_color_and_mood.current()
            self._color_and_mood = self._color_and_mood_values[current_idx]

        combobox_sort_by.bind("<<ComboboxSelected>>", update_sort_by)
        combobox_color_and_mood.bind("<<ComboboxSelected>>", update_mood)

        label_sort_by.grid(row=0, column=0, sticky=_tk.NSEW)
        combobox_sort_by.grid(row=1, column=0, sticky=_tk.NSEW, pady=(0, 3))
        label_color_and_mood.grid(row=2, column=0, sticky=_tk.NSEW, pady=(3, 0))
        combobox_color_and_mood.grid(row=3, column=0, sticky=_tk.NSEW)

        # _fkwidgets.section_divider(wrapper, pady=15).grid(row=4, column=0, sticky=_tk.NSEW)
        label_orientations = _ttk.Label(wrapper, text="Orientations")
        label_orientations.grid(row=4, column=0, sticky=_tk.NSEW, pady=(6, 0))

        wrapper.grid_rowconfigure(5, weight=0)
        frame_orientations_wrapper.grid(row=5, column=0, sticky=_tk.EW)

        frame_styles_wrapper, styles_toggles = _fkwidgets.create_toggle_buttons_panel(wrapper, self._style_values)

        # _fkwidgets.section_divider(wrapper, pady=15).grid(row=6, column=0, sticky=_tk.NSEW)
        label_styles = _ttk.Label(wrapper, text="Styles")
        label_styles.grid(row=6, column=0, sticky=_tk.NSEW, pady=(6, 0))

        frame_styles_wrapper.grid(row=7, column=0, sticky=_tk.EW)

        label_people = _ttk.Label(wrapper, text="People")
        label_people.grid(row=8, column=0, sticky=_tk.NSEW, pady=(6, 0))

        frame_people_buttons = _ttk.Frame(wrapper)
        frame_people_buttons.grid(row=9, column=0, sticky=_tk.NSEW)

        button_no_people = _fkwidgets.toggle_button(
                frame_people_buttons,
                buttongroup="configure_people",
                text="None"
        )

        button_no_people.toggle(True)
        button_configure_people = _fkwidgets.toggle_button(
                frame_people_buttons,
                buttongroup="configure_people",
                text="One or More"
        )

        def open_people_dialog():
            if button_configure_people.toggled:
                self._show_people_preferences_dialog(wrapper)

        button_configure_people.bind("<<Selected>>", lambda e: open_people_dialog())

        button_no_people.pack(side=_tk.LEFT, expand=True, fill=_tk.X)
        button_configure_people.pack(side=_tk.LEFT, expand=True, fill=_tk.X)

        return wrapper

    def _show_people_preferences_dialog(self, master: _tk.Misc):
        class __PrefDialog(_tksimpledialog.Dialog):
            _button_ok: _tk.Button

            def __init__(self, parent) -> None:
                super().__init__(parent)

            def body(self, parent: _tk.Frame) -> _tk.Misc | None:
                self.resizable(None, None)

                parent.grid_columnconfigure(0, minsize=256, weight=0)

                label_no_people = _ttk.Label(parent, text="Number of People")
                label_no_people.grid(row=0, column=0, sticky=_tk.NSEW)

                no_of_people_values = ["One Person", "Two People", "Group of People"]
                frame_no_people_wrapper = _tk.Frame(parent)

                for i, no_people in enumerate(no_of_people_values):
                    btn = _fkwidgets.toggle_button(frame_no_people_wrapper, buttongroup="no_people", text=no_people)
                    btn.pack(side=_tk.LEFT, fill=_tk.X, expand=True)

                    if i == 0:
                        btn.toggle(True)

                frame_no_people_wrapper.grid(row=1, column=0, sticky=_tk.NSEW)

                label_age = _ttk.Label(parent, text="Age")
                label_age.grid(row=2, column=0, sticky=_tk.NSEW, pady=(6, 0))

                age_values = [
                    "Baby", "Child", "Teenager", "Young Adult",
                    "Adult", "Adults Only", "Mature Adult",
                    "Senior Adult"
                ]

                idx = 0
                frame_age_wrapper = _tk.Frame(parent)
                for row in range(3):
                    frame_row = _tk.Frame(frame_age_wrapper)
                    for column in range(3):
                        if idx >= len(age_values):
                            break

                        age_txt = age_values[idx]
                        idx += 1

                        btn = _fkwidgets.toggle_button(frame_row, text=age_txt)
                        btn.pack(side=_tk.LEFT, anchor=_tk.W, expand=True, fill=_tk.BOTH)

                    frame_row.pack(side=_tk.TOP, expand=True, fill=_tk.X)

                frame_age_wrapper.grid(row=3, column=0, sticky=_tk.NSEW)

                composition_values = [
                    "Candid", "Full Length",
                    "Head Shot", "Looking At Camera",
                    "Three Quarters", "Waist Up"
                ]

                label_compositions = _ttk.Label(parent, text="Composition")
                label_compositions.grid(row=4, column=0, sticky=_tk.NSEW, pady=(6, 0))

                frame_compositions_wrapper, composition_toggles = _fkwidgets.create_toggle_buttons_panel(
                        parent,
                        composition_values
                )

                frame_compositions_wrapper.grid(row=5, column=0, sticky=_tk.NSEW)

                ethnicity_values = [
                    "Black", "East Asian", "Middle Eastern", "Multiracial Group",
                    "Pacific Islander", "Southeast Asian", "White", "Hispanic/Latinx",
                    "Multiracial Person", "Native American/First Nation", "South Asian"
                ]

                frame_ethnicity_wrapper, ethnicity_toggles = _fkwidgets.create_toggle_buttons_panel(
                        parent,
                        ethnicity_values
                )

                label_ethnicity = _ttk.Label(parent, text="Ethnicity")
                label_ethnicity.grid(row=6, column=0, pady=(6, 0), sticky=_tk.NSEW)
                frame_ethnicity_wrapper.grid(row=7, column=0, sticky=_tk.NSEW)

                return None

            def buttonbox(self) -> None:
                frame = _ttk.Frame(self)

                self._button_ok = _ttk.Button(frame, text="OK", width=16, command=self.__on_ok_button)
                self._button_ok.grid(row=0, column=1, padx=(3, 0), pady=(0, 6))

                frame.pack(side=_tk.RIGHT, padx=6, pady=0)

            def __on_ok_button(self):
                self.destroy()

        __PrefDialog(master)

    @staticmethod
    def _normalize_alt_text(alt_text: str) -> str:
        tags_text = alt_text
        if " - " in alt_text and ("stock picture" in alt_text or "royalty-free" in alt_text):
            _alt_text = alt_text[:alt_text.rindex(" - ")].strip()
            _alt_text = _fkutils.normalize_tags(_alt_text)
            if len(_alt_text) > 0:
                tags_text = _alt_text

        return _fkutils.normalize_tags(tags_text)
