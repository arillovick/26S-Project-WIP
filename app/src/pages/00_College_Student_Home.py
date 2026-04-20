import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome College Student, {st.session_state['first_name']}! 🎓")
st.write('### What would you like to do today?')

if st.button('Go to Shopping List',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/01_Ashe_GroceryList.py')

if st.button('View Notifications', type='primary', use_container_width=True):
    st.switch_page('pages/02_Ashe_Notifications.py')

if st.button('Food Waste Overview', type='primary', use_container_width=True):
    st.switch_page('pages/03_Ashe_FoodWaste.py')
