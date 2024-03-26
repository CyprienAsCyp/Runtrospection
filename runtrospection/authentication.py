import requests
from dataclasses import dataclass
import webbrowser
from loguru import logger
import json
from runtrospection.strava_app import StravaApp
from runtrospection.constants import URL_TOKEN, URL_AUTHORIZATION
import streamlit as st


@dataclass
class Authenticator(StravaApp):
    app: StravaApp = None
    scopes: str = "read,activity:read"
    authorization_code: str = ""
    refresh_token: str = ""

    def __post_init__(self):
        self.authorization_code = self.app.database_file["authorization_code"]
        self.refresh_token = self.app.database_file["refresh_token"]
        if self.authorization_code != "":
            text = "You already autorised Runtrosepction to access data!"
            logger.info(text)
            st.info(text)
            self.app.access_token = self.get_access_token()
        else:
            self.open_authorization_window()

    def open_authorization_window(self) -> None:
        url = URL_AUTHORIZATION.format(client_id=self.client_id, scopes=self.scopes)
        webbrowser.open(url)
        text = "You have to authorize Runtrospection to access your data. \
                    Once you'll have paste the authorization code in 'input.json', save the file and rerun the program!"
        logger.info(text)
        st.info(text)

    def update_value_in_json(self, key: str, value: str) -> None:
        self.app.database_file[key] = value

    def get_token(self, type: str) -> str:
        url = URL_TOKEN
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
            text = "It's the first time you are connecting, so you don't have any refresh token at the moment."
            logger.warning(text)
            st.warning(text)
            return self.get_token(type="authorization_code")

    def update_refresh_token(self, refresh_token: str) -> None:
        self.update_value_in_json(key="refresh_token", value=refresh_token)
        self.refresh_token = refresh_token
