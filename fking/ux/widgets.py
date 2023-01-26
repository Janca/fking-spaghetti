import sys
import tkinter as _tk
import tkinter.ttk as _ttk
from typing import Callable, Optional, Union

import fking.legacy.utils


def create_browse_widget_group(
        parent: _tk.Misc,
        dialog_fn: Callable[[...], any],
        label_text: str,
        **kwargs
) -> tuple[_tk.Frame, _tk.StringVar, Callable[[Union[_tk.NORMAL, _tk.DISABLED]], None]]:
    wrapper = _ttk.Frame(parent)

    str_var = _tk.StringVar()
    str_var_set_fn = str_var.set

    entry_path = _ttk.Entry(wrapper, textvariable=str_var, state="readonly")
    label_entry_path = _ttk.Label(wrapper, text=label_text, justify=_tk.LEFT, anchor=_tk.W)
    button_browse = _ttk.Button(wrapper, text="Browse", width=10)

    wrapper.grid_columnconfigure(0, weight=1)
    wrapper.grid_columnconfigure(1, weight=0)

    label_entry_path.grid(row=0, column=0, columnspan=2, sticky=_tk.NSEW)
    entry_path.grid(row=1, column=0, sticky=_tk.NSEW)
    button_browse.grid(row=1, column=1, sticky=_tk.NSEW)

    def on_button_browse():
        browse = dialog_fn(**kwargs)
        if not browse:
            return

        browse_path = fking.legacy.utils.normalize_path(browse)
        str_var.set(browse_path)

    def set_state(state: Union[_tk.NORMAL, _tk.DISABLED]):
        button_browse.configure(state=state)

    def override_string_var_set(_: _tk.Misc, v: str):
        str_var_set_fn(v)
        entry_path.xview_scroll(len(v), _tk.UNITS)

    str_var.set = override_string_var_set.__get__(str_var)
    button_browse.configure(command=on_button_browse)

    return wrapper, str_var, set_state


def create_progress_widget_group(
        parent: _tk.Misc,
        label_text: Union[str, _tk.StringVar],
        **kwargs
) -> tuple[_tk.Frame, Callable[[int, Optional[int]], None]]:
    wrapper = _ttk.Frame(parent)

    is_str_label = isinstance(label_text, str)
    label = _ttk.Label(
            wrapper,
            text=label_text if is_str_label else None,
            textvariable=label_text if not is_str_label else None,
            justify=_tk.LEFT,
            anchor=_tk.W
    )

    progressbar = _ttk.Progressbar(wrapper, **kwargs)

    label.pack(side=_tk.TOP, anchor=_tk.W)
    progressbar.pack(side=_tk.BOTTOM, anchor=_tk.W)

    def update_progress_bar(value: int, max_value: int = -1):
        print("Updating progress bar", value, max_value)
        if value < 0 or max_value <= 0:
            progressbar["mode"] = "indeterminate"
            progressbar["value"] = 0
            progressbar["maximum"] = 100
            progressbar.start()
        elif value == -2:
            progressbar.stop()
        else:
            progressbar["mode"] = "determinate"
            progressbar["value"] = value
            progressbar["maximum"] = max_value

    return wrapper, update_progress_bar


def set_entry_text(entry: _tk.Entry, text: Optional[str]):
    state = entry.cget("state")
    entry.configure(state=_tk.NORMAL)
    entry.delete(1, _tk.END)
    entry.insert(_tk.END, text if text else '')
    entry.xview_scroll(sys.maxsize, _tk.PAGES)
    entry.configure(state=state)
