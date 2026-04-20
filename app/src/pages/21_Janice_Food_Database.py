import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Food Global Database")
st.write("### Manage food items in the global database.")

#GET
st.subheader("Look Up a Food Item")
food_id = st.number_input("Food ID", min_value=1, step=1)
if st.button("Get Food Item", type='primary'):
    try:
        response = requests.get(f'http://api:4000/foodGlobal/{food_id}')
        if response.status_code == 200:
            st.dataframe([response.json()])
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")

st.divider()

#add a new food
st.subheader("Add a New Food Item")
new_name = st.text_input("Food Name")
new_price = st.number_input("Unit Price", min_value=0.0, step=0.01)
new_cat_id = st.number_input("Category ID", min_value=1, step=1)
new_sealed = st.number_input("Default Sealed Shelf Life (days)", min_value=0, step=1)
new_opened = st.number_input("Default Open Shelf Life (days)", min_value=0, step=1)

if st.button("Add Food Item", type='primary'):
    try:
        response = requests.post(
            'http://api:4000/foodGlobal',
            json={
                "Name": new_name,
                "UnitPrice": new_price,
                "CategoryId": new_cat_id,
                "DefaultSealedShelfLife": new_sealed,
                "DefaultOpenShelfLife": new_opened
            }
        )
        if response.status_code == 201:
            st.success(f"Food item added! FoodId: {response.json().get('FoodId')}")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")

st.divider()

#UPDATEe
st.subheader("Update a Food Item")
update_id = st.number_input("Food ID to Update", min_value=1, step=1)
update_name = st.text_input("New Name (leave blank to keep current)")
update_price = st.number_input("New Unit Price (0 to keep current)", min_value=0.0, step=0.01)
update_cat_id = st.number_input("New Category ID (0 to keep current)", min_value=0, step=1)

if st.button("Update Food Item", type='primary'):
    try:
        payload = {}
        if update_name:
            payload["Name"] = update_name
        if update_price > 0:
            payload["UnitPrice"] = update_price
        if update_cat_id > 0:
            payload["CategoryId"] = update_cat_id
        response = requests.put(
            f'http://api:4000/foodGlobal/{update_id}',
            json=payload
        )
        if response.status_code == 200:
            st.success("Food item updated successfully.")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")

st.divider()

#DELETE
st.subheader("Delete a Food Item")
delete_id = st.number_input("Food ID to Delete", min_value=1, step=1)

if st.button("Delete Food Item", type='primary'):
    try:
        response = requests.delete(f'http://api:4000/foodGlobal/{delete_id}')
        if response.status_code == 200:
            st.success("Food item deleted successfully.")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")