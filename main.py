from runtrospection.authentication import Authenticator
from runtrospection.strava_app import StravaApp
from runtrospection.streamlit_app import StreamlitApp
from runtrospection.runtrospection import Runtrospection
import streamlit as st
import json
import pandas as pd
from io import StringIO

# 10915836332


def main():
    uploaded_file = st.file_uploader(
        "Choose a JSON file", type="json", accept_multiple_files=False
    )
    if uploaded_file is not None:
        st.write("Your database's filename:", uploaded_file.name)
        data = json.loads(uploaded_file.getvalue())

        streamlit_app = StreamlitApp()
        app = StravaApp(database_file=data)
        auth = Authenticator(app=app)
        rts = Runtrospection()

        app.populate_user_activities()
        activity_id = streamlit_app.enter_activity_id()

        if activity_id:
            df_speed = rts.convert_activity_to_df(
                activity=app.get_laps_from_raw_activity(id=activity_id)
            )
            streamlit_app.build_chart(
                df=df_speed, x=None, y=["average_speed", "max_speed"]
            )
            df_map = rts.convert_coordinates_to_df(
                coordinates=app.get_coordinates_from_raw_activity(id=activity_id)
            )
            streamlit_app.build_map(df=df_map)

            json_string = json.dumps(app.database_file)
            st.download_button(
                label="Download your historical data",
                file_name=uploaded_file.name,
                mime="application/json",
                data=json_string,
            )


if __name__ == "__main__":
    main()
