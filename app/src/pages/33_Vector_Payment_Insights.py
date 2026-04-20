import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()
API_URL = "http://web-api:4000/users"

st.title("Payment Method Analytics")
st.write("Filter users by payment method")

payment_method = st.selectbox(
    "Select Payment Method",
    ["All", "EBT", "Debit Card", "Credit Card"]
)
try:
    if payment_method == "All":
        ebt_res = requests.get(f"{API_URL}/paymentMethod/EBT")
        debit_res = requests.get(f"{API_URL}/paymentMethod/Debit Card")
        credit_res = requests.get(f"{API_URL}/paymentMethod/Credit Card")
        ebt_data = ebt_res.json() if ebt_res.status_code == 200 else []
        debit_data = debit_res.json() if debit_res.status_code == 200 else []
        credit_data = credit_res.json() if credit_res.status_code == 200 else []
        data = ebt_data + debit_data + credit_data
    else:
        response = requests.get(f"{API_URL}/paymentMethod/{payment_method}")
        data = response.json() if response.status_code == 200 else []

    if data:
        df = pd.DataFrame(data)
        if payment_method == "All":
            col1, col2, col3, col4 = st.columns(4)
            ebt_count = sum(1 for u in data if u["PaymentMethod"] == "EBT")
            debit_count = sum(1 for u in data if u["PaymentMethod"] == "Debit Card")
            credit_count = sum(1 for u in data if u["PaymentMethod"] == "Credit Card")
            with col1:
                st.metric("Total Users", len(data))
            with col2:
                st.metric("EBT Users", ebt_count)
            with col3:
                st.metric("Debit Card Users", debit_count)
            with col4:
                st.metric("Credit Card Users", credit_count)

            chart_df = pd.DataFrame({
                "Payment Method": ["EBT", "Debit Card", "Credit Card"],
                "Number of Users": [ebt_count, debit_count, credit_count]
            }).set_index("Payment Method")
            st.bar_chart(chart_df)
        else:
            st.metric(f"Users with {payment_method}", len(data))

        st.subheader("User List")
        st.dataframe(
            df[["UserId", "FirstName", "LastName", "PaymentMethod"]],
            use_container_width=True
        )
    else:
        st.info("No users found for this payment method.")
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running")

if st.button("Return Home"):
    st.switch_page("pages/30_Nonprofit_Coordinator_Home.py")