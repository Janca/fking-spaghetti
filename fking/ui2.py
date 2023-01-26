import tkinter.ttk

import fking.widgets


class _SpaghettiComponents:
    _string_var_search_queries_path: tkinter.StringVar
    _string_var_download_directory_path: tkinter.StringVar

    _entry_search_queries_path: tkinter.Entry
    _entry_download_directory_path: tkinter.Entry

    _frame_search_queries_path: tkinter.Frame
    _frame_download_directory_path: tkinter.Frame

    _button_browse_queries_path: tkinter.Button
    _button_browse_download_directory: tkinter.Button

    _string_var_image_downloads: tkinter.StringVar
    _string_var_search_queries: tkinter.StringVar

    _frame_image_downloads: tkinter.Frame
    _frame_search_queries: tkinter.Frame

    _progressbar_image_downloads: tkinter.ttk.Progressbar
    _progressbar_search_queries: tkinter.ttk.Progressbar

    _frame_status_text: tkinter.Frame
    _frame_scraper_actions: tkinter.Frame

    _button_ok: tkinter.Button
    _button_cancel: tkinter.Button

    def initialize_components(self, root: tkinter.Tk):
        frame = tkinter.Frame(root, padx=6, pady=6)

        self._string_var_search_queries_path = tkinter.StringVar()
        self._string_var_download_directory_path = tkinter.StringVar()

        self._frame_search_queries_path = tkinter.Frame(frame)
        self._frame_download_directory_path = tkinter.Frame(frame)

        self._entry_search_queries_path = tkinter.Entry(self._frame_search_queries_path, justify=tkinter.LEFT,
                                                        textvariable=self._string_var_search_queries_path,
                                                        state="readonly", width=64)

        self._entry_download_directory_path = tkinter.Entry(self._frame_download_directory_path, justify=tkinter.LEFT,
                                                            textvariable=self._string_var_download_directory_path,
                                                            state="readonly", width=64)

        self._button_browse_queries_path = tkinter.Button(self._frame_search_queries_path, text="Browse", width=10)
        self._button_browse_download_directory = tkinter.Button(self._frame_download_directory_path, text="Browse",
                                                                width=10)

        self._string_var_image_downloads = tkinter.StringVar()
        self._string_var_search_queries = tkinter.StringVar()

        self._progressbar_image_downloads = tkinter.ttk.Progressbar(frame, orient=tkinter.HORIZONTAL)
        self._progressbar_search_queries = tkinter.ttk.Progressbar(frame, orient=tkinter.HORIZONTAL)

        self._button_cancel = tkinter.Button(frame)
        self._button_ok = tkinter.Button(frame)

        self.__initialize_layout(frame)
        frame.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

    def __initialize_layout(self, frame: tkinter.Frame):
        self.__layout_path_widgets(frame)
        self.__section(frame)

    def __layout_path_widgets(self, frame: tkinter.Frame):
        tkinter.Label(frame, text="Search Query List", justify=tkinter.LEFT).grid(row=0, column=0, sticky=tkinter.W)
        self._frame_search_queries_path.grid(row=1, column=0, sticky=tkinter.NSEW)
        self._entry_search_queries_path.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        fking.widgets.x_spacer(self._frame_search_queries_path, 3).pack(side=tkinter.LEFT)
        self._button_browse_queries_path.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=True)

        fking.widgets.y_spacer(frame, 3).grid(row=2, column=0)

        tkinter.Label(frame, text="Download Location", justify=tkinter.LEFT).grid(row=3, column=0, sticky=tkinter.W)
        self._frame_download_directory_path.grid(row=4, column=0, sticky=tkinter.NSEW)
        self._entry_download_directory_path.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        fking.widgets.x_spacer(self._frame_download_directory_path, 3).pack(side=tkinter.LEFT)
        self._button_browse_download_directory.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=True)

    def __section(self, frame: tkinter.Frame):
        fking.widgets.y_spacer(frame, 6).grid(row=5, column=0)
        tkinter.ttk.Separator(frame, orient=tkinter.HORIZONTAL).grid(row=6, column=0, sticky=tkinter.NSEW)
        fking.widgets.y_spacer(frame, 6).grid(row=5, column=0)


components = _SpaghettiComponents()
