import tkinter.filedialog

import fking.ux

_tk = tkinter.Tk()
_tk.geometry("200x200")

frame_main_settings, str_var_queries, str_var_download_path, \
    set_state_main_settings = fking.ux.frames.create_primary_settings_frame(_tk)

frame_main_settings.pack(side=tkinter.TOP, anchor=tkinter.N, fill=tkinter.X, expand=True)

frame_progress, update_progress = fking.ux.widgets.create_progress_widget_group(
        _tk, label_text="Image Downloads",
        orient=tkinter.HORIZONTAL
)

frame_progress.pack(side=tkinter.TOP, anchor=tkinter.N, fill=tkinter.X, expand=True)
update_progress(10, 100)

_tk.mainloop()
