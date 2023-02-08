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
    ImageTask as _ImageTask, ScraperResult as _ScraperResult


class GettyImages(_IScraper):
    _sort_by_values = ["Best Match", "Newest", "Most Popular"]
    _color_and_mood_values = ["All", "Black & White", "Bold", "Cool", "Dramatic", "Natural", "Vivid", "Warm"]
    _orientation_values = ["Vertical", "Horizontal", "Square", "Panoramic Horizontal", "Panoramic Vertical"]
    _style_values = [
        "Abstract", "Close-up", "Cut Out",
        "Copy Space", "Full Frame", "Macro",
        "Portrait", "Sparse", "Still Life"
    ]

    _no_people_dict = {
        "One Person": "one",
        "Two People": "two",
        "Group of People": "group"
    }

    _no_of_people_values = ["One Person", "Two People", "Group of People"]

    _ethnicity_dict = {
        "Black": "black",
        "East Asian": "eastasian",
        "Middle Eastern": "middleeastern",
        "Multiracial Group": "multiethnicgroup",
        "Pacific Islander": "pacificislander",
        "Southeast Asian": "southeastasian",
        "White": "caucasian",
        "Hispanic/Latinx": "hispaniclantino",
        "Multiracial Person": "mixedraceperson",
        "Native American/First Nation": "nativeamericanfirstnations",
        "South Asian": "southasian"
    }

    _sort_by: str = _sort_by_values[2]
    _color_and_mood: str = _color_and_mood_values[0]

    _styles: list[str] = []
    _orientations: list[str] = []

    _search_people: bool = False
    _no_people: str = _no_of_people_values[0]
    _age_people: list[str] = []
    _compositions: list[str] = []
    _ethnicities: list[str] = []

    def __init__(self) -> None:
        super().__init__("Getty Images")

    def query(self, search_query: str, _page: int = 1) -> _ScraperResult:
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
                return _ScraperResult([], False)

            image_tasks: list[_ImageTask] = []
            gallery_images = document_soup.find_all("img", {"class": "MosaicAsset-module__thumb___yvFP5"})

            def is_full() -> bool:
                return len(image_tasks) >= _fkapp.context.max_images_per_term

            if gallery_images:
                query_dirname = _fkutils.sanitize_dirname(search_query)

                for gallery_image in gallery_images:
                    if is_full():
                        return _ScraperResult(image_tasks, False)

                    image_url = gallery_image["src"]
                    image_alt_text = gallery_image["alt"]

                    caption_text = self._normalize_alt_text(image_alt_text)
                    image_task = _ImageTask(search_query, query_dirname, image_url, caption_text)
                    image_tasks.append(image_task)

            next_button_class = "PaginationRow-module__button___QQbMu PaginationRow-module__nextButton___gH3HZ"
            next_button = document_soup.find("button", {"class": next_button_class})

            has_next = next_button and not is_full()
            return _ScraperResult(image_tasks, has_next)

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

        if color_and_mood != "all":
            url += f"&mood={color_and_mood}"

        compositions = []
        if len(self._orientations) > 0:
            url += f"&orientations={_fkutils.url_encode(','.join([o.replace(' ', '').lower() for o in self._orientations]))}"
        if len(self._styles) > 0:
            compositions.extend(self._styles)

        if self._search_people:
            url += f"&numberofpeople={self._no_people_dict[self._no_people]}"
            if len(self._age_people) > 0:
                url += f"&ageofpeople={_fkutils.url_encode(','.join([it.replace(' ', '').lower() for it in self._age_people]))}"
            if len(self._compositions) > 0:
                compositions.extend(self._compositions)
            if len(self._ethnicities) > 0:
                ethnicities = []
                for e in self._ethnicities:
                    ethnicities.append(self._ethnicity_dict[e])
                url += f"&ethnicity={_fkutils.url_encode(','.join(ethnicities))}"
        else:
            url += "&numberofpeople=none"

        if len(compositions) > 0:
            url += f"&compositions={_fkutils.url_encode(','.join([c.replace(' ', '').replace('-', '').lower() for c in compositions]))}"

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

        frame_orientations_wrapper, \
            orientation_toggles, = _fkwidgets.create_toggle_buttons_panel(wrapper, self._orientation_values)
        for o_toggle in orientation_toggles:
            o_toggle.bind("<<Selected>>", lambda e, key=o_toggle.cget("text"): self._orientations.append(key))
            o_toggle.bind("<<Deselected>>", lambda e, key=o_toggle.cget("text"): self._orientations.remove(key))

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
        for style_toggle in styles_toggles:
            style_toggle.bind("<<Selected>>", lambda e, key=style_toggle.cget("text"): self._styles.append(key))
            style_toggle.bind("<<Deselected>>", lambda e, key=style_toggle.cget("text"): self._styles.remove(key))

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

        def enable_people_search():
            self._search_people = True
            self._show_people_preferences_dialog(wrapper)

        def disable_people_search():
            self._search_people = False
            self._no_people = self._no_of_people_values[0]
            self._age_people.clear()
            self._compositions.clear()
            self._ethnicities.clear()

        button_configure_people.bind("<<Selected>>", lambda e: enable_people_search())
        button_configure_people.bind("<<Deselected>>", lambda e: disable_people_search())

        button_no_people.pack(side=_tk.LEFT, expand=True, fill=_tk.X)
        button_configure_people.pack(side=_tk.LEFT, expand=True, fill=_tk.X)

        return wrapper

    def _show_people_preferences_dialog(self, master: _tk.Misc):
        _PeoplePreferenceDialog(master, self)

    @staticmethod
    def _normalize_alt_text(alt_text: str) -> str:
        tags_text = alt_text
        if " - " in alt_text and ("stock picture" in alt_text or "royalty-free" in alt_text):
            _alt_text = alt_text[:alt_text.rindex(" - ")].strip()
            _alt_text = _fkutils.normalize_tags(_alt_text)
            if len(_alt_text) > 0:
                tags_text = _alt_text

        return _fkutils.normalize_tags(tags_text)


