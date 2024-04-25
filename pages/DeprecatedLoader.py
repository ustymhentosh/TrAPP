import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog as fd
import os


class LoaderPage(ttk.Frame):

    def __init__(self, master, _=None):
        ttk.Frame.__init__(self, master)
        root = ttk.Frame(master=self)
        container = ttk.Frame(master=root)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_columnconfigure(2, weight=1)
        container.grid_columnconfigure(3, weight=1)

        self.main_dir = ""

        def callback():
            dir_name = fd.askdirectory()
            self.main_dir = dir_name

        def is_there_our_files():
            return ".organized_data" in list(os.listdir(os.getcwd()))

        main_lbl = ttk.Label(
            master=container, text="", font="Calibri 14", justify="center"
        )

        ttk.Style().configure("primary.TButton", font=("Calibri", 12))
        if is_there_our_files():
            main_lbl["text"] = (
                "У вашій папці мітятся уже проаналізовані данні.\nПрацювати із ними чи завантажити нові?"
            )
            button_pick = ttk.Button(
                master=container,
                text="📂 обрати папку",
                command=callback,
                style="primary.TButton",
            )
            button_cont = ttk.Button(
                master=container,
                text="✅ продовжити",
                command=lambda: master.switch_frame("MainPage"),
                style="primary.TButton",
            )
            button_pick.grid(column=1, row=1)
            button_cont.grid(column=2, row=1)
        else:
            main_lbl["text"] = "Оберіть папку із данними Excel для маршрутів."
            button_pick = ttk.Button(
                master=container,
                text="📂 обрати папку",
                command=callback,
                style="primary.TButton",
            )
            button_pick.grid(row=1, columnspan=4)

        main_lbl.grid(column=0, row=0, columnspan=4, pady=(10, 30))

        container.pack(expand=True, fill="both")
        root.pack(padx=20, pady=20, expand=True, fill="both")
