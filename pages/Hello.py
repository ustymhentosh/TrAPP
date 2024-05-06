import tkinter as tk
import ttkbootstrap as ttk
import time
import random


class Hello(ttk.Frame):

    def __init__(self, master, _=None):

        ttk.Frame.__init__(self, master)
        root = ttk.Frame(master=self)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)
        # ttk.Style().configure("primary.TButton", font=("Calibri", 12))

        def run_pb():
            for i in range(0, 101):
                time.sleep(0.06 * random.random())
                pd["value"] = i
                pb_t["text"] = f"{i} %"
                root.update()
            master.switch_frame("GPSLoaderPG")

        self.logo = ttk.PhotoImage(file="images/icon77.png")
        self.logo_sized = self.logo.subsample(2, 2)

        main_lbl = ttk.Label(
            master=root,
            text="TrAPP",
            font="Calibri 30",
            justify="center",
        )
        pht = ttk.Label(master=root, image=self.logo_sized)

        pb_f = ttk.Frame(master=root)
        pd = ttk.Progressbar(
            master=pb_f, mode="determinate", length=400, style="success.Striped"
        )
        pb_t = ttk.Label(master=pb_f, font="Calibri 12")
        main_lbl.grid(row=0, column=1)
        pb_f.grid(
            row=2,
            column=1,
        )
        pht.grid(
            row=1,
            column=1,
        )
        pd.grid(
            row=0,
            column=0,
        )
        pb_t.grid(row=0, column=1, padx=20)

        root.pack(padx=20, pady=20, expand=True, fill="both")
        root.after(50, run_pb)
