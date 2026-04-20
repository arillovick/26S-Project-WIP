import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Food waste dashboard track food waste across chosen categories
SideBarLinks()
st.title("Food Waste Overview By Category")
category_id = st.number_input("Category ID", min_value=1, step=1)






