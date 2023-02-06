import tkinter as _tk
import tkinter.ttk as _ttk
from typing import Union


class _ToggleButton(_ttk.Button):
    def toggle(self: _ttk.Button, selected: bool):
        raise NotImplementedError()


def spacer(master, size: int, orient: Union[_tk.HORIZONTAL, _tk.VERTICAL]) -> _tk.Widget:
    padding = int(size / 2.0)
    if padding != (size / 2.0):
        padding = (padding, padding + 1)

    spacer = _tk.Frame(master)
    pad = _tk.Frame(spacer)

    if orient == _tk.HORIZONTAL:
        pad.grid(row=0, column=0, padx=padding, sticky=_tk.NSEW)
    elif orient == _tk.VERTICAL:
        pad.grid(row=0, column=0, pady=padding, sticky=_tk.NSEW)
    else:
        raise ValueError(f"Expected Union['{_tk.HORIZONTAL}', '{_tk.VERTICAL}']")

    return spacer


def x_spacer(master, size: int) -> _tk.Widget:
    return spacer(master, size, _tk.HORIZONTAL)


def y_spacer(master, size: int) -> _tk.Widget:
    return spacer(master, size, _tk.VERTICAL)


def label_separator(master, label: Union[str, _tk.StringVar]) -> _tk.Widget:
    wrapper = _tk.Frame(master)
    is_string_var = isinstance(label, _tk.StringVar)

    _ttk.Label(
        wrapper,
        text=label if not is_string_var else None,
        textvariable=label if is_string_var else None
    ).pack(side=_tk.LEFT, anchor=_tk.W, fill=_tk.Y, expand=False)
    x_spacer(wrapper, 3).pack(side=_tk.LEFT, expand=False)
    _ttk.Separator(
        wrapper,
        orient=_tk.HORIZONTAL
    ).pack(side=_tk.LEFT, anchor=_tk.W, fill=_tk.X, expand=True)

    return wrapper


def toggle_button(master, **kwargs) -> _ToggleButton:
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


def layout_form_row(master: _tk.Widget, *args: _tk.Widget) -> _tk.Widget:
    for i, widget in enumerate(args, start=1):
        if i == len(args):
            widget.pack(side=_tk.RIGHT, anchor=_tk.E, fill=_tk.Y, expand=False)
        else:
            widget.pack(side=_tk.LEFT, anchor=_tk.W, fill=_tk.BOTH, expand=True)
    return master
