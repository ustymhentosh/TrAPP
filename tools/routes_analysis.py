import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import json

plt.style.use("default")


def _plot_and_save_dct(dct, plot_name, fl_nm):
    """
    Plots commute time
    """
    hours = [i for i in dct.keys() if len(dct[i]) > 2]
    times = [np.mean(dct[item]) for item in hours]
    std_devs = [np.std(dct[item]) for item in hours]
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
    plt.show()


def get_commute_time(
    path: str,
    num: str,
    start_station: str,
    finish_station: str,
    days=[0, 1, 2, 3, 4],
):
    format_string = "%Y/%m/%d %H:%M"
    results = {}
    for i in range(6, 23):
        results[i] = []

    for i in days:
        with open(f"{path}/{num}_segments_{i}.json", encoding="utf-8") as f:
            dct = json.load(f)

        for one_bus in dct.keys():
            is_start = False
            for moment in dct[one_bus]:
                if moment[0] == start_station:
                    start = datetime.strptime(moment[1], format_string)
                    is_start = True
                elif is_start and moment[0] == finish_station:
                    end = datetime.strptime(moment[1], format_string)
                    if start.date() == end.date():
                        c = end - start
                        minutes = c.total_seconds() / 60
                        if start.hour in results.keys() and 100 > minutes > 0:
                            results[start.hour].append(minutes)
    return results


if __name__ == "__main__":

    dct = get_commute_time(
        ".organized_gps/3А", "3А", "ТРЦ Кінг Кросс (320)", "Податкова (428)"
    )
    _plot_and_save_dct(dct, "від Кінг-Крос до Податкової(понеділок)", "plots/test.png")
