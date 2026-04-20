import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome College Student, {st.session_state['first_name']}! 🎓")
st.write('### What would you like to do today?')

if st.button('View My Pantry',
            type='primary',
            use_container_width=True):
    st.switch_page('pages/01_Ashe_Pantry.py')

if st.button('My Grocery List',
            type='primary',
            use_container_width=True):
    st.switch_page('pages/02_Ashe_Grocery_List.py')

if st.button('My Food Waste',
            type='primary',
            use_container_width=True):
    st.switch_page('pages/03_Ashe_Food_Waste.py')
