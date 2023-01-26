import tkinter
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
