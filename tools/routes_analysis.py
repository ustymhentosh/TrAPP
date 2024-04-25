import matplotlib.pyplot as plt
from datetime import datetime
import os
import numpy as np
import json
import networkx as nx


def str_list_time(tm):
    res = ""
    for i in tm:
        res += "-" + str(i)
    return res


def _plot_and_save_dct(dct, plot_name, fl_nm):
    """
    Plots commute time
    """
    hours = list(dct.keys())
    times = [item[0] for item in dct.values()]
    std_devs = [item[1] for item in dct.values()]

    avg_time = np.mean(times)
    avg_std_dev = np.mean(std_devs)

    plt.figure(figsize=(10, 5))
    plt.plot(hours, times, marker="o", label="Час поїздки")
    plt.errorbar(
        hours,
        times,
        yerr=std_devs,
        fmt="o",
        label=f"Похибка (середня {avg_std_dev:.2f})",
    )
    plt.axhline(
        avg_time, linestyle="--", color="blue", label=f"Середній час: {avg_time:.2f}"
    )
    plt.xlabel("Час дня")
    plt.ylabel("Час поїздки")
    plt.title(plot_name)
    plt.legend()
    plt.grid(True)

    for hour, time in zip(hours, times):
        plt.text(
            hour + 0.1,
            time + 0.5,
            f"{time:.2f}",
            fontsize=8,
            color="black",
        )

    plt.savefig(fl_nm)
    plt.show()


def merge_dicts(dict1, dict2):
    merged_dict = {}
    all_keys = set(dict1.keys()) | set(dict2.keys())

    for key in all_keys:
        values1 = dict1.get(key, {})
        values2 = dict2.get(key, {})

        merged_values = {}
        for sub_key, sub_list in values1.items():
            merged_values[sub_key] = sub_list.copy()
        for sub_key, sub_list in values2.items():
            if sub_key in merged_values:
                merged_values[sub_key].extend(sub_list)
            else:
                merged_values[sub_key] = sub_list.copy()

        merged_dict[key] = merged_values

    return merged_dict


def _get_only_needed_segments_times(file_path, needed_segments):
    resulted_dct = {}
    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as f:
        main_dct = json.load(f)
    for sgm_nm in needed_segments:
        resulted_dct[sgm_nm] = main_dct[sgm_nm]
    return resulted_dct


def create_plot_for_one_bus_segment(
    data_folder_path: str,
    bus_name: str,
    start_stop: str,
    end_stop: str,
    days: list,
    name_of_the_plot=None,
):
    """
    Creates graph for segment time for on ebus
    Args:
        data_folder_path (str): folder with json data
        bus_name (str): name of the bus
        days (list): [0, 2, 3 ...]
    """
    for i in range(0, 6):
        with open(
            f"{data_folder_path}{os.sep}{bus_name}{os.sep}{bus_name}_segments_{i}.json",
            "r",
            encoding="utf-8",
        ) as f:
            if i:
                all_segments.intersection(set(json.load(f).keys()))
            else:
                all_segments = set(json.load(f).keys())

    all_segments = list(all_segments)

    nx_grph = nx.DiGraph()
    for segment in [i.split("|||") for i in all_segments]:
        nx_grph.add_edge(segment[0], segment[1], weight=1)

    shortest_path = nx.dijkstra_path(nx_grph, start_stop, end_stop, weight="weight")
    needed_segments = [
        f"{shortest_path[i]}|||{shortest_path[i+1]}"
        for i in range(len(shortest_path) - 1)
    ]
    all_segment_times = {}
    for i in needed_segments:
        all_segment_times[i] = {}

    for day in days:
        file_path = f"{data_folder_path}{os.sep}{bus_name}{os.sep}{bus_name}_segments_{day}.json"
        all_segment_times = merge_dicts(
            _get_only_needed_segments_times(file_path, needed_segments),
            all_segment_times,
        )

    results = {}
    for hour in range(7, 22):
        avarage_for_hour = 0
        sd_for_hour = 0
        for segment in needed_segments:
            if all_segment_times.get(segment) and all_segment_times[segment].get(
                str(hour)
            ):
                times = []
                for i in all_segment_times[segment][str(hour)]:
                    if i > 0:
                        times.append(i / 60)
                    else:
                        times.append(0.5)
                print(segment, times)
                avarage_for_hour += sum(times) / len(times)
                sd_for_hour += np.std(times)
        results[hour] = [avarage_for_hour, sd_for_hour]

    if not name_of_the_plot:
        _plot_and_save_dct(
            results,
            f"Час руху маршуту {bus_name} із {start_stop} до {end_stop} у дні {days}",
            f"plots/{bus_name} {start_stop}-{end_stop} дні {str_list_time(days)}",
        )
    else:
        _plot_and_save_dct(results, name_of_the_plot)


if __name__ == "__main__":
    create_plot_for_one_bus_segment(
        ".organized_data",
        "3А",
        "Іподром (434)",
        "Податкова (428)",
        [0, 1, 2],
    )
