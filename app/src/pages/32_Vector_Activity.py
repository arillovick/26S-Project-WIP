import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

API_URL = "http://web-api:4000/foodWaste"

st.title("Food Waste by Date")
st.write("View food waste trends over time.")
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            df["DateThrownOut"] = pd.to_datetime(df["DateThrownOut"])
            df = df.groupby("DateThrownOut")["Amount"].sum().reset_index()
            df = df.sort_values("DateThrownOut")
            st.subheader("Total Waste Over Time")
            st.line_chart(df.set_index("DateThrownOut")["Amount"],
                         use_container_width=True,
                         y_label="Amount Wasted",
                         x_label="Date")
            st.subheader("Raw Data")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No food waste records found")
    else:
        st.error(f"Error fetching data: {response.json().get('error', 'Unknown error')}")
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running")
if st.button("Return Home"):
    st.switch_page("pages/30_Nonprofit_Coordinator_Home.py")