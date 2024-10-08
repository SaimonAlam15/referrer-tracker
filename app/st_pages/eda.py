import streamlit as st

from data import get_data
from queries import DATA_ANALYSIS_QUERY


def eda():
    data = get_data(DATA_ANALYSIS_QUERY)
    st.dataframe(data)