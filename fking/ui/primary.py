import datetime
import os.path
import tkinter as _tk
import tkinter.ttk as _ttk
from typing import Union

import fking.app as _fkapp
import fking.scrapers as _fkscrapers
import fking.ui as _fkui
import fking.network as _fknetworks
import fking.ui.frames as _fkframes
import fking.ui.widgets as _fkwidgets
import fking.utils as _fkutils

AUTO = "auto"
START = "start"


def show():
    tk = _tk.Tk()
    tk.wm_maxsize(396, 4000)
    tk.wm_minsize(396, 339)
    tk.resizable(False, False)
    tk.wm_title("fking-spaghetti v0.0.2 - a bulk image downloader")

    _fkui.start_tkinter_event_bus(tk)

    tk_frame = _ttk.Frame(tk, padding=9)
    tk_frame.pack(side=_tk.TOP, fill=_tk.BOTH, expand=True)

    tk_frame.grid_columnconfigure(0, minsize=378, weight=1)

    #
    # Primary Frame
    # ===============
    frame_primary_settings, str_var_queries_list_path, \
        str_var_download_directory, set_state_primary_settings = _fkframes.create_primary_settings_frame(tk_frame)

    def update_ui_state(state: Union[_tk.NORMAL, _tk.DISABLED, AUTO, START] = AUTO):
        queries_list_path = str_var_queries_list_path.get()
        download_directory = str_var_download_directory.get()
        scraper_selected = str_var_source.get()

        if state == START:
            _fkwidgets.set_state(_tk.DISABLED, frame_source_selector)
            set_state_primary_settings(_tk.DISABLED)
            button_start.configure(state=_tk.DISABLED)
            button_cancel.configure(state=_tk.NORMAL)
        elif state == AUTO:
            _fkwidgets.set_state(_tk.NORMAL, frame_source_selector)
            if queries_list_path and download_directory and scraper_selected:
                set_state_primary_settings(_tk.NORMAL)
                button_start.configure(state=_tk.NORMAL)
                button_cancel.configure(state=_tk.DISABLED)
            else:
                set_state_primary_settings(_tk.NORMAL)
                button_start.configure(state=_tk.DISABLED)
                button_cancel.configure(state=_tk.DISABLED)
        else:
            set_state_primary_settings(state)
            button_start.configure(state=state)
            button_cancel.configure(state=state)
            _fkwidgets.set_state(state, frame_source_selector)

    def validate_download_directory(dirpath: str):
        if dirpath and os.path.exists(dirpath):
            if len(os.listdir(dirpath)) > 0:
                dt_now = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
                dirpath = _fkutils.normalize_path(os.path.join(dirpath, f"spaghetti_{dt_now}"))
                str_var_download_directory.set(dirpath)

        update_ui_state()

    _fkwidgets.subscribe_to_tk_var(str_var_queries_list_path, lambda _: update_ui_state())
    _fkwidgets.subscribe_to_tk_var(str_var_download_directory, lambda dirpath: validate_download_directory(dirpath))

    frame_primary_settings.grid(row=0, column=0, sticky=_tk.NSEW)
    _ttk.Separator(tk_frame, orient=_tk.HORIZONTAL).grid(row=1, column=0, sticky=_tk.NSEW, pady=9)
    # =================
    # End of Primary Frame
    #
    # Source selector
    frame_source_selector, str_var_source = _fkframes.create_source_selector_frame(tk_frame)
    frame_source_settings = _ttk.Frame(tk_frame)

    def show_scraper_settings(key: str):
        nonlocal frame_source_settings

        if key == _fkapp.context.active_scraper_name:
            return

        if _fkapp.context.active_scraper is not None:
            print("Forgetting source settings grid")
            frame_source_settings.destroy()

            frame_source_settings = _ttk.Frame(tk_frame)
            frame_source_settings.grid(row=3, column=0, sticky=_tk.NSEW)

        next_scraper = _fkscrapers.get(key)
        _fkapp.context.active_scraper = next_scraper

        tkinter_ui = next_scraper.tkinter_settings(frame_source_settings)

        if tkinter_ui:
            _ttk.Frame(frame_source_settings).pack(side=_tk.TOP, expand=True, fill=_tk.X, pady=(6, 0))
            _fkwidgets.section_divider(frame_source_settings, pady=(0, 3)).pack(side=_tk.TOP, expand=True,
                                                                                fill=_tk.BOTH)
            # _ttk.Separator(frame_source_settings, orient=_tk.HORIZONTAL).pack(side=_tk.TOP, expand=True, fill=_tk.X)
            _ttk.Frame(frame_source_settings).pack(side=_tk.TOP, expand=True, fill=_tk.X, pady=(0, 3))
            tkinter_ui.pack(side=_tk.TOP, expand=True, fill=_tk.BOTH, pady=3)
        update_ui_state()

    _fkwidgets.subscribe_to_tk_var(str_var_source, lambda key: show_scraper_settings(key))

    frame_source_selector.grid(row=2, column=0, sticky=_tk.NSEW, pady=(0, 6))
    frame_source_settings.grid(row=3, column=0, sticky=_tk.NSEW)
    # End of source selector
    #
    # Push All Content to Bottom on Resize
    tk_frame.grid_rowconfigure(4, minsize=0, weight=1)
    _ttk.Frame(tk_frame).grid(row=4, column=0, sticky=_tk.NSEW)
    _ttk.Separator(tk_frame, orient=_tk.HORIZONTAL).grid(row=5, column=0, sticky=_tk.NSEW, pady=6)
    # =================
    # End of Content Push
    #
    # Progress Frame
    # =================
    frame_progress, \
        set_image_downloads, \
        increment_image_downloads, increment_image_download_totals, \
        set_search_terms, \
        increment_search_terms, increment_search_term_totals = _fkframes.create_progress_frame(tk_frame)

    def reset_progress():
        set_search_terms(_fkwidgets.RESET)
        set_image_downloads(_fkwidgets.RESET)

    _fkui.bind(_fkui.EVENT_DOWNLOAD_TASK_ADDED, lambda *args, **kwargs: increment_image_download_totals(1))
    _fkui.bind(_fkui.EVENT_DOWNLOAD_TASK_COMPLETE, lambda *args, **kwargs: increment_image_downloads(1))

    _fkui.bind(_fkui.EVENT_SEARCH_TERM_ADDED, lambda *args, **kwargs: increment_search_term_totals(1))
    _fkui.bind(_fkui.EVENT_SEARCH_TERM_COMPLETE, lambda *args, **kwargs: increment_search_terms(1))

    frame_progress.grid(row=6, column=0, sticky=_tk.NSEW, pady=0)
    # =================
    # End of Progress Frame
    #
    #
    # Status Bar
    # =================
    str_status_text = _tk.StringVar(tk_frame, value="Ready")
    label_status_text = _ttk.Label(tk_frame, textvariable=str_status_text, justify=_tk.LEFT, anchor=_tk.W)
    label_status_text.grid(row=7, column=0, sticky=_tk.EW, pady=(3, 0))

    _fkui.bind(_fkui.EVENT_STATUS_BAR_TEXT, lambda *args, **kwargs: str_status_text.set(kwargs["text"]))
    # =================
    # End of Status Bar
    #
    #
    # Scraper Controls
    # =================
    frame_scraper_controls = _ttk.Frame(tk_frame)
    button_cancel = _ttk.Button(frame_scraper_controls, text="Cancel")
    button_start = _ttk.Button(frame_scraper_controls, text="Start")

    button_cancel.pack(side=_tk.LEFT, anchor=_tk.W, fill=_tk.X, expand=True)
    button_start.pack(side=_tk.RIGHT, anchor=_tk.E, fill=_tk.X, expand=True)

    def start_scraper():
        reset_progress()

        queries_path = str_var_queries_list_path.get()
        download_path = str_var_download_directory.get()

        _fkapp.context.query_list_path = queries_path
        _fkapp.context.download_directory = download_path

        _fkapp.start_scraper()

    def cancel_scrape():
        str_status_text.set("Cancelling scraper... stopping threads...")
        _fkapp.stop_scraper(True)

    button_start.bind("<Button-1>", lambda e: start_scraper())
    button_cancel.bind("<Button-1>", lambda e: cancel_scrape())
    frame_scraper_controls.grid(row=8, column=0, sticky=_tk.NSEW, pady=(6, 0))

    # =================
    # End of Scraper Controls
    #
    #
    # Scraper events
    # =================

    def scraper_started():
        update_ui_state(START)
        _fknetworks.load_proxies()
        if frame_source_settings:
            _fkwidgets.set_state(_tk.DISABLED, frame_source_settings)

    def scraper_completed():
        update_ui_state()
        if frame_source_settings:
            _fkwidgets.set_state(_tk.NORMAL, frame_source_settings)

    _fkui.bind(_fkui.SCRAPER_STARTED, lambda *args, **kwargs: scraper_started())
    _fkui.bind(_fkui.SCRAPER_COMPLETE, lambda *args, **kwargs: scraper_completed())

    update_ui_state()
    tk.mainloop()
