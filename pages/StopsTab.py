import tkinter as tk
import ttkbootstrap as ttk
import os
import json
import threading
from tools.station_analysis import create_plot_for_one_bus_one_stop_intrv


class StopsTab(ttk.Frame):
    def __init__(self, master, main_dir):
        ttk.Frame.__init__(self, master)
        root = ttk.Frame(master=self)
        self.main_dir = main_dir
        self.comp_dir = ".organized_gps"
        self.main_dct = self.load_main_dct()

        def on_field_change(_):
            bus_pick["values"] = self.main_dct[self.selected_stop.get()]

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
            run_butt["text"] = "Отримати"
            run_butt["state"] = tk.ACTIVE
            master.event_generate("<<PlotingFinished>>", when="tail")

        def create_stop_time_graph():
            run_butt["text"] = "⏳ у роботі ⏳"
            run_butt["state"] = tk.DISABLED
            plotting_thread = threading.Thread(target=start_plot_stop, args=())
            plotting_thread.start()

        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        root.rowconfigure(3, weight=1)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)

        self.selected_stop = tk.StringVar()
        self.selected_bus = tk.StringVar()

        stop_f = ttk.Frame(master=root)
        stop_l = ttk.Label(master=stop_f, text="зупинка")
        stop_pick = ttk.Combobox(
            master=stop_f,
            values=list(self.main_dct.keys()),
            font="Calibri 14",
            width=20,
            textvariable=self.selected_stop,
        )
        stop_pick.bind("<<ComboboxSelected>>", on_field_change)
        stop_l.pack()
        stop_pick.pack()

        bus_f = ttk.Frame(master=root)
        bus_l = ttk.Label(master=bus_f, text="маршрут")
        bus_pick = ttk.Combobox(
            master=bus_f,
            values=[],
            font="Calibri 14",
            width=10,
            textvariable=self.selected_bus,
        )
        bus_l.pack()
        bus_pick.pack()

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

        self.selected_st = tk.StringVar()
        self.selected_st.set("початкова година")
        start_hours_f = ttk.Frame(master=root)
        start_l = ttk.Label(master=start_hours_f, text="З")
        start_h = ttk.OptionMenu(
            master=start_hours_f,
            variable=self.selected_st,
            style="info.Outline.TMenubutton",
            command=self.update_title,
        )
        start_menu = tk.Menu(start_h)
        for option in [f"{i}:00" for i in range(6, 23)]:
            start_menu.add_radiobutton(
                label=option, value=option, variable=self.selected_st
            )
        start_h["menu"] = start_menu
        start_l.pack(side="left", padx=10)
        start_h.pack(side="right")

        self.selected_fn = tk.StringVar()
        self.selected_fn.set("кінцева година")
        finish_hours_f = ttk.Frame(master=root)
        fin_l = ttk.Label(master=finish_hours_f, text="До")
        finish_h = ttk.OptionMenu(
            master=finish_hours_f,
            variable=self.selected_fn,
            style="info.Outline.TMenubutton",
            command=self.update_title,
        )
        fin_menu = tk.Menu(finish_h)
        for option in [f"{i}:00" for i in range(6, 23)]:
            fin_menu.add_radiobutton(
                label=option, value=option, variable=self.selected_fn
            )
        finish_h["menu"] = fin_menu
        fin_l.pack(side="left", padx=10)
        finish_h.pack(side="right")

        run_butt = ttk.Button(
            master=root,
            text="отримати",
            style="success",
            command=lambda: create_stop_time_graph(),
        )

        stop_f.grid(row=0, column=0, padx=10)
        bus_f.grid(row=0, column=1)
        days_frm.grid(row=1, column=0, columnspan=4)
        start_hours_f.grid(row=2, column=0)
        finish_hours_f.grid(row=2, column=1)
        run_butt.grid(row=3, column=0, columnspan=4)

        root.pack(expand=True, fill="both")

    def load_main_dct(self):
        with open("stops_dct.json", "r", encoding="utf-8") as f:
            dct = json.load(f)
        return dct

    def update_title(self, selected_option):
        self.selected_st.set(selected_option)
