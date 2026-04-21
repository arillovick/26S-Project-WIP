import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome Platform Engineer, {st.session_state['first_name']}! 🛠️")
st.write('### What would you like to do today?')

if st.button('Manage FoodGlobal Databases',
            type='primary',
            use_container_width=True):
    st.switch_page('pages/21_Janice_Food_Database.py')

if st.button('View Audit Log',
            type='primary',
            use_container_width=True):
    st.switch_page('pages/22_Janice_Audit_Log.py')

if st.button('User Activity',
            type='primary',
            use_container_width=True):
    st.switch_page('pages/23_Janice_User_Activity.py')