import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()
st.title("View My Pantry")
st.write("### View and manage your pantry items here.")

pantry_id = 1
API_URL = f"http://api:4000/pantry/{pantry_id}"

try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        pantry = response.json()
        if pantry:
            st.subheader("Your Pantry Items")
            st.dataframe(pantry)
        else:
            st.info("Your pantry is currently empty. Add items to get started!")
    else:
        st.error(f"Error fetching pantry data: {response.json().get('error', 'Unknown error')}")
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")

st.divider()
st.subheader("Update Storage Location")
pantry_item_id = st.number_input("Pantry Item ID", min_value=1, step=1)
new_location = st.text_input("New Storage Location")

if st.button("Update Location", type='primary'):
    try:
        response = requests.put(
            f'http://api:4000/pantryItem/{pantry_item_id}',
            json={"StorageLocation": new_location}
        )
        if response.status_code == 200:
            st.success("Storage location updated.")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")

    st.divider()
    st.subheader("Delete Pantry Item")
    delete_item_id = st.number_input("Pantry Item ID to Remove", min_value=1, step=1)
    if st.button("Delete Item", type='primary'):
        try:
            response = requests.delete(f'http://api:4000/pantryItem/{delete_item_id}')
            if response.status_code == 200:
                st.success("Pantry item deleted.")
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {str(e)}")