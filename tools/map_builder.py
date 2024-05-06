import os
import folium
import pandas as pd
import matplotlib.pyplot as plt


def create_map(stops_list, file_name, bus_num):
    # Define custom tile layer without labels
    CartoDB_VoyagerNoLabels = folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png",
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains="abcd",
        max_zoom=20,
    )

    m = folium.Map(location=[49.8397, 24.0297], zoom_start=12)
    CartoDB_VoyagerNoLabels.add_to(m)

    def parse_csv_file(csv_file):
        df = pd.read_csv(csv_file)
        return [
            ((row["stop_lat"], row["stop_lon"]), row["stop_name"])
            for _, row in df.iterrows()
        ]

    stops = parse_csv_file("./additional_data/stops.csv")

    for coord in stops:
        if coord[1] in stops_list:
            c = folium.CircleMarker(
                coord[0],
                radius=2,
                color="blue",
                fill=True,
                fill_color="blue",
                fill_opacity=0.6,
                popup=coord[1],
                tooltip=coord[1],
            ).add_to(m)

    title_html = f"""
             <h4 align="center" style="font-size:20px; font-family:Calibri;"><b>Маршрут - {bus_num}</b></h4>
             """
    m.get_root().html.add_child(folium.Element(title_html))
    m.save(file_name)
