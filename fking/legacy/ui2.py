import math
import tkinter.ttk
from typing import Callable

import fking.legacy.widgets


class _SpaghettiComponents:
    _string_var_search_queries_path: tkinter.StringVar
    _string_var_download_directory_path: tkinter.StringVar

    _entry_search_queries_path: tkinter.ttk.Entry
    _entry_download_directory_path: tkinter.ttk.Entry

    _frame_search_queries_path: tkinter.Frame
    _frame_download_directory_path: tkinter.Frame

    _button_browse_queries_path: tkinter.ttk.Button
    _button_browse_download_directory: tkinter.ttk.Button

    _string_var_image_downloads: tkinter.StringVar
    _string_var_search_queries: tkinter.StringVar

    _frame_image_downloads: tkinter.Frame
    _frame_search_queries: tkinter.Frame

    _progressbar_image_downloads: tkinter.ttk.Progressbar
    _progressbar_search_queries: tkinter.ttk.Progressbar

    _frame_status_text: tkinter.Frame
    _frame_scraper_actions: tkinter.Frame

    _int_var_download_threads: tkinter.IntVar
    _scale_download_threads: tkinter.ttk.Scale
    _spinbox_download_threads: tkinter.ttk.Spinbox

    _frame_download_threads: tkinter.Frame

    _frame_getty_sort_by: tkinter.Frame
    _combobox_getty_sort_by: tkinter.ttk.Combobox

    _frame_getty_color_and_mood: tkinter.Frame
    _combobox_getty_color_and_mood: tkinter.ttk.Combobox

    _button_ok: tkinter.ttk.Button
    _button_cancel: tkinter.ttk.Button

    def initialize_components(self, root: tkinter.Tk):
        frame = tkinter.Frame(root, padx=6, pady=6)
        frame.grid_columnconfigure(0, weight=1)

        self._string_var_search_queries_path = tkinter.StringVar()
        self._string_var_download_directory_path = tkinter.StringVar()

        self._frame_search_queries_path = tkinter.Frame(frame)
        self._frame_download_directory_path = tkinter.Frame(frame)

        self._entry_search_queries_path = tkinter.ttk.Entry(self._frame_search_queries_path, justify=tkinter.LEFT,
                                                            textvariable=self._string_var_search_queries_path,
                                                            state=tkinter.NORMAL, width=48)

        self._entry_download_directory_path = tkinter.ttk.Entry(self._frame_download_directory_path,
                                                                justify=tkinter.LEFT,
                                                                textvariable=self._string_var_download_directory_path,
                                                                state=tkinter.NORMAL, width=48)

        self._button_browse_queries_path = tkinter.ttk.Button(self._frame_search_queries_path, text="Browse", width=10)
        self._button_browse_download_directory = tkinter.ttk.Button(self._frame_download_directory_path, text="Browse",
                                                                    width=10)

        self._string_var_image_downloads = tkinter.StringVar()
        self._string_var_search_queries = tkinter.StringVar()

        self._progressbar_image_downloads = tkinter.ttk.Progressbar(frame, orient=tkinter.HORIZONTAL)
        self._progressbar_search_queries = tkinter.ttk.Progressbar(frame, orient=tkinter.HORIZONTAL)

        self._int_var_download_threads = tkinter.IntVar()
        self._int_var_download_threads.set(10)

        self._frame_download_threads = tkinter.Frame(frame)
        self._scale_download_threads = tkinter.ttk.Scale(self._frame_download_threads, from_=1, to=20, value=10,
                                                         orient=tkinter.HORIZONTAL)

        self._frame_getty_sort_by = tkinter.Frame(frame)

        sort_by = ["Best Match", "Newest", "Most Popular"]
        self._combobox_getty_sort_by = tkinter.ttk.Combobox(frame, values=sort_by, state="readonly")

        self._frame_getty_color_and_mood = tkinter.Frame(frame)

        color_and_mood = ["All", "Warm", "Cool", "Vivid", "Natural", "Bold", "Dramatic", "Black & White"]
        self._combobox_getty_color_and_mood = tkinter.ttk.Combobox(
                frame,
                values=color_and_mood,
                state="readonly"
        )

        self._combobox_getty_sort_by.current(0)
        self._combobox_getty_color_and_mood.current(0)

        self._button_cancel = tkinter.ttk.Button(frame)
        self._button_ok = tkinter.ttk.Button(frame)

        self.__initialize_layout(frame)
        frame.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

    def __initialize_layout(self, frame: tkinter.Frame):
        self.__layout_path_widgets(frame)
        self.__layout_pref_widgets(frame)

        tkinter.ttk.Separator(
                frame,
                orient=tkinter.HORIZONTAL
        ).grid(row=6, column=0, sticky=tkinter.NSEW, pady=(9, 3))

        test = [
            "Vertical",
            "Horizontal",
            "Square",
            "Panoramic Horizontal",
            "Panoramic Vertical"
        ]

        test_frame = tkinter.Frame(frame, background='blue')
        test_label = tkinter.Text(test_frame, relief=tkinter.FLAT, wrap=tkinter.WORD)
        test_label.pack(anchor=tkinter.CENTER)
        test_label.configure(
                state=tkinter.DISABLED,
                cursor="arrow",
                background=frame.cget("background"),
                selectbackground=frame.cget("background"),
                pady=0, padx=0
        )

        for t in test:
            test_label.window_create(tkinter.INSERT, window=fking.legacy.widgets.toggle_button(test_label, text=t))

        test_frame.grid(row=7, column=0, sticky=tkinter.NSEW)
        # self.__layout_getty_widgets(frame)

    def __layout_path_widgets(self, frame: tkinter.Frame):
        tkinter.ttk.Label(frame, text="Search Query List", justify=tkinter.LEFT).grid(row=0, column=0, sticky=tkinter.W)
        self._frame_search_queries_path.grid(row=1, column=0, sticky=tkinter.NSEW)
        self._entry_search_queries_path.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        fking.legacy.widgets.x_spacer(self._frame_search_queries_path, 3).pack(side=tkinter.LEFT)
        self._button_browse_queries_path.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=True)

        fking.legacy.widgets.y_spacer(frame, 3).grid(row=2, column=0)

        tkinter.ttk.Label(frame, text="Download Location", justify=tkinter.LEFT).grid(row=3, column=0, sticky=tkinter.W)
        self._frame_download_directory_path.grid(row=4, column=0, sticky=tkinter.NSEW)
        self._entry_download_directory_path.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        fking.legacy.widgets.x_spacer(self._frame_download_directory_path, 3).pack(side=tkinter.LEFT)
        self._button_browse_download_directory.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=True)

    def __layout_pref_widgets(self, frame: tkinter.Frame):
        self._frame_download_threads.grid(row=5, column=0, sticky=tkinter.NSEW, pady=(6, 0))

        frame_download_threads_label = tkinter.Frame(self._frame_download_threads)
        tkinter.ttk.Label(
                frame_download_threads_label,
                text="Download Threads:",
                justify=tkinter.LEFT,
                anchor=tkinter.W
        ).pack(side=tkinter.LEFT)
        tkinter.ttk.Label(
                frame_download_threads_label,
                textvariable=self._int_var_download_threads,
                justify=tkinter.LEFT,
                anchor=tkinter.W
        ).pack(side=tkinter.LEFT)
        frame_download_threads_label.pack(side=tkinter.TOP, expand=True, fill=tkinter.BOTH)
        tkinter.ttk.Label(
                self._frame_download_threads,
                text="1",
                justify=tkinter.LEFT
        ).pack(side=tkinter.LEFT, expand=False, fill=tkinter.Y, padx=6)
        tkinter.ttk.Label(
                self._frame_download_threads,
                text="20",
                justify=tkinter.RIGHT
        ).pack(side=tkinter.RIGHT, expand=False, fill=tkinter.Y, padx=6)
        self._scale_download_threads.pack(side=tkinter.BOTTOM, expand=True, fill=tkinter.X)

    def __layout_getty_widgets(self, frame: tkinter.Frame):
        tkinter.ttk.Label(
                frame,
                text="Sorty By",
                justify=tkinter.LEFT,
                anchor=tkinter.W
        ).grid(row=7, column=0, sticky=tkinter.W)

        self._combobox_getty_sort_by.grid(row=8, column=0, sticky=tkinter.NSEW)

        tkinter.ttk.Label(
                frame,
                text="Color & Mood",
                justify=tkinter.LEFT,
                anchor=tkinter.W
        ).grid(row=9, column=0, sticky=tkinter.W, pady=(6, 0))
        self._combobox_getty_color_and_mood.grid(row=10, column=0, sticky=tkinter.NSEW)

        tkinter.ttk.Separator(frame, orient=tkinter.HORIZONTAL).grid(row=11, column=0, sticky=tkinter.NSEW, pady=(9, 6))

        _SpaghettiComponents.__init_centered_toggle_buttons(
                frame,
                [
                    "Vertical",
                    "Horizontal",
                    "Square",
                    "Panoramic Horizontal",
                    "Panoramic Vertical"
                ]
        ).grid(row=12, column=0, sticky=tkinter.NSEW)

        tkinter.ttk.Separator(frame, orient=tkinter.HORIZONTAL).grid(row=13, column=0, sticky=tkinter.NSEW, pady=(9, 6))

        _SpaghettiComponents.__init_centered_toggle_buttons(
                frame,
                [
                    "Abstract", "Portrait", "Close-up", "Sparse",
                    "Cut Out", "Full Frame", "Copy Space", "Macro",
                    "Still Life"
                ]
        ).grid(row=14, column=0, sticky=tkinter.NSEW)

    @staticmethod
    def __init_centered_toggle_buttons(
            frame: tkinter.Widget,
            labels: list[str],
            target: Callable[[tkinter.Event, bool], None] = None
    ) -> tkinter.Frame:
        o_idx = 0

        columns = math.ceil(math.sqrt(len(labels)))
        rows = math.ceil(len(labels) / columns)

        frame_buttons = tkinter.Frame(frame)
        frame_buttons.grid_columnconfigure(0, weight=1)
        frame_buttons.grid_columnconfigure(2, weight=1)

        # frame_orientation_buttons.grid(row=10, column=0, sticky=tkinter.NSEW)

        for row in range(rows):
            wrapper = tkinter.Frame(frame_buttons)
            wrapper.grid_columnconfigure(0, weight=1)
            wrapper.grid_columnconfigure(2, weight=1)

            wrapper.grid(row=row, column=1, sticky=tkinter.NSEW)

            center_wrapper = tkinter.Frame(wrapper)
            center_wrapper.grid(row=0, column=1)

            for col in range(columns):
                if o_idx >= len(labels):
                    break
                fking.legacy.widgets.toggle_button(
                        center_wrapper,
                        text=labels[o_idx],
                        target=target
                ).pack(side=tkinter.LEFT, anchor=tkinter.CENTER, fill=tkinter.BOTH, expand=True)
                o_idx += 1

        return frame_buttons


components = _SpaghettiComponents()
