import requests
from dataclasses import dataclass
import webbrowser
from typing import Tuple
from loguru import logger
from runtrospection.runtrospection import StravaApp


@dataclass
class Authenticator:
    application: StravaApp
    scopes: str = "read,activity:read"
    authorization_code: str

    def open_authorization_window(self):
        url = f"http://www.strava.com/oauth/authorize?client_id={self.application.client_id}&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope={self.scopes}"
        webbrowser.open(url)

    def get_token(self, type: str) -> Tuple[str, str]:
        url = "https://www.strava.com/oauth/token"
        payload = {
            "client_id": self.application.client_id,
            "client_secret": self.application.client_secret,
            "code": self.authorization_code,
            "grant_type": type,
        }
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json()["access_token"], response.json()["refresh_token"]

    def update_access_token(self) -> Tuple[str, str]:
        try:
            return self.get_token(type="authorization_code")
        except:
            logger.info("Access token is no longer valid. Another one is queried.")
            return self.get_token(type="refresh_token")
