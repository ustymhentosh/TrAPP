import tkinter as tk

import ttkbootstrap as ttk
from tkinter import filedialog as fd
import os


class FrontDoor(ttk.Frame):

    def __init__(self, master, _=None):

        ttk.Frame.__init__(self, master)
        root = ttk.Frame(master=self)

        container = ttk.Frame(master=root)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=3)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_columnconfigure(2, weight=1)
        container.grid_columnconfigure(3, weight=1)

        main_lbl = ttk.Label(
            master=container,
            text="Оберіть інструмент",
            font="Calibri 20",
            justify="center",
        )

        # ttk.Style().configure("primary.TButton", font=("Calibri", 12))

        # Creating a photoimage object to use image
        self.bus_pht = ttk.PhotoImage(file="images/1F68D_color.png")
        self.camera_pht = ttk.PhotoImage(file="images/E1C4_color.png")

        self.bus_sized = self.bus_pht.subsample(3, 3)
        self.cam_sized = self.camera_pht.subsample(3, 3)

        # here, image option is used to
        # set image on button
        bus_button = ttk.Frame(master=container)
        cam_button = ttk.Frame(master=container)

        bus_mode = ttk.Button(
            bus_button,
            image=self.bus_sized,
            command=lambda: master.switch_frame("GPSLoaderPG"),
        )
        bus_ml = ttk.Label(master=bus_button, text="Транспорт")
        bus_mode.pack()
        bus_ml.pack()

        camera_mode = ttk.Button(cam_button, image=self.cam_sized)
        cam_ml = ttk.Label(master=cam_button, text="Камери")
        camera_mode.pack()
        cam_ml.pack()

        main_lbl.grid(column=0, row=0, columnspan=4, pady=(10, 10))
        bus_button.grid(column=0, row=1, columnspan=2, pady=(10, 10), padx=10)
        cam_button.grid(column=2, row=1, columnspan=2, pady=(10, 10), padx=10)

        container.pack(expand=True, fill="both")
        root.pack(padx=20, pady=20, expand=True, fill="both")
