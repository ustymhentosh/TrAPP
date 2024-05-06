from pathlib import Path
import time
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog as fd
import os
from threading import Thread
from ttkbootstrap import Style

from tools.loader import extract_and_organize_one_route


class GPSLoaderPG(ttk.Frame):

    def __init__(self, master, _=None):
        ttk.Frame.__init__(self, master)
        root = ttk.Frame(master=self)
        root.grid_rowconfigure(0, weight=2)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=6)
        root.grid_rowconfigure(3, weight=1)
        root.grid_rowconfigure(4, weight=2)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        self.main_dir = ""
        self.path_to_results_fldr = ".organized_gps"
        
        def count_excel_files(folder_path):
            excel_files = [file for file in os.listdir(folder_path) if file.endswith('.xlsx') or file.endswith('.xls')]
            return len(excel_files)

        def callback():
            dir_name = fd.askdirectory()
            self.main_dir = dir_name
            folder_lbl["text"] = f"Знайдено: {count_excel_files(self.main_dir)} Excel файлів"
            folder_lbl.grid(column=1, row = 2, padx=10, sticky="w")
            # master.switch_frame("MainPage")

        def is_there_our_files():
            return ".organized_gps" in list(os.listdir(os.getcwd()))

        def run_loading():
            path_to_excels_folder = self.main_dir
            total_len = len(os.listdir(path_to_excels_folder))
            try:
                self.progress_bar["maximum"] = total_len,
                for i in os.listdir(path_to_excels_folder):
                    self.progress_bar["value"] = self.progress_bar["value"] + 1
                    self.progress_num["text"] = f"{round(100 * self.progress_bar["value"]/ total_len, 1)}%"

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
                self.progress_window.destroy()
            except:
                self.progress_window.destroy()
                master.deiconify()
        
        def del_top_level():
            self.progress_window.destroy()
            master.deiconify()

        def compute():
            self.progress_window = tk.Toplevel(master)
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
                style='success.Striped.Horizontal.TProgressbar'
            )
            self.progress_bar.pack(side="left")
            self.progress_num = ttk.Label(master=self.pbf)
            self.progress_num.pack(side="right", padx=10)
            
            self.pbf.grid(row = 1, column=0, sticky="w", padx=20)
            
            self.progress_window.protocol("WM_DELETE_WINDOW", del_top_level)

            master.withdraw()
            a = Thread(target=run_loading)
            a.start()
        
        def show_load_btn():
            load_btn.grid(column=0, row=2, sticky=tk.W)
            folder_lbl.grid(column=1, row=2, sticky="w")
        def hide_load_btn():
            load_btn.grid_forget()
            folder_lbl.grid_forget()
            
        def next_btn():
            if is_there_our_files():
                mode = self.choice.get()
                if mode == "prc":
                    master.switch_frame("MainPage")
                elif mode == "new" and count_excel_files(self.main_dir) > 0:
                    compute()
            else:
                compute()

        ttk.Style().configure("primary.Outline.TButton", font=("Calibri", 11))
        ttk.Style().configure("success.Outline.TButton", font=("Calibri", 11))
        self.pls_pht = ttk.PhotoImage(file="images/Excel.svg.png")
        self.pls_sized = self.pls_pht.subsample(8, 8)
        self.go_pht = ttk.PhotoImage(file="images/27A1_color.png")
        self.go_sized = self.go_pht.subsample(8, 8)
        self.calc_pht = ttk.PhotoImage(file="images/1F9EE_color.png")
        self.calc_sized = self.calc_pht.subsample(8, 8)

        main_lbl = ttk.Label(
            master=root, text="", font="Calibri 14 bold", justify="left"
        )
        
        middle_cont = ttk.Frame(master=root)
        middle_cont.rowconfigure(0, weight=1)
        middle_cont.rowconfigure(1, weight=1)
        middle_cont.rowconfigure(2, weight=3)
        middle_cont.columnconfigure(0, weight=1)
        middle_cont.columnconfigure(1, weight=2)

        folder_lbl = ttk.Label(
            master=middle_cont,
            text="",
            font="Courier 12",
            justify="left",
            wraplength=400,
            anchor=tk.CENTER
        )
        
        self.choice = tk.StringVar()
        self.choice.set("prc")
        
        Style().configure('TRadiobutton', font=('Calibri', 14))
        Style().map('TRadiobutton', foreground=[
        ('disabled', 'white'),
        ('selected', '#3486eb'),
        ('!selected', 'gray')])
        Style().configure('success.Outline.TButton', font=('Calibri', 14, "bold"))

        if is_there_our_files():
            main_lbl["text"] = "Знайдено обраховані дані, оберіть опцію:"
            proced_cb = ttk.Radiobutton(middle_cont, text=' <- використати наявні дані', variable=self.choice, value="prc", command=hide_load_btn)
            load_cb = ttk.Radiobutton(middle_cont, text=' <- обрахувати нові дані', variable=self.choice, value="new", command=show_load_btn)
            load_btn = ttk.Button(master=middle_cont, 
                                  text="📂 відкрити", 
                                  style="primary.Outline.TButton", 
                                  command=callback)
            proced_cb.grid(column=0, row=0, sticky="w", columnspan=2)
            load_cb.grid(column=0, row=1, sticky="w", columnspan=2)
        else:
            main_lbl["text"] = "Необхідно обрахувати дані, оберіть папку:"
            load_btn = ttk.Button(master=middle_cont, 
                                  text="📂 відкрити", 
                                  style="primary.Outline.TButton",
                                  command=callback)
            load_btn.grid(column=0, row=2, sticky="w")
        
        sep1 = ttk.Separator(master=root)
        sep2 = ttk.Separator(master=root)

        run_butt = ttk.Button(
            master=root,
            text="Далі",
            style="success.Outline.TButton",
            command = next_btn
        )

        main_lbl.grid(row=0, column=0, pady=(10, 0), sticky=tk.W, columnspan=4)
        sep1.grid(row=1, column=0, columnspan=4, sticky=tk.EW)
        middle_cont.grid(row=2, column=0, columnspan=4, sticky=tk.NSEW)
        sep2.grid(row=3, column=0, columnspan=4, sticky=tk.EW)
        run_butt.grid(row=4, column=0, columnspan=4, sticky=tk.E)

        root.pack(padx=20, pady=20, expand=True, fill="both")
