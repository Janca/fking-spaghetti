import os
import sys
import threading
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk
from typing import Optional

import fking.context
import fking.queues
import fking.scraper
import fking.utils

from fking.context import context

_tk = tkinter.Tk()

_tk.title("fking spaghetti v0.0.1 - a fking bulk image downloader")
_tk.option_add("*tearOff", False)

_frame = tkinter.Frame(padx=6, pady=6)
_frame.pack(side=tkinter.TOP, expand=True, fill=tkinter.BOTH)

_is_busy = False
_scraping_thread: Optional[threading.Thread] = None


def __update_ui_state(busy: bool = False):
    state = tkinter.DISABLED

    if context.is_ready and not busy:
        state = tkinter.NORMAL

    if busy:
        _button_browse_search_term_list.configure(state=tkinter.DISABLED)
        _button_browse_output_directory.configure(state=tkinter.DISABLED)
        _button_cancel.configure(state=tkinter.NORMAL)
    else:
        _button_browse_search_term_list.configure(state=tkinter.NORMAL)
        _button_browse_output_directory.configure(state=tkinter.NORMAL)
        _button_cancel.configure(state=tkinter.DISABLED)

    _button_start.configure(state=state)


def __create_directories():
    os.makedirs(context.output_directory, exist_ok=True)
    os.makedirs(context.output_matching_captions, exist_ok=True)
    os.makedirs(context.output_mismatched_captions, exist_ok=True)
    os.makedirs(context.output_focals, exist_ok=True)


def __set_entry_text(entry: tkinter.Entry, text: str):
    state_before = entry.cget("state")
    entry.configure(state=tkinter.NORMAL)
    entry.delete(0, tkinter.END)
    entry.insert(tkinter.END, text)
    entry.xview_scroll(1, tkinter.PAGES)
    entry.configure(state=state_before)


def __set_progress(progress_bar: tkinter.ttk.Progressbar, value: int, max_value: int = -1):
    if value == -2:
        progress_bar.stop()

    elif value < 0:
        progress_bar["mode"] = "indeterminate"
        progress_bar["value"] = 0
        progress_bar["maximum"] = 100
        progress_bar.start()

    else:
        progress_bar.stop()
        progress_bar["mode"] = "determinate"
        progress_bar["value"] = value
        progress_bar["maximum"] = max_value


def __on_browse_output_directory():
    __set_status_text("Browsing for output directory...")
    dst_directory = tkinter.filedialog.askdirectory(title="fking spaghetti v0.0.1 - Select an Output Directory")
    if dst_directory:
        existing_files = os.listdir(dst_directory)
        if existing_files:
            dst_directory = os.path.join(dst_directory, "spaghetti_output")

        dst_directory = fking.utils.normalize_path(dst_directory)

        __set_entry_text(_textfield_output_directory, dst_directory)
        context.update_directories(dst_directory)
        __update_ui_state()

    __set_status_text("Ready")


def __on_browse_search_terms_list():
    __set_status_text("Browsing for search term list...")
    search_terms_path = tkinter.filedialog.askopenfilename(
            defaultextension=".txt",
            title="fking spaghetti v0.0.1 - Select a Search Term List",
            filetypes=[("Text documents", "*.txt")]
    )

    __set_status_text("Loading search term list...")

    if search_terms_path:
        context.search_terms_path = fking.utils.normalize_path(search_terms_path)
        __set_entry_text(_textfield_input_search_terms, search_terms_path)

        with open(search_terms_path, 'r') as f:
            terms = f.read().splitlines()

            search_terms = []
            for term in terms:
                t = term.strip()
                if t not in search_terms:
                    search_terms.append(t)

            context.search_terms = search_terms

    __set_status_text(f"Ready... Loaded '{len(search_terms)}' search queries...")


def __on_button_start():
    global _scraping_thread

    if not context.is_ready:
        return

    if _scraping_thread is not None and _scraping_thread.is_alive():
        return

    def do_scrape():
        __update_ui_state(True)
        __set_status_text("Preparing search...")

        context.reset(True)

        __do_status_bar_updates()
        fking.queues.start_image_download_threads()

        for i, term in enumerate(context.search_terms, start=1):
            if context.interrupted:
                break

            __set_status_text(f"Searching '{term}'...")

            _search_term_status_var.set(f"{i}/{context.search_terms_length}")
            __set_progress(_progress_bar_search_term_list, i, context.search_terms_length)

            fking.scraper.scrape_search_term(term)

        context.scraper_busy = False
        if not context.interrupted:
            __set_status_text("Searching complete... waiting on downloads")
            fking.queues.wait_on_image_download_threads()

            __set_status_text("Ready")
            __update_ui_state(False)

    _scraping_thread = threading.Thread(target=do_scrape, daemon=True)
    _scraping_thread.start()


