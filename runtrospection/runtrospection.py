from dataclasses import dataclass
from datetime import datetime
import requests


@dataclass
class StravaApp:
    client_id: str = "91201"
    cient_secret: str = "e7cd3eb0483992f73d49dbb6941c4274e3309466"


@dataclass
class Runtrospection(StravaApp):
    access_token: str

    def __post_init__(self):
        pass

    def get_activities_list(self) -> list[dict[str, str]]:
        start = int(datetime(2023, 1, 1, 0, 0).timestamp())
        end = int(datetime.now().timestamp())
        url_activities = f"https://www.strava.com/api/v3/athlete/activities?before={end}&after={start}"
        response = requests.get(
            url_activities, headers={"Authorization": f"Bearer {self.access_token}"}
        )
        response.raise_for_status()
        return [
            {"name": record["name"], "id": record["id"]} for record in response.json()
        ]

    def get_activity(self, id):
        url_activity = f"https://www.strava.com/api/v3/activities/{id}/laps"
        response = requests.get(
            url_activity, headers={"Authorization": f"Bearer {self.access_token}"}
        )
        response.raise_for_status()
        return response.json()
