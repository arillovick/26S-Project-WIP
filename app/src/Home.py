##################################################
# This is the main/entry-point file for the
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports regular and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout='wide')

# If a user is at this page, we assume they are not
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false.
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel.
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

logger.info("Loading the Home page of the app")
st.title('🛒 GreenCart')
st.write('### Reduce food waste, save money, and shop smarter.')
st.write('#### Hi! As which user would you like to log in?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user
# can click to MIMIC logging in as that mock user.

if st.button("Act as Ashe, a College Student",
        type='primary',
        use_container_width=True):
    # when user clicks the button, they are now considered authenticated
    st.session_state['authenticated'] = True
    # we set the role of the current user
    st.session_state['role'] = 'college_student'
    # we add the first name of the user (so it can be displayed on
    # subsequent pages).
    st.session_state['first_name'] = 'Ashe'
    # finally, we ask streamlit to switch to another page, in this case, the
    # landing page for this particular user type
    logger.info("Logging in as College Student Persona")
    st.switch_page('pages/00_College_Student_Home.py')

if st.button('Act as Bob, a Family Household Manager',
        type='primary',
        use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'family_household_manager'
    st.session_state['first_name'] = 'Bob'
    st.switch_page('pages/10_Family_Household_Manager_Home.py')

if st.button('Act as Janice, a Platform Engineer',
        type='primary',
        use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'platform_engineer'
    st.session_state['first_name'] = 'Janice'
    st.switch_page('pages/20_Platform_Engineer_Home.py')

if st.button('Act as Vector, a Nonprofit Coordinator',
        type='primary',
        use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'nonprofit_coordinator'
    st.session_state['first_name'] = 'Vector'
    st.switch_page('pages/30_Nonprofit_Coordinator_Home.py')
