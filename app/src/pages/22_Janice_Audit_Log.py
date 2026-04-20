import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Audit Log")
st.write("### View all changes made to the FoodGlobal database.")

BASE_URL = "http://api:4000"

#******************************
st.subheader("All Audit Log Entries")

try:
    response = requests.get(f"{BASE_URL}/auditLog/")
    if response.status_code == 200:
        logs = response.json()
        if logs:
            st.dataframe(logs, use_container_width=True)
        else:
            st.info("No audit log entries found.")
    else:
        st.error(f"Error fetching audit log: {response.json().get('error', 'Unknown error')}")
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")

st.divider()

#***************************
st.subheader("Look Up a Specific Audit Log Entry")

log_id = st.number_input("Audit Log ID", min_value=1, step=1)

if st.button("Search", type="primary"):
    try:
        r = requests.get(f"{BASE_URL}/auditLog/{int(log_id)}")
        if r.status_code == 200:
            log = r.json()
            st.success("Entry found.")
            st.json(log)
        elif r.status_code == 404:
            st.warning("No audit log entry found with that ID.")
        else:
            st.error(f"Error: {r.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")