import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog as fd
import os
import json
import threading
from pages.RoutesTab import RoutesTab
from pages.StopsTab import StopsTab
from tools.routes_analysis_demo import get_commute_time, _plot_and_save_dct


class MainPage(ttk.Frame):

    def __init__(self, master, main_dir):
        ttk.Frame.__init__(self, master)
        root = ttk.Frame(master=self)

        ttk.Style().configure(
            "light.TNotebook", font=("Calibri", 14), background="#F5F5F5"
        )
        tab_parent = ttk.Notebook(root, bootstyle="light", style="light.TNotebook")

        # create frames
        route_frame = RoutesTab(tab_parent, main_dir)
        stop_frame = StopsTab(tab_parent, main_dir)

        stop_frame.pack(fill="both", expand=True)
        route_frame.pack(fill="both", expand=True)
        tab_parent.add(route_frame, text="Маршрути")
        tab_parent.add(stop_frame, text="Зупинки")

        tab_parent.pack(expand=True, fill="both")
        root.pack(expand=True, fill="both")
