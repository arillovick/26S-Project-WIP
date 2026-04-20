import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Food waste dashboard track food waste across chosen categories
SideBarLinks()
API_URL = "http://localhost:4000/foodWaste"
st.title("Food Waste Overview")
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
            st.subheader(f"Showing {len(data)} wasted food")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Food Item**")
                for item in data:
                    st.write(item["Name"])
            with col2:
                st.write("**Amount Wasted**")
                for item in data:
                    st.write(item["Amount"])
        else:
            st.info("No food waste records found")
    else:
        st.error(f"Error fetching data: {response.json().get('error', 'Unknown error')}")
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running")

if st.button("Return Home"):
    st.switch_page("pages/30_Nonprofit_Coordinator_Home.py")


