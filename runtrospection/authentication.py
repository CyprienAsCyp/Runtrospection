import requests
from dataclasses import dataclass
import webbrowser
from loguru import logger
import json
import os
from runtrospection.strava_app import StravaApp


@dataclass
class Authenticator(StravaApp):
    scopes: str = "read,activity:read"
    authorization_code: str = ""
    refresh_token: str = ""

    def __post_init__(self):
        with open(f"{os.getcwd()}/input.json", "r") as jsonFile:
            data = json.load(jsonFile)
        self.authorization_code = data["authorization_code"]
        self.refresh_token = data["refresh_token"]
        if self.authorization_code != "":
            logger.info("Athlete already autorised Runtrosepction to access data!")
            self.access_token = self.get_access_token()
        else:
            self.open_authorization_window()

    def open_authorization_window(self) -> None:
        url = f"http://www.strava.com/oauth/authorize?client_id={self.client_id}&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope={self.scopes}"
        webbrowser.open(url)
        logger.info(
            "You have to authorize Runtrospection to access your data. \
                    Once you'll have paste the authorization code in 'input.json', save the file and rerun the program!"
        )

    def update_value_in_json(self, key: str, value: str) -> None:
        with open(f"{os.getcwd()}/input.json", "r") as jsonFile:
            data = json.load(jsonFile)
        data[key] = value
        with open(f"{os.getcwd()}/input.json", "w") as jsonFile:
            json.dump(data, jsonFile)

    def get_token(self, type: str) -> str:
        url = "https://www.strava.com/oauth/token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": type,
        }
        if type == "authorization_code":
            payload.update({"code": self.authorization_code})
        else:
            payload.update({"refresh_token": self.refresh_token})
        response = requests.post(url, data=payload)
        response.raise_for_status()
        self.update_refresh_token(refresh_token=response.json()["refresh_token"])
        return response.json()["access_token"]

    def get_access_token(self) -> str:
        try:
            return self.get_token(type="refresh_token")
        except requests.HTTPError:
            logger.warning(
                "It's the first time you are connecting, so you don't have any refresh token at the moment."
            )
            return self.get_token(type="authorization_code")

    def update_refresh_token(self, refresh_token: str) -> None:
        self.update_value_in_json(key="refresh_token", value=refresh_token)
        self.refresh_token = refresh_token
