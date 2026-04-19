import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()
st.title("My Shopping List")
st.write("### View and manage your shopping list here.")

userid = 1
API_URL = f"http://api:4000/{userid}/groceryList"

try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        groceryList = response.json()
        if groceryList:
            st.subheader("Your Grocery List")
            st.dataframe(groceryList)
        else:
            st.info("You don't have any grocery lists yet. Click the button below to create one.")
    else:
        st.error(f"Error fetching grocery list data: {response.json().get('error', 'Unknown error')}")
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")

st.divider()
st.subheader("Create New Grocery List")
list_name = st.text_input("Grocery List Name")

if st.button("Create List", type='primary'):
    try:
        response = requests.post(
            f'http://web-api:4000/users/{userid}/groceryList',
            json={"name": list_name, "userId": userid}
        )
        if response.status_code == 201:
            st.success("Grocery list created.")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")

    st.divider()
    st.subheader("Delete Grocery List")
    delete_list_id = st.number_input("Grocery List ID to Remove", min_value=1, step=1)
    if st.button("Delete List", type='primary'):
        try:
            response = requests.delete(f'http://web-api:4000/groceryList/{delete_list_id}')
            if response.status_code == 200:
                st.success("Grocery list deleted.")
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {str(e)}")

    st.write("Could not connect to database to get grocery lists.")