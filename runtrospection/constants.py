import os
from datetime import datetime

if "CLIENT_SECRET" not in os.environ:
    from dotenv import load_dotenv

    load_dotenv()

CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
CLIENT_ID = "91201"


URL_TOKEN = "https://www.strava.com/oauth/token"
URL_AUTHORIZATION = "http://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope={scopes}"
URL_ACTIVITIES = "https://www.strava.com/api/v3/athlete/activities"
URL_ACTIVITY = "https://www.strava.com/api/v3/activities/{id}"
URL_LAPS = "https://www.strava.com/api/v3/activities/{id}/laps"

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

DEFAULT_START = datetime(2024, 3, 15, 0, 0).timestamp()
DEFAULT_END = datetime.now().timestamp()

DATABASE_FILENAME = f"{os.getcwd()}/input.json"
