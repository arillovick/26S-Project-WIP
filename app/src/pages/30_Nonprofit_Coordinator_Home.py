import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome Nonprofit Coordinator, {st.session_state['first_name']}! 🌱")
st.write('### What would you like to do today?')

if st.button('View Food Waste Trends by Category',
            type='primary',
            use_container_width=True):
    st.switch_page('pages/31_Vector_Waste_Trends.py')

if st.button('View Food Waste by Date',
            type='primary',
            use_container_width=True):
    st.switch_page('pages/32_Vector_Activity.py')

if st.button('Payment Method Insights',
            type='primary',
            use_container_width=True):
    st.switch_page('pages/33_Vector_Payment_Insights.py')
