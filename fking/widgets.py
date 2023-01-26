import tkinter
import tkinter.ttk
from typing import Union


def spacer(master, size: int, orient: Union[tkinter.HORIZONTAL, tkinter.VERTICAL]) -> tkinter.Widget:
    padding = int(size / 2.0)
    if padding != (size / 2.0):
        padding = (padding, padding + 1)

    spacer = tkinter.Frame(master)
    pad = tkinter.Frame(spacer)

    if orient == tkinter.HORIZONTAL:
        pad.grid(row=0, column=0, padx=padding, sticky=tkinter.NSEW)
    elif orient == tkinter.VERTICAL:
        pad.grid(row=0, column=0, pady=padding, sticky=tkinter.NSEW)
    else:
        raise ValueError(f"Expected Union['{tkinter.HORIZONTAL}', '{tkinter.VERTICAL}']")

    return spacer


def x_spacer(master, size: int) -> tkinter.Widget:
    return spacer(master, size, tkinter.HORIZONTAL)


def y_spacer(master, size: int) -> tkinter.Widget:
    return spacer(master, size, tkinter.VERTICAL)


def label_separator(master, label: Union[str, tkinter.StringVar]) -> tkinter.Widget:
    wrapper = tkinter.Frame(master)
    is_string_var = isinstance(label, tkinter.StringVar)

    tkinter.ttk.Label(
            wrapper,
            text=label if not is_string_var else None,
            textvariable=label if is_string_var else None
    ).pack(side=tkinter.LEFT, anchor=tkinter.W, fill=tkinter.Y, expand=False)
    x_spacer(wrapper, 3).pack(side=tkinter.LEFT, expand=False)
    tkinter.ttk.Separator(
            wrapper,
            orient=tkinter.HORIZONTAL
    ).pack(side=tkinter.LEFT, anchor=tkinter.W, fill=tkinter.X, expand=True)

    return wrapper


def toggle_button(master, **kwargs) -> tkinter.ttk.Button:
    button = tkinter.ttk.Button(master, **kwargs)
    button.toggled = False

    def do_toggle(self: tkinter.ttk.Button):
        self.toggled = not self.toggled
        toggle(self, self.toggled)

        return "break"

    def toggle(self: tkinter.ttk.Button, selected: bool):
        self.toggled = selected
        self.state(["pressed" if selected else "!pressed"])

    button.bind("<ButtonRelease-1>", lambda e: do_toggle(button))
    button.toggle = toggle.__get__(button)

    return button


def layout_form_row(master: tkinter.Widget, *args: tkinter.Widget) -> tkinter.Widget:
    for i, widget in enumerate(args, start=1):
        if i == len(args):
            widget.pack(side=tkinter.RIGHT, anchor=tkinter.E, fill=tkinter.Y, expand=False)
        else:
            widget.pack(side=tkinter.LEFT, anchor=tkinter.W, fill=tkinter.BOTH, expand=True)
    return master
