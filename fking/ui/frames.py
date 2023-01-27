import tkinter as _tk
import tkinter.filedialog
import tkinter.ttk as _ttk
from typing import Callable, Union

import fking.scrapers as _fkscrappers
import fking.ui.widgets as _fkwidgets


def create_primary_settings_frame(
        parent: _tk.Misc
) -> tuple[_tk.Frame, _tk.StringVar, _tk.StringVar, Callable[[Union[_tk.NORMAL, _tk.DISABLED]], None]]:
    wrapper = _ttk.Frame(parent)

    frame_terms, str_var_terms, set_state_terms = _fkwidgets.create_browse_widget_group(
            wrapper,
            dialog_fn=_tk.filedialog.askopenfilename,
            label_text="Query List",
            title="fking spaghetti v0.0.1 - Select a Search Query List",
            filetypes=[("Text documents", "*.txt")]
    )

    frame_download_dir, str_download_dir, set_state_download_dir = _fkwidgets.create_browse_widget_group(
            wrapper,
            dialog_fn=_tk.filedialog.askdirectory,
            label_text="Download Directory"
    )

    def set_state(state: Union[_tk.NORMAL, _tk.DISABLED]):
        set_state_terms(state)
        set_state_terms(state)

    frame_terms.pack(side=_tk.TOP, anchor=_tk.N, expand=True, fill=_tk.X, pady=3)
    frame_download_dir.pack(side=_tk.BOTTOM, anchor=_tk.S, expand=True, fill=_tk.X, pady=3)

    return wrapper, str_var_terms, str_download_dir, set_state


def create_progress_frame(
        parent: _tk.Misc
) -> tuple[_tk.Frame, Callable[[...], None], Callable[[...], None]]:
    wrapper = _ttk.Frame(parent)

    frame_image_download, \
        update_image_download = _fkwidgets.create_progress_widget_group(wrapper, "Image Downloads")

    frame_search_query, \
        update_search_query = _fkwidgets.create_progress_widget_group(wrapper, "Search Queries")

    frame_image_download.pack(side=_tk.TOP, expand=True, fill=_tk.X, pady=3)
    frame_search_query.pack(side=_tk.TOP, expand=True, fill=_tk.X, pady=3)

    return wrapper, update_image_download, update_search_query


def create_source_selector_frame(parent: _tk.Misc) -> tuple[_tk.Frame, _tk.StringVar]:
    wrapper = _ttk.Frame(parent)

    str_var_scraper = _tk.StringVar(wrapper)
    scraper_keys = list(_fkscrappers.get_all())

    label = _ttk.Label(wrapper, text="Source", justify=_tk.LEFT, anchor=_tk.W)
    combobox_source = _ttk.Combobox(
            wrapper,
            values=scraper_keys,
            justify=_tk.LEFT,
            state="readonly",
            textvariable=str_var_scraper
    )

    label.pack(side=_tk.TOP, anchor=_tk.W, expand=True, fill=_tk.X)
    combobox_source.pack(side=_tk.TOP, anchor=_tk.W, expand=True, fill=_tk.X)

    return wrapper, str_var_scraper
