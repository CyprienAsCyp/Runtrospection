from runtrospection.authentication import Authenticator
from runtrospection.strava_app import StravaApp
from runtrospection.runtrospection import Runtrospection
import streamlit as st


def main():
    app = StravaApp()
    auth = Authenticator(app=app)
    rts = Runtrospection()
    print(f"access token: {app.access_token}")
    df = rts.convert_activity_to_df(activity=app.get_activity_laps(id="10915836332"))
    st.line_chart(data=df, x="start_date", y=["average_speed", "max_speed"])


if __name__ == "__main__":
    main()
