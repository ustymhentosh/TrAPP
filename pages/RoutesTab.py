import tkinter as tk
import ttkbootstrap as ttk
import os
import json
from tools.routes_analysis import get_commute_time, _plot_and_save_dct
from tools.map_builder import create_map
import webbrowser


class RoutesTab(ttk.Frame):
    def __init__(self, master, main_dir):
        ttk.Frame.__init__(self, master)
        root = ttk.Frame(master=self)
        self.main_dir = main_dir
        self.comp_dir = ".organized_gps"

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
                self.comp_dir + "/" + str(self.selected_bus.get()),
                str(self.selected_bus.get()),
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
            run_butt["text"] = "отримати"
            run_butt["state"] = tk.ACTIVE

        def create_route_time_graph():
            run_butt["text"] = "у роботі"
            run_butt["state"] = tk.DISABLED
            start_plot_route()

        def build_map():
            create_map(
                get_stops_for_bus(),
                "./additional_data/current_map.html",
                bus_pick.get(),
            )
            url = f"file://{os.getcwd()}/additional_data/current_map.html"
            # url = "file://d/testdata.html"
            webbrowser.open(url, new=2)

        self.map_pht = ttk.PhotoImage(file="images/map_icon.svg.png")
        self.map_sized = self.map_pht.subsample(10, 10)

        self.selected_start_stop = tk.StringVar()
        self.selected_finish_stop = tk.StringVar()

        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        root.rowconfigure(3, weight=1)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)

        bus_frm = ttk.Frame(master=root)
        bus_frm.columnconfigure(0, weight=1)
        bus_frm.columnconfigure(1, weight=1)
        bus_lbl = ttk.Label(
            master=bus_frm, text="№ маршруту", font="Calibri 14", style="primary"
        )
        self.selected_bus = tk.StringVar()
        bus_pick = ttk.Combobox(
            master=bus_frm,
            values=os.listdir(self.comp_dir),
            font="Calibri 14",
            width=10,
            textvariable=self.selected_bus,
        )
        map_link = ttk.Button(
            master=bus_frm,
            image=self.map_sized,
            style="primary.outline",
            command=build_map,
        )
        bus_pick.bind("<<ComboboxSelected>>", on_field_change)
        bus_lbl.grid(column=0, row=0, sticky="sw")
        bus_pick.grid(column=0, row=1, sticky="sw")
        map_link.grid(column=0, row=0, rowspan=2, sticky="s", padx=(80, 0))

        start_finish_frm = ttk.Frame(master=root)
        start_stop_lbl = ttk.Label(
            master=start_finish_frm, text="початкова зупинка", style="primary"
        )
        start_stop_picker = ttk.Combobox(
            master=start_finish_frm,
            values=get_stops_for_bus(),
            font="Calibri 14",
            textvariable=self.selected_start_stop,
        )
        finish_stop_lbl = ttk.Label(
            master=start_finish_frm, text="кінцева зупинка", style="primary"
        )
        finish_stop_picker = ttk.Combobox(
            master=start_finish_frm,
            values=get_stops_for_bus(),
            font="Calibri 14",
            textvariable=self.selected_finish_stop,
        )

        days_frm = ttk.Frame(master=root)
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
            master=days_frm,
            text="Пн",
            variable=self.mon_var,
            onvalue=1,
            style="info",
        )
        tue = ttk.Checkbutton(
            master=days_frm,
            text="Вт",
            variable=self.tue_var,
            onvalue=1,
            style="info",
        )
        wed = ttk.Checkbutton(
            master=days_frm,
            text="Ср",
            variable=self.wed_var,
            onvalue=1,
            style="info",
        )
        thr = ttk.Checkbutton(
            master=days_frm,
            text="Чт",
            variable=self.thr_var,
            onvalue=1,
            style="info",
        )
        fri = ttk.Checkbutton(
            master=days_frm,
            text="Пт",
            variable=self.fri_var,
            onvalue=1,
            style="info",
        )
        sat = ttk.Checkbutton(
            master=days_frm,
            text="Сб",
            variable=self.sat_var,
            onvalue=1,
            style="info",
        )
        sun = ttk.Checkbutton(
            master=days_frm,
            text="Нд",
            variable=self.sun_var,
            onvalue=1,
            style="info",
        )

        mon.grid(row=0, column=0, padx=(0, 5), pady=5)
        tue.grid(row=0, column=1, padx=5, pady=5)
        wed.grid(row=0, column=2, padx=5, pady=5)
        thr.grid(row=0, column=3, padx=5, pady=5)
        fri.grid(row=0, column=4, padx=5, pady=5)
        sat.grid(row=0, column=5, padx=5, pady=5)
        sun.grid(row=0, column=6, padx=5, pady=5)

        sep = ttk.Separator(master=root)

        run_butt = ttk.Button(
            master=root,
            text="отримати",
            style="success.outline",
            command=create_route_time_graph,
        )

        bus_frm.grid(row=0, column=0, sticky="ew", columnspan=2)

        start_stop_lbl.grid(column=0, row=0, sticky="w")
        finish_stop_lbl.grid(column=1, row=0, sticky="w")
        start_stop_picker.grid(column=0, row=1, padx=(0, 10))
        finish_stop_picker.grid(column=1, row=1)

        start_finish_frm.grid(row=1, column=0, sticky="w")
        days_frm.grid(row=2, column=0, sticky="w")
        sep.grid(row=3, column=0, columnspan=4, sticky=tk.NSEW)
        run_butt.grid(row=4, column=0, columnspan=4, sticky=tk.E)

        root.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=20,
        )
