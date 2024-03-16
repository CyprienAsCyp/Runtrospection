from runtrospection.authentication import Authenticator
from runtrospection.strava_app import StravaApp
from runtrospection.streamlit_app import StreamlitApp
from runtrospection.runtrospection import Runtrospection

# 10915836332


def main():
    streamlit_app = StreamlitApp()
    app = StravaApp()
    auth = Authenticator(app=app)
    rts = Runtrospection()
    print(f"access token: {app.access_token}")
    activity_id = streamlit_app.enter_activity_id()
    if activity_id:
        df_speed = rts.convert_activity_to_df(
            activity=app.get_laps_from_raw_activity(id=activity_id)
        )
        streamlit_app.build_chart(df=df_speed, x=None, y=["average_speed", "max_speed"])
        df_map = rts.convert_coordinates_to_df(
            coordinates=app.get_coordinates_from_raw_activity(id=activity_id)
        )
        streamlit_app.build_map(df=df_map)


if __name__ == "__main__":
    main()