# noinspection PyProtectedMember
class _PeoplePreferenceDialog(_tksimpledialog.Dialog):
    _button_ok: _tk.Button

    def __init__(self, parent, getty: GettyImages) -> None:
        self.getty = getty
        super().__init__(parent)

    def body(self, parent: _tk.Frame) -> Optional[_tk.Misc]:
        self.resizable(None, None)

        parent.grid_columnconfigure(0, minsize=256, weight=0)

        label_no_people = _ttk.Label(parent, text="Number of People")
        label_no_people.grid(row=0, column=0, sticky=_tk.NSEW)

        frame_no_people_wrapper = _tk.Frame(parent)

        def update_no_people(n_people: str):
            self.getty._no_people = n_people

        no_peoples = list(self.getty._no_people_dict.keys())
        for i, no_people in enumerate(no_peoples):
            btn = _fkwidgets.toggle_button(frame_no_people_wrapper, buttongroup="no_people", text=no_people)
            btn.pack(side=_tk.LEFT, fill=_tk.X, expand=True)
            btn.bind("<<Selected>>", lambda e, n_people=no_people: update_no_people(n_people))

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

        frame_age_wrapper, age_toggles = _fkwidgets.create_toggle_buttons_panel(parent, age_values)
        for age_toggle in age_toggles:
            age_toggle.bind("<<Selected>>", lambda e, key=age_toggle.cget("text"): self.getty._age_people.append(key))
            age_toggle.bind("<<Deselected>>", lambda e, key=age_toggle.cget("text"): self.getty._age_people.remove(key))

        frame_age_wrapper.grid(row=3, column=0, sticky=_tk.NSEW)

        composition_values = [
            "Candid", "Full Length",
            "Head Shot", "Looking At Camera",
            "Three Quarters", "Waist Up"
        ]

        label_compositions = _ttk.Label(parent, text="Composition")
        label_compositions.grid(row=4, column=0, sticky=_tk.NSEW, pady=(6, 0))

        frame_comp_wrapper, composition_toggles = _fkwidgets.create_toggle_buttons_panel(parent, composition_values)
        for comp_toggle in composition_toggles:
            comp_toggle.bind(
                "<<Selected>>",
                lambda e, key=comp_toggle.cget("text"): self.getty._compositions.append(key)
            )

            comp_toggle.bind(
                "<<Deselected>>",
                lambda e, key=comp_toggle.cget("text"): self.getty._compositions.remove(key)
            )

        frame_comp_wrapper.grid(row=5, column=0, sticky=_tk.NSEW)

        ethnicity_values = list(self.getty._ethnicity_dict.keys())

        label_ethnicity = _ttk.Label(parent, text="Ethnicity")
        label_ethnicity.grid(row=6, column=0, pady=(6, 0), sticky=_tk.NSEW)

        frame_ethnicity_wrapper, ethnicity_toggles = _fkwidgets.create_toggle_buttons_panel(parent, ethnicity_values)
        for ethnicity_toggle in ethnicity_toggles:
            ethnicity_toggle.bind(
                "<<Selected>>",
                lambda e, key=ethnicity_toggle.cget("text"): self.getty._ethnicities.append(key)
            )

            ethnicity_toggle.bind(
                "<<Deselected>>",
                lambda e, key=ethnicity_toggle.cget("text"): self.getty._ethnicities.remove(key)
            )

        frame_ethnicity_wrapper.grid(row=7, column=0, sticky=_tk.NSEW)

        return None

    def buttonbox(self) -> None:
        frame = _ttk.Frame(self)

        self._button_ok = _ttk.Button(frame, text="OK", width=16, command=self.__on_ok_button)
        self._button_ok.grid(row=0, column=1, padx=(3, 0), pady=(12, 6))

        frame.pack(side=_tk.RIGHT, padx=6, pady=0)

    def __on_ok_button(self):
        print(self.getty.generate_query_url("kitten", 1))
        self.destroy()
