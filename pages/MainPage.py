import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog as fd
import os
import json
import threading
from tools.routes_analysis_demo import get_commute_time, _plot_and_save_dct


class MainPage(ttk.Frame):

    def __init__(self, master, main_dir):
        ttk.Frame.__init__(self, master)
        root = ttk.Frame(master=self)
        self.main_dir = main_dir
        self.comp_dir = ".organized_data"

        def on_field_change(arg):
            start_stop_picker["values"] = sorted(get_stops_for_bus())
            finish_stop_picker["values"] = sorted(get_stops_for_bus())

        def get_stops_for_bus():
            if bus_pick.get():
                bus_name = bus_pick.get()
                with open(
                    f"{self.comp_dir}{os.sep}{bus_name}{os.sep}{bus_name}_all_stops.json",
                    "r",
                    encoding="utf-8",
                ) as f:
                    stops = json.load(f)
            else:
                stops = "мартруту_не_вибрано"
            return stops

        def find_file_from_start(start, folder):
            for filename in os.listdir(folder):
                if filename.startswith(start):
                    return os.path.join(folder, filename)
            return None

        def start_plot_route():
            day_abbreviations = {
                0: "Пн",
                1: "Вт",
                2: "Ср",
                3: "Чт",
                4: "Пт",
                5: "Сб",
                6: "Нд",
            }
            self.selected_days = []
            for day_index, var in self.day_vars.items():
                if var.get() == 1:
                    self.selected_days.append(day_index)

            dct = get_commute_time(
                find_file_from_start(self.selected_bus.get(), self.main_dir),
                self.selected_start_stop.get(),
                self.selected_finish_stop.get(),
                self.selected_days,
            )
            selected_abbreviations = [
                day_abbreviations[index] for index in self.selected_days
            ]
            answ = "".join(selected_abbreviations)
            title = f"""Маршрут: {self.selected_bus.get()}, проміжок: {self.selected_start_stop.get()} - {self.selected_finish_stop.get()}, дні:{answ}"""
            _plot_and_save_dct(dct, title, "plots/lastplot.png")
            run_butt["text"] = "Отримати"
            run_butt["state"] = tk.ACTIVE
            master.event_generate("<<PlotingFinished>>", when="tail")

        def create_route_time_graph():
            run_butt["text"] = "⏳ у роботі ⏳"
            run_butt["state"] = tk.DISABLED
            plotting_thread = threading.Thread(target=start_plot_route, args=())
            plotting_thread.start()

        self.selected_start_stop = tk.StringVar()
        self.selected_finish_stop = tk.StringVar()

        ttk.Style().configure(
            "light.TNotebook", font=("Calibri", 14), background="#F5F5F5"
        )
        tab_parent = ttk.Notebook(root, bootstyle="light", style="light.TNotebook")

        # create frames
        stop_frame = ttk.Frame(tab_parent)
        route_frame = ttk.Frame(tab_parent)
        stop_frame.pack(fill="both", expand=True)
        route_frame.pack(fill="both", expand=True)
        tab_parent.add(route_frame, text="Маршрути")
        tab_parent.add(stop_frame, text="Зупинки")

        route_frame.rowconfigure(0, weight=1)
        route_frame.rowconfigure(1, weight=1)
        route_frame.rowconfigure(2, weight=1)
        route_frame.rowconfigure(3, weight=1)
        route_frame.columnconfigure(0, weight=1)
        route_frame.columnconfigure(1, weight=4)
        route_frame.columnconfigure(2, weight=1)

        bus_frm = ttk.Frame(master=route_frame)
        bus_lbl = ttk.Label(master=bus_frm, text="№ маршрут", font="Calibri 14")
        self.selected_bus = tk.StringVar()
        bus_pick = ttk.Combobox(
            master=bus_frm,
            values=os.listdir(self.comp_dir),
            font="Calibri 14",
            width=10,
            textvariable=self.selected_bus,
        )
        bus_pick.bind("<<ComboboxSelected>>", on_field_change)
        bus_lbl.pack()
        bus_pick.pack()

        start_finish_frm = ttk.Frame(master=route_frame)
        start_stop_lbl = ttk.Label(master=start_finish_frm, text="початкова зупинка")
        start_stop_picker = ttk.Combobox(
            master=start_finish_frm,
            values=get_stops_for_bus(),
            font="Calibri 14",
            textvariable=self.selected_start_stop,
        )
        finish_stop_lbl = ttk.Label(master=start_finish_frm, text="початкова зупинка")
        finish_stop_picker = ttk.Combobox(
            master=start_finish_frm,
            values=get_stops_for_bus(),
            font="Calibri 14",
            textvariable=self.selected_finish_stop,
        )

        days_frm = ttk.Frame(master=route_frame)
        self.mon_var = tk.IntVar(value=0)
        self.tue_var = tk.IntVar(value=0)
        self.wed_var = tk.IntVar(value=0)
        self.thr_var = tk.IntVar(value=0)
        self.fri_var = tk.IntVar(value=0)
        self.sat_var = tk.IntVar(value=0)
        self.sun_var = tk.IntVar(value=0)

        self.day_vars = {
            0: self.mon_var,
            1: self.tue_var,
            2: self.wed_var,
            3: self.thr_var,
            4: self.fri_var,
            5: self.sat_var,
            6: self.sun_var,
        }

        # Create Checkbuttons with IntVars
        mon = ttk.Checkbutton(
            master=days_frm, text="Пн", variable=self.mon_var, onvalue=1
        )
        tue = ttk.Checkbutton(
            master=days_frm, text="Вт", variable=self.tue_var, onvalue=1
        )
        wed = ttk.Checkbutton(
            master=days_frm, text="Ср", variable=self.wed_var, onvalue=1
        )
        thr = ttk.Checkbutton(
            master=days_frm, text="Чт", variable=self.thr_var, onvalue=1
        )
        fri = ttk.Checkbutton(
            master=days_frm, text="Пт", variable=self.fri_var, onvalue=1
        )
        sat = ttk.Checkbutton(
            master=days_frm, text="Сб", variable=self.sat_var, onvalue=1
        )
        sun = ttk.Checkbutton(
            master=days_frm, text="Нд", variable=self.sun_var, onvalue=1
        )

        mon.grid(row=0, column=0, padx=5, pady=5)
        tue.grid(row=0, column=1, padx=5, pady=5)
        wed.grid(row=0, column=2, padx=5, pady=5)
        thr.grid(row=0, column=3, padx=5, pady=5)
        fri.grid(row=0, column=4, padx=5, pady=5)
        sat.grid(row=0, column=5, padx=5, pady=5)
        sun.grid(row=0, column=6, padx=5, pady=5)

        run_butt = ttk.Button(
            master=route_frame,
            text="Отримати",
            style="success",
            command=lambda: create_route_time_graph(),
        )

        bus_frm.grid(row=0, column=1)

        start_stop_picker.grid(column=0, row=1, padx=(0, 10))
        finish_stop_picker.grid(column=1, row=1)
        start_stop_lbl.grid(column=0, row=0)
        finish_stop_lbl.grid(column=1, row=0)

        start_finish_frm.grid(row=1, column=1)
        days_frm.grid(row=2, column=1)
        run_butt.grid(row=3, column=1)

        tab_parent.pack(expand=True, fill="both")
        root.pack(expand=True, fill="both")
