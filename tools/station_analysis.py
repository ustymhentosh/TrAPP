import matplotlib.pyplot as plt
from datetime import datetime
import os
import numpy as np
import json


def _get_only_needed_stop_times_from_file(file_path: str, stop_name: str):
    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as f:
        stops_times = json.load(f)
    return stops_times[stop_name]


def _get_intervals_closes_for_times_with_respect_to_days(all_times: list, hours: list):
    format_string = "%Y/%m/%d %H:%M"
    resulting_times = []
    all_times = sorted(all_times, key=lambda x: datetime.strptime(x, format_string))
    for i in range(len(all_times)):
        if i != 0:
            curr_time = datetime.strptime(all_times[i], format_string)
            prev_time = datetime.strptime(all_times[i - 1], format_string)
            if prev_time.hour in hours and prev_time.date() == curr_time.date():
                resulting_times.append(
                    (abs(curr_time - prev_time)).total_seconds() / 60
                )
    return resulting_times


def str_list_time(tm):
    res = ""
    for i in tm:
        res += "-" + str(i)
    return res


def _create_plot_type_1(
    intervals: list, plot_name, bus, stop_name, time, days, save_path
):

    plt.hist(intervals, color="lightgreen", ec="black", bins=30)

    # Calculate mean, median, and standard deviation
    mean_val = np.mean(intervals)
    median_val = np.median(intervals)
    std_dev = np.std(intervals)

    # Add vertical lines for mean, median, and standard deviation
    plt.axvline(
        mean_val,
        color="red",
        linestyle="dashed",
        linewidth=1,
        label=f"Середнє: {mean_val:.2f}",
    )
    plt.axvline(
        median_val,
        color="blue",
        linestyle="dashed",
        linewidth=1,
        label=f"Медіана: {median_val:.2f}",
    )
    plt.axvline(
        mean_val + std_dev,
        color="purple",
        linestyle="dashed",
        linewidth=1,
        label=f"Відхилення: {std_dev:.2f}",
    )
    plt.axvline(mean_val - std_dev, color="purple", linestyle="dashed", linewidth=1)
    plt.legend()
    plt.title(plot_name)
    plt.xlabel("Інтервал у хвилинах")
    plt.ylabel("Кількість випадків за місяць")

    # plt.savefig(
    #     f"plots/{bus} {stop_name} години {str_list_time(time)} дні {str_list_time(days)}"
    # )
    plt.show()


def create_plot_for_one_bus_one_stop_intrv(
    data_folder_path: str,
    stop_name: str,
    bus_name: str,
    days: list,
    hours: list,
    title: str,
    save_path: str,
    bound: int,
):
    """
    Creates and returns plot for stop intervals of one bus at one stop
    Args:
        data_folder_path (str): folder with data
        stop_name (str): name of the analyzed stop
        bus_name (str): bus route name
        days (list): days list ex [0, 1, 2] = mon, tue, wed
        hours (list): hours ex [7, 8, 9]
        title: str
        save_path: str
    Returns:
        list: all intervals of bus stoping there and then
    """
    with open(
        f"{data_folder_path}{os.sep}{bus_name}{os.sep}{bus_name}_all_stops.json",
        "r",
        encoding="utf-8",
    ) as f:
        stops_for_bus = json.load(f)

    all_times = []
    if stop_name in stops_for_bus:
        for day in days:
            file_path = f"{data_folder_path}{os.sep}{bus_name}{os.sep}{bus_name}_stops_{day}.json"
            all_times.extend(
                _get_only_needed_stop_times_from_file(file_path, stop_name)
            )

    intervals = _get_intervals_closes_for_times_with_respect_to_days(all_times, hours)
    # plot_name = f"Інтервал руху маршуту {bus_name} на зупинці {stop_name}\nчас -> {hours}, дні {days}"
    intervals = [i for i in intervals if i < bound]
    _create_plot_type_1(intervals, title, bus_name, stop_name, hours, days, save_path)


def _helper_get_stations_routes_dct(or_data: str, out_put: str):
    result = {}
    for i in os.listdir(or_data):
        with open(f"{or_data}/{i}/{i}_all_stops.json", "r", encoding="utf-8") as f:
            one_dct = json.load(f)
            for j in one_dct:
                if result.get(j):
                    result[j].append(i)
                else:
                    result[j] = [i]
    with open(out_put, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)


# _helper_get_stations_routes_dct(".organized_data", "stops_dct.json")

# create_plot_for_one_bus_one_stop_intrv(
#     ".organized_data", "Сокільницька (435)", "3А", [0, 1, 2], [10, 11, 12, 13, 14], 40
# )
