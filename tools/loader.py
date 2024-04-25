import pandas as pd
import os
from datetime import datetime
import json
from tqdm import tqdm
from pathlib import Path


def extract_and_organize_one_route(
    route_file_path: str, skip_rows: int, save_folder_path: str, bus_name: str
):
    """
    From raw xlsx file of one bus/tram... creates clean folder for further work
    ##### Args:
        route_file_path (str): path to xlsx file
        skip_rows (int): how many Excel rows to skip
        save_folder_path (str): in which folder to save jsons
        bus_name(str): bus name
    ##### Returns:
        bool: True if success False -> fail
    """
    format_string = "%Y/%m/%d %H:%M"
    df = pd.read_excel(route_file_path, skiprows=skip_rows)
    unique_stops = set()
    # unique_segments = set()
    # segments = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}
    stops_detected = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}
    bad_count = 0
    good_count = 0

    # previous_stop_name_time = []
    for i, value in df.iterrows():
        # mark unique stops
        stop_name = value.iloc[0]
        unique_stops.add(stop_name)
        stop_time_or_not = value.iloc[1]
        try:
            stop_time = datetime.strptime(stop_time_or_not, format_string)
            stop_day = stop_time.weekday()
            stop_hour = stop_time.hour

            # mark instop presence
            if stops_detected[stop_day].get(stop_name):
                stops_detected[stop_day][stop_name].append(
                    stop_time.strftime(format_string)
                )
            else:
                stops_detected[stop_day][stop_name] = [
                    stop_time.strftime(format_string)
                ]

            # # mark segment
            # if previous_stop_name_time:
            #     previous_time = previous_stop_name_time[1]
            #     if stop_time.date() == previous_time.date():
            #         segment_time = stop_time - previous_time
            #         segment_time = segment_time.total_seconds()
            #         segment_name = f"{previous_stop_name_time[0]}|||{stop_name}"
            #         unique_segments.add(segment_name)
            #         if abs(segment_time) > 3600:
            #             bad_count += 1
            #         else:
            #             good_count += 1
            #             if segments[stop_day].get(segment_name):
            #                 if segments[stop_day][segment_name].get(stop_hour):
            #                     segments[stop_day][segment_name][stop_hour].append(
            #                         segment_time
            #                     )
            #                 else:
            #                     segments[stop_day][segment_name][stop_hour] = [
            #                         segment_time
            #                     ]
            #             else:
            #                 segments[stop_day][segment_name] = {
            #                     stop_hour: [segment_time]
            #                 }
            # previous_stop_name_time = [stop_name, stop_time]

        except Exception as c:
            previous_stop_name_time = []
            # print(c)
    print(bad_count, good_count)
    # for day in range(6):
    #     with open(
    #         f"{save_folder_path}{os.sep}{bus_name}_segments_{day}.json",
    #         "w",
    #         encoding="utf-8",
    #     ) as f:
    #         json.dump(segments[day], f, indent=4, ensure_ascii=False)
    for day in range(7):
        with open(
            f"{save_folder_path}{os.sep}{bus_name}_stops_{day}.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(stops_detected[day], f, indent=4, ensure_ascii=False)

    with open(
        f"{save_folder_path}{os.sep}{bus_name}_all_stops.json", "w", encoding="utf-8"
    ) as f:
        json.dump(list(unique_stops), f, indent=4, ensure_ascii=False)

    return True


def extract_info_from_all_available_routes(
    path_to_excels_folder: str, path_to_results_fldr: str
):
    """
    For each excel file in the folder generates organized json stats
    Args:
        path_to_excles_folder (str): path to folder with excels
        path_to_excles_folder (str): path to folder where organized files will be stored
    """

    for i in tqdm(os.listdir(path_to_excels_folder)):
        if not os.path.exists(f"{path_to_results_fldr}/{Path(i).stem}/"):
            os.makedirs(f"{path_to_results_fldr}/{Path(i).stem}/")
        extract_and_organize_one_route(
            os.path.join(path_to_excels_folder, i),
            4,
            f"{path_to_results_fldr}/{Path(i).stem}",
            Path(i).stem,
        )


if __name__ == "__main__":
    extract_info_from_all_available_routes("./../data/raw_data", ".organized_data")
