import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()
st.title("Add New Pantry Item")
st.write("### Add a new item to your pantry anytime.")

pantry_id = st.number_input("Pantry ID", min_value=1, step=1)
food_id = st.number_input("Food ID", min_value=1, step=1)
storage_location = st.text_input("Storage Location (e.g. Fridge, Pantry Shelf, Freezer)")
date_bought = st.date_input("Date Bought")
expiration_date = st.date_input("Expiration Date")

if st.button("Add Pantry Item", type='primary'):
    try:
        response = requests.post(
            'http://api:4000/pantryItem',
            json={
                "PantryId": pantry_id,
                "FoodId": food_id,
                "StorageLocation": storage_location,
                "DateBought": str(date_bought),
                "ExpirationDate": str(expiration_date)
            }
        if response.status_code == 201:
            st.success("Pantry item added!")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")