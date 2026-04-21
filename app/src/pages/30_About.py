import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.write("# About GreenCart 🛒")

st.markdown(
    """
    Food waste is a growing crisis. In the United States alone, roughly 30-40% of the food supply is 
    wasted every year, amounting to over 133 billion pounds, and 43% of that waste comes from households. 
    Beyond the financial toll, food waste is one of the leading drivers of landfill methane emissions, 
    which are 29 times more harmful than carbon dioxide.

    **GreenCart** combines pantry tracking, grocery list planning, expiration monitoring, and food waste 
    analytics to help users make smarter grocery decisions while reducing the environmental and financial 
    impact of food waste.

    ### What GreenCart Does
    - Track the remaining shelf life of items in your kitchen
    - Receive reminders before food spoils
    - Plan grocery lists with estimated budgets
    - Monitor food waste by category
    - Get sustainability recommendations for items that are no longer safely edible

    ### Tech Stack
    - **Frontend:** Streamlit
    - **Backend:** Flask REST API
    - **Database:** MySQL
    - **Infrastructure:** Docker

    ### Team
    Abigail Rillovick, Danielle Chen, Dreshta Boghra, Nina Mayer, Alyssa Haidar

    *Shop smarter, waste less.*
    """
)

if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")