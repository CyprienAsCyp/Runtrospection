from dataclasses import dataclass
import streamlit as st
import pandas as pd
from typing import Union


@dataclass
class StreamlitApp:

    def enter_activity_id(self):
        activity_id = st.text_input("Activity ID")
        return activity_id

    def build_chart(self, df: pd.DataFrame, x: str, y: Union[str, list[str]]):
        st.line_chart(data=df, x=x, y=y)

    def build_map(self, df: pd.DataFrame):
        st.map(data=df, size=5)
