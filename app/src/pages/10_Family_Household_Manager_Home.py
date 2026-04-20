import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Family Household Manager, {st.session_state['first_name']}! 🏠.")
st.write('### What would you like to do today?')

if st.button('Manage Pantry Items',
            type='primary',
            use_container_width=True):
    st.switch_page('pages/51_Bob_Pantry.py')

if st.button('Add Pantry Items',
            type='primary',
            use_container_width=True):
    st.switch_page('pages/52_Bob_Add_Pantry.py')

if st.button('Spending Overview',
            type='primary',
            use_container_width=True):
    st.switch_page('pages/53_Bob_Spending.py')
