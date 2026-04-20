import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("User Activity Lookup")
st.write("### View a user's account state, inventory, and recent activity.")

BASE_URL = "http://api:4000"

#***
st.subheader("Look Up a User")
user_id = st.number_input("User ID", min_value=1, step=1)
if st.button("Search", type="primary"):
    try:
        r = requests.get(f"{BASE_URL}/users/{int(user_id)}/activity")
        if r.status_code == 200:
            data = r.json()

            st.subheader("Account Info")
            st.dataframe([data.get("user", {})], use_container_width=True)

            st.divider()

            st.subheader("Current Pantry Inventory")
            inventory = data.get("inventory", [])
            if inventory:
                st.dataframe(inventory, use_container_width=True)
            else:
                st.info("No pantry items found for this user.")

            st.divider()

            st.subheader("Recent Food Waste Activity (Last 10)")
            recent_waste = data.get("recent_waste", [])
            if recent_waste:
                st.dataframe(recent_waste, use_container_width=True)
            else:
                st.info("No recent food waste activity found for this user.")

        elif r.status_code == 404:
            st.warning("No user found with that ID.")
        else:
            st.error(f"Error: {r.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")