import tkinter.ttk

_tk = tkinter.Tk()

_tk.title("fking spaghetti v0.0.1 - a fking bulk image downloader")
_tk.option_add("*tearOff", False)

_frame = tkinter.Frame(padx=6, pady=6)

_frame.pack(side=tkinter.TOP, expand=True, fill=tkinter.BOTH)

_combobox_search_term_list_select = tkinter.ttk.Combobox(_frame)
_combobox_search_term_list_select.configure(state="readonly")

_button_refresh_search_term_list = tkinter.Button(_frame, text="Refresh", width=10)
_button_browse_output_directory = tkinter.Button(_frame, text="Browse")

tkinter.Label(_frame, text="Download Destination", justify=tkinter.LEFT).grid(
        row=2,
        column=0,
        columnspan=2,
        sticky='w',
        pady=(6, 0)
)

_frame_textfield = tkinter.Frame(_frame, background="#a0a0a0", borderwidth=1)
_textfield_output_directory = tkinter.Entry(_frame_textfield, justify=tkinter.LEFT, relief=tkinter.FLAT, width=64)
_textfield_output_directory.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

_frame_textfield.grid(row=3, column=0, padx=(0, 3), sticky=tkinter.NSEW)
_button_browse_output_directory.grid(row=3, column=1, padx=(3, 0), sticky=tkinter.NSEW)

_progress_bar_download_queue = tkinter.ttk.Progressbar(_frame, orient=tkinter.HORIZONTAL)
_progress_bar_search_term_list = tkinter.ttk.Progressbar(_frame, orient=tkinter.HORIZONTAL)

tkinter.Label(_frame, text="Search Query List", justify=tkinter.LEFT).grid(row=0, column=0, columnspan=2, sticky='w')
_combobox_search_term_list_select.grid(row=1, column=0, padx=(0, 3), sticky=tkinter.NSEW)
_button_refresh_search_term_list.grid(row=1, column=1, padx=(3, 0), sticky=tkinter.NSEW)

tkinter.Label(_frame, text="Image Download Queue", justify=tkinter.LEFT).grid(
        row=4,
        column=0,
        columnspan=2,
        sticky='w',
        pady=(6, 0)
)

_progress_bar_download_queue.grid(row=5, column=0, columnspan=2, sticky=tkinter.NSEW)

tkinter.Label(_frame, text="Search Term Queue", justify=tkinter.LEFT).grid(
        row=6,
        column=0,
        columnspan=2,
        sticky='w'
)

_progress_bar_search_term_list.grid(row=7, column=0, columnspan=2, sticky=tkinter.NSEW)

_frame_action_buttons = tkinter.Frame(_frame)
_frame_action_buttons.grid(row=8, column=0, columnspan=2, sticky=tkinter.NSEW, pady=(18, 0))

_button_start = tkinter.Button(_frame_action_buttons, text="Start")
_button_start.pack(side=tkinter.RIGHT, expand=True, fill=tkinter.X)

_button_cancel = tkinter.Button(_frame_action_buttons, text="Cancel")
_button_cancel.pack(side=tkinter.LEFT, expand=True, fill=tkinter.X)

_spacer = tkinter.Frame(_frame_action_buttons)
_spacer.pack(side=tkinter.LEFT, padx=3)


def show_ui():
    _tk.mainloop()
