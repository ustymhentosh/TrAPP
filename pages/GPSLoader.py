from pathlib import Path
import time
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog as fd
import os
from threading import Thread

from tools.loader import extract_and_organize_one_route


class GPSLoaderPG(ttk.Frame):

    def __init__(self, master, _=None):
        ttk.Frame.__init__(self, master)
        root = ttk.Frame(master=self)
        container = ttk.Frame(master=root)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=3)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_columnconfigure(2, weight=1)

        self.main_dir = ""
        self.path_to_results_fldr = ".organized_gps"

        def callback():
            dir_name = fd.askdirectory()
            self.main_dir = dir_name
            folder_lbl["text"] = f"Обрано: {self.main_dir}"
            button_cont["state"] = tk.ACTIVE
            button_new["state"] = tk.ACTIVE
            # master.switch_frame("MainPage")

        def is_there_our_files():
            return ".organized_gps" in list(os.listdir(os.getcwd()))

        def run_loading():
            path_to_excels_folder = self.main_dir
            total_len = len(os.listdir(path_to_excels_folder))
            for i in os.listdir(path_to_excels_folder):
                self.progress_bar["value"] = self.progress_bar["value"] + 1
                self.progress_num["text"] = f"{round(100 * self.progress_bar["value"]/ total_len, 1)}%"
                print(i)

                if not os.path.exists(f"{self.path_to_results_fldr}/{Path(i).stem}/"):
                    os.makedirs(f"{self.path_to_results_fldr}/{Path(i).stem}/")
                extract_and_organize_one_route(
                    f"{path_to_excels_folder}/{i}",
                    4,
                    f"{self.path_to_results_fldr}/{Path(i).stem}",
                    Path(i).stem,
                )
            master.switch_frame("MainPage", self.main_dir)
            master.deiconify()

        def compute():
            self.progress_window = tk.Toplevel(root)
            self.progress_window.title("Обчислення даних")
            self.progress_window.geometry("400x150")
            
            self.progress_window.rowconfigure(0, weight=1)
            self.progress_window.rowconfigure(1, weight=1)

            self.progress_label = ttk.Label(self.progress_window, text="oбчислення...")
            self.progress_label.grid(row = 0, column = 0, pady = (10, 0), sticky="w", padx=20)

            self.pbf = ttk.Frame(master=self.progress_window)
            self.progress_bar = ttk.Progressbar(
                self.pbf,
                length=250,
                mode="determinate",
                maximum=len(os.listdir(self.path_to_results_fldr)),
                style='success.Striped.Horizontal.TProgressbar'
            )
            self.progress_bar.pack(side="left")
            self.progress_num = ttk.Label(master=self.pbf)
            self.progress_num.pack(side="right", padx=10)
            
            self.pbf.grid(row = 1, column=0, sticky="w", padx=20)

            master.withdraw()
            Thread(target=run_loading).start()

        ttk.Style().configure("primary.Outline.TButton", font=("Calibri", 11))
        ttk.Style().configure("success.Outline.TButton", font=("Calibri", 11))
        self.pls_pht = ttk.PhotoImage(file="images/Excel.svg.png")
        self.pls_sized = self.pls_pht.subsample(12, 12)
        self.go_pht = ttk.PhotoImage(file="images/27A1_color.png")
        self.go_sized = self.go_pht.subsample(6, 6)
        self.calc_pht = ttk.PhotoImage(file="images/1F9EE_color.png")
        self.calc_sized = self.calc_pht.subsample(6, 6)

        main_lbl = ttk.Label(
            master=container, text="", font="Calibri 14", justify="center"
        )

        folder_lbl = ttk.Label(
            master=container,
            text="",
            font="Calibri 10",
            justify="center",
            wraplength=400,
        )

        if is_there_our_files():
            main_lbl["text"] = (
                "У вашій папці містятся обчислені дані.\nВкажіть папку із даними Excel."
            )
            button_pick = ttk.Button(
                master=container,
                command=callback,
                image=self.pls_sized,
                text="обрати папку",
                style="outline.success.TButton",
                compound="top",
            )
            button_cont = ttk.Button(
                master=container,
                image=self.go_sized,
                text="використати наявні",
                command=lambda: master.switch_frame("MainPage", self.main_dir),
                style="outline.primary.TButton",
                compound="top",
                state=tk.DISABLED,
            )
            button_new = ttk.Button(
                master=container,
                image=self.calc_sized,
                text="обчислити нові",
                command=lambda: compute(),
                style="outline.primary.TButton",
                compound="top",
                state=tk.DISABLED,
            )
            button_pick.grid(column=0, row=2, padx=10, ipadx=10, ipady=10)
            button_cont.grid(column=1, row=2, ipady=10)
            button_new.grid(column=2, row=2, padx=10, ipady=10)
        else:
            main_lbl["text"] = "Оберіть папку із данними Excel для маршрутів."
            button_pick = ttk.Button(
                master=container,
                command=callback,
                image=self.pls_sized,
                text="обрати папку",
                style="outline.success.TButton",
                compound="top",
            )
            button_cont = ttk.Button(
                master=container,
                image=self.calc_sized,
                text="обчислити",
                command=lambda: compute(),
                style="outline.primary.TButton",
                compound="top",
                state=tk.DISABLED,
            )
            button_pick.grid(column=0, row=2, ipady=20, ipadx=20)
            button_cont.grid(column=1, row=2, ipady=20, ipadx=20)

        main_lbl.grid(column=0, row=0, columnspan=4, pady=(10, 0))
        folder_lbl.grid(column=0, row=1, columnspan=4, pady=(10, 0))
        container.pack(expand=True, fill="both")
        root.pack(padx=20, pady=20, expand=True, fill="both")