def __on_button_cancel():
    if not context.is_ready or not context.scraper_busy:
        return

    _button_cancel.configure(state=tkinter.DISABLED)

    __set_status_text("Stopping threads... please wait...")
    context.interrupted = True

    def do_stop():
        fking.queues.wait_on_image_download_threads()

        __set_status_text("Cancelled... Ready...")
        __update_ui_state(False)

    threading.Thread(target=do_stop, daemon=True).start()


def __do_request_exit(*args):
    if context.scraper_busy:
        return

    _tk.destroy()
    sys.exit()


def __set_status_text(text: Optional[str] = None):
    if text:
        _status_var.set(text)
    else:
        _status_var.set('')


_tk.protocol("WM_DELETE_WINDOW", __do_request_exit)

_frame_textfield_2 = tkinter.Frame(_frame, background="#a0a0a0", borderwidth=1)
_textfield_input_search_terms = tkinter.Entry(_frame_textfield_2, justify=tkinter.LEFT, relief=tkinter.FLAT, width=64)
_textfield_input_search_terms.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
_frame_textfield_2.grid(row=1, column=0, sticky=tkinter.NSEW)

_textfield_input_search_terms.configure(state="readonly")

_button_browse_search_term_list = tkinter.Button(_frame, text="Browse", width=10, command=__on_browse_search_terms_list)
_button_browse_output_directory = tkinter.Button(_frame, text="Browse", command=__on_browse_output_directory)

tkinter.Label(_frame, text="Search Query List", justify=tkinter.LEFT).grid(row=0, column=0, columnspan=2, sticky='w')
_button_browse_search_term_list.grid(row=1, column=1, padx=(3, 0), sticky=tkinter.NSEW)

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
_textfield_output_directory.configure(state="readonly")

_frame_textfield.grid(row=3, column=0, padx=(0, 3), sticky=tkinter.NSEW)
_button_browse_output_directory.grid(row=3, column=1, padx=(3, 0), sticky=tkinter.NSEW)

_progress_bar_download_queue = tkinter.ttk.Progressbar(_frame, orient=tkinter.HORIZONTAL)
_progress_bar_search_term_list = tkinter.ttk.Progressbar(_frame, orient=tkinter.HORIZONTAL)

tkinter.Label(_frame, text="Image Download Queue", justify=tkinter.LEFT).grid(
        row=4,
        column=0,
        sticky='w',
        pady=(12, 0)
)

_progress_bar_download_queue.grid(row=5, column=0, columnspan=2, sticky=tkinter.NSEW)

_image_queue_status_var = tkinter.StringVar()
_image_queue_status_var.set("0/0")

tkinter.Label(_frame, textvariable=_image_queue_status_var, justify=tkinter.RIGHT, anchor=tkinter.W).grid(
        row=4,
        column=1,
        sticky='e',
        pady=(12, 0)
)

tkinter.Label(_frame, text="Search Term Queue", justify=tkinter.LEFT).grid(
        row=6,
        column=0,
        sticky='w',
        pady=(6, 0)
)

_search_term_status_var = tkinter.StringVar()
_search_term_status_var.set("0/0")

tkinter.Label(_frame, textvariable=_search_term_status_var, justify=tkinter.RIGHT, anchor=tkinter.W).grid(
        row=6,
        column=1,
        sticky='e',
        pady=(12, 0)
)

_progress_bar_search_term_list.grid(row=7, column=0, columnspan=2, sticky=tkinter.NSEW)

_status_var = tkinter.StringVar()
_status_var.set("Not Ready")

_frame_status = tkinter.Frame(_frame)
tkinter.Label(_frame_status, text="Status:", justify=tkinter.LEFT).grid(row=0, column=0)
_textfield_status = tkinter.Label(_frame_status, textvariable=_status_var, justify=tkinter.LEFT, anchor=tkinter.W)
_textfield_status.grid(row=0, column=1)

_frame_status.grid(row=8, column=0, columnspan=2, sticky=tkinter.NSEW, pady=(12, 3))

_frame_action_buttons = tkinter.Frame(_frame)
_frame_action_buttons.grid(row=9, column=0, columnspan=2, sticky=tkinter.NSEW)

_button_start = tkinter.Button(_frame_action_buttons, text="Start", command=__on_button_start)
_button_start.pack(side=tkinter.RIGHT, expand=True, fill=tkinter.X)

_button_cancel = tkinter.Button(_frame_action_buttons, text="Cancel", command=__on_button_cancel)
_button_cancel.pack(side=tkinter.LEFT, expand=True, fill=tkinter.X)

_spacer = tkinter.Frame(_frame_action_buttons)
_spacer.pack(side=tkinter.LEFT, padx=3)


def __do_status_bar_updates():
    images_downloaded = context.images_downloaded
    image_queue_size = context.total_queued_images

    _image_queue_status_var.set(f"{images_downloaded:,}/{image_queue_size:,}")
    __set_progress(_progress_bar_download_queue, images_downloaded, image_queue_size)
    _tk.after(200, __do_status_bar_updates)


def show_ui():
    __set_status_text("Ready")
    __update_ui_state()

    _tk.mainloop()
