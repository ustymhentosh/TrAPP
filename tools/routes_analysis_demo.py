import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


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

    plt.savefig(fl_nm)
    plt.show()


def get_commute_time(
    path: str,
    start_station: str,
    finish_station: str,
    days=[0, 1, 2, 3, 4],
):

    df = pd.read_excel(path, skiprows=4)
    format_string = "%Y/%m/%d %H:%M"
    results = {}
    for i in range(6, 23):
        results[i] = []

    for index, row in df.iterrows():
        if row.iloc[0] == start_station:
            try:
                start = datetime.strptime(row.iloc[1], format_string)
            except Exception as error:
                # print("An exception occurred:", error)
                continue

        elif row.iloc[0] == finish_station:
            try:
                end = datetime.strptime(row.iloc[1], format_string)
                if start.date() == end.date():
                    c = end - start
                    minutes = c.total_seconds() / 60
                    if start.weekday() in days:
                        if start.hour in results.keys() and 100 > minutes > 0:
                            results[start.hour].append(minutes)
            except Exception as error:
                # print("An exception occurred:", error)
                continue
    return results


if __name__ == "__main__":

    dct = get_commute_time(
        "./../data/raw_data/18.xlsx", "Низинна (195)", "Податкова (428)"
    )

    _plot_and_save_dct(dct, "Some plot", "plots/test.png")
