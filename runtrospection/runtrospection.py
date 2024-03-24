from dataclasses import dataclass
import pandas as pd
import streamlit as st


@dataclass
class Runtrospection:

    @st.cache_data
    def convert_activity_to_df(self, activity: list[dict]) -> pd.DataFrame:
        df = pd.DataFrame(data=activity)
        df["start_date"] = pd.to_datetime(df["start_date"])
        df = df.set_index(pd.DatetimeIndex(df["start_date"]))
        df = df.drop(["start_date"], axis=1)
        df = df.resample("60s").ffill()
        return df

    @st.cache_data
    def convert_coordinates_to_df(self, coordinates: list[set]) -> pd.DataFrame:
        return pd.DataFrame(data=coordinates, columns=["lat", "lon"])
