from dataclasses import dataclass
from datetime import datetime
import requests
import polyline
import streamlit as st
import os
from dotenv import load_dotenv

if "CLIENT_SECRET" not in os.environ:
    load_dotenv()

CLIENT_SECRET = os.environ.get("CLIENT_SECRET")


@dataclass
class StravaApp:
    access_token: str = ""
    client_id: str = "91201"
    client_secret: str = CLIENT_SECRET

    def __post_init__(self):
        pass

    def get_activities_list(self) -> list[dict[str, str]]:
        start = int(datetime(2023, 1, 1, 0, 0).timestamp())
        end = int(datetime.now().timestamp())
        url_activities = f"https://www.strava.com/api/v3/athlete/activities"
        params = {"before": end, "after": start, "page": 1, "per_page": 30}
        response = requests.get(
            url_activities,
            params=params,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        response.raise_for_status()
        return [
            {"name": record["name"], "id": record["id"]} for record in response.json()
        ]

    def get_activity_laps(self, id: int):
        url_activity = f"https://www.strava.com/api/v3/activities/{id}/laps"
        response = requests.get(
            url_activity, headers={"Authorization": f"Bearer {self.access_token}"}
        )
        response.raise_for_status()
        return response.json()

    @st.cache_data
    def get_raw_activity(self, id: int):
        url_activity = f"https://www.strava.com/api/v3/activities/{id}"
        response = requests.get(
            url_activity, headers={"Authorization": f"Bearer {self.access_token}"}
        )
        response.raise_for_status()
        return response.json()

    def get_laps_from_raw_activity(self, id: int):
        return self.get_raw_activity(id=id)["laps"]

    def get_coordinates_from_raw_activity(self, id: int) -> list[set]:
        return polyline.decode(self.get_raw_activity(id=id)["map"]["polyline"])
