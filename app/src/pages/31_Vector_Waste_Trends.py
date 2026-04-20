import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()
API_URL = "http://web-api:4000/foodWaste"

st.title("Food Waste by Category")
st.write("View Total Food Waste by Category")
category = st.selectbox("Filter by Category", ["All", "Produce", "Meat", "Dairy", "Frozen", 
                                               "Seafood", "Beverages", "Condiments", "Grains"])
params = {}
if category != "All":
    params["category"] = category
try:
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            st.subheader(f"Showing {len(data)} wasted food items")
            df = pd.DataFrame(data)
            df = df.rename(columns={"Name": "Food Item", "Amount": "Amount Wasted"})
            df = df.set_index("Food Item")
            st.bar_chart(df["Amount Wasted"])
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