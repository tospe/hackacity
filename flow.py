import pandas as pd
from pathlib import Path
from datetime import datetime
import numpy as np
from sklearn.model_selection import train_test_split

DATA_ROOT = Path(__file__).resolve().parents[3].joinpath("data")

def data_prep():
    scooters = pd.read_csv(str(DATA_ROOT.joinpath("raw", "e-scooters", "od_view.csv")))

    scooters_trips = scooters.loc[scooters["event_types"] == "{trip_start}"]
    scooters_trips_end = scooters.loc[scooters["event_types"] == "{trip_end}"]

    scooters_trips["trip_start_lat"] = scooters_trips["lat"]
    scooters_trips["trip_start_lng"] = scooters_trips["lng"]

    for idx, row in scooters_trips.iterrows():
        trip_id = row["trip_id"]
        trip_end = scooters_trips_end.loc[scooters_trips_end["trip_id"] == trip_id]

        if len(trip_end) == 0:
            continue
        else:
            trip_end = trip_end.iloc[0]


        scooters_trips.at[idx, "trip_end_lat"] = trip_end["lat"]
        scooters_trips.at[idx, "trip_end_lng"] = trip_end["lng"]
        
    scooters_trips = scooters_trips[["timestamp", "trip_id", "lat", "lng"]]
    print(scooters_trips)

def scooter_prep():
    scooters = pd.read_csv(str(DATA_ROOT.joinpath("raw", "e-scooters", "od_view.csv")))
    scooters = scooters[["timestamp", "trip_id", "event_types", "lat", "lng"]]
    scooters["timestamp"] = pd.to_datetime(scooters["timestamp"], unit="ms")
    scooters.drop(scooters.loc[scooters["timestamp"].dt.year < 2021].index, inplace=True)

    scooters.loc[scooters["event_types"] == "{trip_start}"].to_csv(str(DATA_ROOT.joinpath("processed", "trip_starts.csv")), index=False)
    scooters.loc[scooters["event_types"] == "{trip_end}"].to_csv(str(DATA_ROOT.joinpath("processed", "trip_ends.csv")), index=False)

    return scooters

def ap_prep():
    aps = pd.read_csv(str(DATA_ROOT.joinpath("raw", "wifi-ap", "devices_per_ap.csv")), delimiter=";")
    mac2coords = pd.read_csv(str(DATA_ROOT.joinpath("raw", "wifi-ap", "ap_mac_to_coordinates.csv")), delimiter=";")

    aps = aps.join(mac2coords.set_index("Access_Points"), on="Access_Point")
    aps.drop(aps.loc[aps["Coordinates"] == "Not Available"].index, inplace=True)
    aps["Date_day"] = pd.to_datetime(aps["Date_day"], format="%d/%m/%Y")
    aps.dropna(inplace=True)
    aps.drop(aps.loc[aps["Date_day"].dt.year < 2021].index, inplace=True)
    aps.drop(aps[~aps["Coordinates"].str.contains(r"\[(-?[0-9]+(?:\.-?[0-9]+)?), (-?[0-9]+(?:\.-?[0-9]+)?)\]")].index, inplace=True)
    aps["lng"] = aps["Coordinates"].str.extract(r"\[(-?[0-9]+(?:\.-?[0-9]+)?), -?[0-9]+(?:\.-?[0-9]+)?\]")
    aps["lat"] = aps["Coordinates"].str.extract(r"\[-?[0-9]+(?:\.-?[0-9]+)?, (-?[0-9]+(?:\.-?[0-9]+)?)\]")
    aps = aps[["Access_Point", "Date_day", "count_total", "lat", "lng"]]
    aps = pd.DataFrame(np.repeat(aps.values, aps["count_total"].values, axis=0))
    aps.columns = ["Access_Point", "Date_day", "count_total", "lat", "lng"]
    
    _, x_test, _, y_test = train_test_split(aps[["Date_day", "count_total", "lat", "lng"]], aps["Access_Point"], stratify=aps["Access_Point"], test_size=0.06)
    aps = pd.DataFrame(x_test)
    aps.columns = ["Date_day", "count_total", "lat", "lng"]
    aps["Access_Point"] = y_test
    aps.drop("count_total", axis=1, inplace=True)
    
    aps.to_csv(str(DATA_ROOT.joinpath("processed", "wifi-aps.csv")), index=None)

if __name__ == "__main__":
    ap_prep()