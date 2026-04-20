import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()
st.title("See Spending by Category")
st.write("### View your actual spending vs. budget by food category.")

user_id = 1
API_URL = f"http://api:4000/groceryList/{user_id}/CategorySpend"

try:
    response = requests.get(API_URL)
    if response.status_code == 200:
            spending = response.json()
            if spending:
                st.subheader("Category Breakdown")
                st.dataframe(spending)
            else:
                st.error("No spending data found.")
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    else:
         st.error(f"Error fetching spending data: {response.json().get('error', 'Unknown error')}")
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")