import tkinter as tk
import ttkbootstrap as ttk
import os
import json
import threading
from tools.station_analysis import create_plot_for_one_bus_one_stop_intrv
import matplotlib.pyplot as plt


class StopsTab(ttk.Frame):
    def __init__(self, master, main_dir):
        ttk.Frame.__init__(self, master)
        root = ttk.Frame(master=self)
        self.main_dir = main_dir
        self.comp_dir = ".organized_gps"
        self.main_dct = self.load_main_dct()

        def on_field_change(_):
            bus_pick["values"] = sorted(self.main_dct[self.selected_stop.get()])

        def start_plot_stop():
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
            selected_abbreviations = [
                day_abbreviations[index] for index in self.selected_days
            ]
            hours = [
                i
                for i in range(
                    int(self.selected_st.get()[:-3]),
                    int(self.selected_fn.get()[:-3]) + 1,
                )
            ]
            answ = "".join(selected_abbreviations)
            title = f"Інтервали прибуття маршруту {self.selected_bus.get()} на зупинку {self.selected_stop.get()}, дні: {answ}, години: {hours}"
            create_plot_for_one_bus_one_stop_intrv(
                self.comp_dir,
                self.selected_stop.get(),
                self.selected_bus.get(),
                self.selected_days,
                hours,
                title,
                "plots/plot_type_2.png",
                bound=60,
            )
            run_butt["text"] = "отримати"
            run_butt["state"] = tk.ACTIVE

        def create_stop_time_graph():
            run_butt["text"] = "⏳ у роботі ⏳"
            run_butt["state"] = tk.DISABLED
            try:
                start_plot_stop()
            except:
                run_butt["text"] = "отримати"
                run_butt["state"] = tk.ACTIVE

        # Set page grid
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        root.rowconfigure(3, weight=1)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)

        # Create stop and bus fields
        self.selected_stop = tk.StringVar()
        self.selected_bus = tk.StringVar()

        top_frm = ttk.Frame(master=root)
        stop_f = ttk.Frame(master=top_frm)
        stop_l = ttk.Label(master=stop_f, text="Зупинка", style="primary")
        stop_pick = ttk.Combobox(
            master=stop_f,
            values=sorted(list(self.main_dct.keys())),
            font="Calibri 14",
            width=20,
            textvariable=self.selected_stop,
        )
        stop_pick.bind("<<ComboboxSelected>>", on_field_change)
        stop_l.grid(column=0, row=0, sticky="w")
        stop_pick.grid(column=0, row=1, sticky="w")

        bus_f = ttk.Frame(master=top_frm)
        bus_l = ttk.Label(master=bus_f, text="№ маршруту", style="primary")
        bus_pick = ttk.Combobox(
            master=bus_f,
            values=[],
            font="Calibri 14",
            width=10,
            textvariable=self.selected_bus,
        )
        bus_l.grid(column=0, row=0, sticky="w")
        bus_pick.grid(column=0, row=1, sticky="w")

        # Create days picker
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
            master=days_frm, text="Пн", variable=self.mon_var, onvalue=1, style="info"
        )
        tue = ttk.Checkbutton(
            master=days_frm, text="Вт", variable=self.tue_var, onvalue=1, style="info"
        )
        wed = ttk.Checkbutton(
            master=days_frm, text="Ср", variable=self.wed_var, onvalue=1, style="info"
        )
        thr = ttk.Checkbutton(
            master=days_frm, text="Чт", variable=self.thr_var, onvalue=1, style="info"
        )
        fri = ttk.Checkbutton(
            master=days_frm, text="Пт", variable=self.fri_var, onvalue=1, style="info"
        )
        sat = ttk.Checkbutton(
            master=days_frm, text="Сб", variable=self.sat_var, onvalue=1, style="info"
        )
        sun = ttk.Checkbutton(
            master=days_frm, text="Нд", variable=self.sun_var, onvalue=1, style="info"
        )

        mon.grid(row=0, column=0, padx=(0, 5), pady=5)
        tue.grid(row=0, column=1, padx=5, pady=5)
        wed.grid(row=0, column=2, padx=5, pady=5)
        thr.grid(row=0, column=3, padx=5, pady=5)
        fri.grid(row=0, column=4, padx=5, pady=5)
        sat.grid(row=0, column=5, padx=5, pady=5)
        sun.grid(row=0, column=6, padx=5, pady=5)

        # Create Hours picker
        hour_pick = ttk.Frame(master=root)
        self.selected_st = tk.StringVar()
        self.selected_st.set("поч. год.")
        start_hours_f = ttk.Frame(master=hour_pick)
        start_l = ttk.Label(master=start_hours_f, text="з", style="primary")
        start_h = ttk.OptionMenu(
            master=start_hours_f,
            variable=self.selected_st,
            style="dark.Outline.TMenubutton",
            command=self.update_title,
        )
        start_menu = tk.Menu(start_h)
        for option in [f"{i}:00" for i in range(6, 23)]:
            start_menu.add_radiobutton(
                label=option, value=option, variable=self.selected_st
            )
        start_h["menu"] = start_menu
        start_l.grid(column=0, row=0, sticky="w")
        start_h.grid(column=0, row=1, sticky="w")

        self.selected_fn = tk.StringVar()
        self.selected_fn.set("кнц. год.")
        finish_hours_f = ttk.Frame(master=hour_pick)
        fin_l = ttk.Label(master=finish_hours_f, text="до", style="primary")
        finish_h = ttk.OptionMenu(
            master=finish_hours_f,
            variable=self.selected_fn,
            style="dark.Outline.TMenubutton",
            command=self.update_title,
        )
        fin_menu = tk.Menu(finish_h)
        for option in [f"{i}:00" for i in range(6, 23)]:
            fin_menu.add_radiobutton(
                label=option, value=option, variable=self.selected_fn
            )
        finish_h["menu"] = fin_menu
        fin_l.grid(column=0, row=0, sticky="w")
        finish_h.grid(column=0, row=1, sticky="w")

        sep = ttk.Separator(master=root)

        # Get button
        run_butt = ttk.Button(
            master=root,
            text="отримати",
            style="success.outline",
            command=lambda: create_stop_time_graph(),
        )

        # Packing
        stop_f.grid(row=0, column=0, sticky="w")
        bus_f.grid(row=0, column=1, sticky="w", padx=10)
        top_frm.grid(row=0, column=0, sticky="w", columnspan=4)
        days_frm.grid(row=2, column=0, columnspan=4, sticky="w")

        hour_pick.grid(row=1, column=0, sticky="w", columnspan=4)
        start_hours_f.grid(row=0, column=0, sticky="w")
        finish_hours_f.grid(row=0, column=1, sticky="w", padx=10)

        sep.grid(row=3, column=0, columnspan=4, sticky=tk.NSEW)
        run_butt.grid(row=4, column=0, columnspan=4, sticky=tk.E)

        def log(_):
            # self.plotting_thread.join()
            for thread in threading.enumerate():
                print(thread.name)

        root.bind("<<PlotingFinished>>", lambda x: log("w"))
        root.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=20,
        )

    def load_main_dct(self):
        with open("stops_dct.json", "r", encoding="utf-8") as f:
            dct = json.load(f)
        return dct

    def update_title(self, selected_option):
        self.selected_st.set(selected_option)
