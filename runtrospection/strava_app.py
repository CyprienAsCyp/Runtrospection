from dataclasses import dataclass
from datetime import datetime
import requests
import polyline
import streamlit as st
from io import BytesIO
import pandas as pd
import json
from runtrospection.constants import (
    CLIENT_SECRET,
    CLIENT_ID,
    URL_ACTIVITIES,
    URL_LAPS,
    URL_ACTIVITY,
    DATETIME_FORMAT,
    DEFAULT_START,
    DEFAULT_END,
)


@dataclass
class StravaApp:
    database_file: BytesIO
    access_token: str = ""
    client_id: str = CLIENT_ID
    client_secret: str = CLIENT_SECRET

    def __post_init__(self):
        jsonFile = self.database_file.read()
        data = json.load(jsonFile)
        self.df_activities = pd.DataFrame(data=data["activities"])

    def get_new_activities_list(self) -> list[dict[str, str]]:
        start = self.compute_start_timestamp(df=self.df_activities)
        end = int(DEFAULT_END)
        page = 1
        activities = []
        page_records = self.get_activities(start, end, page)
        activities.extend(page_records)
        while len(page_records) == 30:
            page += 1
            page_records = self.get_activities(start, end, page)
            activities.extend(self.get_activities(start, end, page))
        return activities

    def get_activities(self, start: int, end: int, page: int):
        url_activities = URL_ACTIVITIES
        params = {"before": end, "after": start, "page": page, "per_page": 30}
        response = requests.get(
            url_activities,
            params=params,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        response.raise_for_status()
        return [record for record in response.json()]

    def compute_start_timestamp(self, df: pd.DataFrame = None) -> int:
        return (
            datetime.strptime(
                df.sort_values("start_date", ascending=False)["start_date"].values[0],
                DATETIME_FORMAT,
            ).timestamp()
            if not df.empty
            else int(DEFAULT_START)
        )

    def get_activity_laps(self, id: int):
        url_activity = URL_LAPS.format(id=id)
        response = requests.get(
            url_activity, headers={"Authorization": f"Bearer {self.access_token}"}
        )
        response.raise_for_status()
        return response.json()

    @st.cache_data
    def get_raw_activity(self, id: int):
        url_activity = URL_ACTIVITY.format(id=id)
        response = requests.get(
            url_activity, headers={"Authorization": f"Bearer {self.access_token}"}
        )
        response.raise_for_status()
        return response.json()

    def get_laps_from_raw_activity(self, id: int):
        return self.get_raw_activity(id=id)["laps"]

    def get_coordinates_from_raw_activity(self, id: int) -> list[set]:
        return polyline.decode(self.get_raw_activity(id=id)["map"]["polyline"])

    def populate_user_activities(self):
        new_activities = self.get_new_activities_list()
        my_bar = st.progress(0, text="Writing new activities to your database.")
        jsonFile = self.database_file.read()
        data = json.load(jsonFile)

        completed = 0
        new_data = []
        for activity in new_activities:
            new_data.append(self.get_raw_activity(id=activity["id"]))
            my_bar.progress(
                (completed + 1) / len(new_activities),
                text=f"Writing new activities to your database ({completed +1}).",
            )
            completed += 1
        my_bar.empty()
        data["activities"] += new_data
        jsonFile = self.database_file.write()
        json.dump(data, jsonFile)
