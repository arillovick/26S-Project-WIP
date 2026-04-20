import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Household Manager, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('My Pantry',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/40_Bob_Pantry.py')

if st.button('Add Pantry Item', type='primary', use_container_width=True):
    st.switch_page('pages/41_Bob_Add_Pantry.py')

if st.button('Spending by Category', type='primary', use_container_width=True):
    st.switch_page('pages/42_Bob_Spending.py')