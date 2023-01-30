import sys
import tkinter as _tk
import tkinter.ttk as _ttk
from abc import ABC as _ABC
from typing import Callable, Optional, TypeVar, Union

import fking.utils

RESET = -3
PROGRESSBAR_STOP = -2
PROGRESS_BAR_INDETERMINATE = -1

_TK = TypeVar("_TK", _tk.Widget, _tk.Frame)


class Toggle(_ttk.Button, _ABC):

    def toggle(self, selected: bool):
        raise NotImplementedError()


def create_browse_widget_group(
        parent: _tk.Misc,
        dialog_fn: Callable[[...], any],
        label_text: str,
        **kwargs
) -> tuple[_tk.Frame, _tk.StringVar, Callable[[Union[_tk.NORMAL, _tk.DISABLED]], None]]:
    wrapper = _ttk.Frame(parent)

    str_var = _tk.StringVar(wrapper)
    str_var_set_fn = str_var.set

    entry_path = _ttk.Entry(wrapper, textvariable=str_var)
    label_entry_path = _ttk.Label(wrapper, text=label_text, justify=_tk.LEFT, anchor=_tk.W)
    button_browse = _ttk.Button(wrapper, text="Browse", width=10)

    wrapper.grid_columnconfigure(0, weight=1)
    wrapper.grid_columnconfigure(1, weight=0)
    wrapper.grid_rowconfigure(1, weight=1)

    label_entry_path.grid(row=0, column=0, columnspan=2, sticky=_tk.NSEW)
    entry_path.grid(row=1, column=0, sticky=_tk.NSEW, padx=(0, 3))
    button_browse.grid(row=1, column=1, sticky=_tk.NSEW)

    def on_button_browse():
        browse = dialog_fn(**kwargs)
        if not browse:
            return

        browse_path = fking.utils.normalize_path(browse)
        str_var.set(browse_path)

    def set_state(state: Union[_tk.NORMAL, _tk.DISABLED]):
        button_browse.configure(state=state)
        entry_path.configure(state=state)

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
) -> tuple[_tk.Frame, Callable[[int, int], None]]:
    wrapper = _ttk.Frame(parent)

    is_str_label = isinstance(label_text, str)
    frame_labels = _ttk.Frame(wrapper)

    label = _ttk.Label(
        frame_labels,
        text=label_text if is_str_label else None,
        textvariable=label_text if not is_str_label else None,
        justify=_tk.LEFT,
        anchor=_tk.W
    )

    progressbar = _ttk.Progressbar(wrapper, **kwargs)
    progressbar.str_var_stats = _tk.StringVar(wrapper)

    label_progress_stats = _ttk.Label(
        frame_labels,
        textvariable=progressbar.str_var_stats,
        justify=_tk.RIGHT,
        anchor=_tk.E
    )

    progressbar.str_var_stats.set("0/0")

    label.pack(side=_tk.LEFT, anchor=_tk.W, fill=_tk.X, expand=True)
    label_progress_stats.pack(side=_tk.RIGHT, anchor=_tk.E, fill=_tk.X, expand=False)

    frame_labels.pack(side=_tk.TOP, anchor=_tk.W, fill=_tk.X, expand=True)
    progressbar.pack(side=_tk.BOTTOM, anchor=_tk.W, fill=_tk.X, expand=True, ipady=3)

    def update_progress_bar(value: int, max_value: int = -1):
        print("Updating progress bar", value, max_value)
        if value < 0 or max_value <= 0:
            progressbar.str_var_stats.set("0/0")
            progressbar["mode"] = "indeterminate"
            progressbar["value"] = 0
            progressbar["maximum"] = 100
            progressbar.start()
        elif value == -2 or value == -3:
            progressbar.str_var_stats.set("0/0")
            progressbar.stop()
        else:
            progressbar.str_var_stats.set(f"{value:,}/{max_value:,}")
            progressbar.stop()

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


def subscribe_to_tk_var(tk_var: _tk.Variable, target: Callable[[any], None]):
    tk_var.trace_add("write", lambda name, index, mode, _tk_var=tk_var: target(_tk_var.get()))


def section_divider(
        parent: _tk.Misc,
        padx: Union[str, float, tuple[Union[str, float], Union[str, float]]] = 0,
        pady: Union[str, float, tuple[Union[str, float], Union[str, float]]] = 0
) -> _tk.Widget:
    wrapper = _ttk.Frame(parent)
    wrapper.grid_columnconfigure(0, weight=1)
    _ttk.Separator(wrapper, orient=_tk.HORIZONTAL).grid(row=0, column=0, padx=padx, pady=pady, sticky=_tk.NSEW)
    return wrapper


def x_flow_panel(parent: _tk.Misc) -> tuple[_tk.Frame, _tk.Text]:
    parent_background = parent.cget("background")

    wrapper = _ttk.Frame(parent)
    x_flow = _tk.Text(
        wrapper,
        state=_tk.NORMAL,
        background='blue',
        selectbackground=parent_background,
        padx=0, pady=0,
        cursor="arrow",
        relief=_tk.FLAT,
        wrap=_tk.WORD
    )

    x_flow.pack(side=_tk.TOP, anchor=_tk.CENTER, fill=_tk.BOTH, expand=True)
    return wrapper, x_flow


def toggle_button(master, **kwargs) -> Toggle:
    button = _ttk.Button(master, **kwargs)
    button.toggled = False

    def do_toggle(self: _ttk.Button):
        self.toggled = not self.toggled
        toggle(self, self.toggled)

        return "break"

    def toggle(self: _ttk.Button, selected: bool):
        self.toggled = selected
        self.state(["pressed" if selected else "!pressed"])

    button.bind("<ButtonRelease-1>", lambda e: do_toggle(button))
    button.toggle = toggle.__get__(button)

    # noinspection PyTypeChecker
    return button
