import datetime
import os.path
import tkinter as _tk
import tkinter.ttk as _ttk

import fking.ui
import fking.ui.frames as _fkframes
import fking.ui.widgets as _fkwidgets
import fking.utils as _fkutils


def show():
    tk = _tk.Tk()
    fking.ui.start_tkinter_event_bus(tk)

    tk_frame = _ttk.Frame(tk, padding=9)
    tk_frame.pack(side=_tk.TOP, fill=_tk.BOTH, expand=True)

    tk_frame.grid_columnconfigure(0, minsize=464, weight=1)

    #
    # Primary Frame
    # ===============
    frame_primary_settings, str_var_queries_list_path, \
        str_var_download_directory, set_state_primary_settings = _fkframes.create_primary_settings_frame(tk_frame)

    def update_ui_state():
        if str_var_queries_list_path and str_var_download_directory:
            set_state_primary_settings(_tk.NORMAL)
            button_start.configure(state=_tk.NORMAL)
            button_cancel.configure(state=_tk.DISABLED)
        else:
            set_state_primary_settings(_tk.DISABLED)
            button_start.configure(state=_tk.DISABLED)
            button_cancel.configure(state=_tk.DISABLED)

    def validate_download_directory(dirpath: str):
        if dirpath and os.path.exists(dirpath):
            if len(os.listdir(dirpath)) > 0:
                dt_now = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")
                dirpath = _fkutils.normalize_path(os.path.join(dirpath, f"spaghetti_{dt_now}"))
                str_var_download_directory.set(dirpath)

        update_ui_state()

    _fkwidgets.subscribe_to_tk_var(str_var_queries_list_path, lambda _: update_ui_state())
    _fkwidgets.subscribe_to_tk_var(str_var_download_directory, lambda dirpath: validate_download_directory(dirpath))

    frame_primary_settings.grid(row=0, column=0, sticky=_tk.NSEW, pady=(0, 3))
    # =================
    # End of Primary Frame
    #
    # Push All Content to Bottom on Resize
    tk_frame.grid_rowconfigure(1, minsize=0, weight=1)
    _ttk.Frame(tk_frame).grid(row=1, column=0, sticky=_tk.NSEW)
    # =================
    # End of Content Push
    #
    # Progress Frame
    # =================
    frame_progress, update_progress_image_downloads, \
        update_progress_search_queries = _fkframes.create_progress_frame(tk_frame)

    def increment_image_downloads(v: int = 1):
        pass

    def increment_image_downloads_total(v: int = 1):
        pass

    def increment_search_terms(v: int = 1):
        pass

    def increment_search_terms_total(v: int = 0):
        pass

    def reset_progress():
        update_progress_image_downloads(_fkwidgets.PROGRESSBAR_STOP)
        update_progress_search_queries(_fkwidgets.PROGRESSBAR_STOP)

    fking.ui.bind("<<DownloadTaskComplete>>", increment_image_downloads)
    fking.ui.bind("<<DownloadTaskAdded>>", increment_image_downloads_total)

    fking.ui.bind("<<SearchTermComplete>>", increment_search_terms)
    fking.ui.bind("<<SearchTermAdded>>", increment_search_terms_total)

    frame_progress.grid(row=2, column=0, sticky=_tk.NSEW, pady=3)
    # =================
    # End of Progress Frame
    #
    #
    # Scraper Controls
    # =================
    frame_scraper_controls = _ttk.Frame(tk_frame)
    button_cancel = _ttk.Button(frame_scraper_controls, text="Cancel")
    button_start = _ttk.Button(frame_scraper_controls, text="Start")

    button_cancel.pack(side=_tk.LEFT, anchor=_tk.W, fill=_tk.X, expand=True)
    button_start.pack(side=_tk.RIGHT, anchor=_tk.E, fill=_tk.X, expand=True)
    frame_scraper_controls.grid(row=3, column=0, sticky=_tk.NSEW, pady=(6, 0))
    # =================
    # End of Scraper Controls
    #
    #
    # Status Bar
    # =================

    tk.mainloop()
