from dataclasses import dataclass
import pandas as pd
import streamlit as st


@dataclass
class Runtrospection:

    @st.cache_data
    def convert_activity_to_df(self, activity: list[dict]) -> pd.DataFrame:
        return pd.DataFrame(data=activity)
