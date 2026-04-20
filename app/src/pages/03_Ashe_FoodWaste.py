import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import plotly.express as px
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Food Waste Analytics")
st.write("### A weekly breakdown of how your food is being used.")

BASE_URL = "http://api:4000"
user_id = 1  

# Fetch data 
waste_records = []
user_waste    = []
cost_data     = None

try:
    # Route 3: all waste records with categories — GET /foodWaste/
    r_all = requests.get(f"{BASE_URL}/foodWaste/")
    if r_all.status_code == 200:
        waste_records = r_all.json()
    else:
        st.error(f"Error fetching waste records: {r_all.json().get('error', 'Unknown error')}")

    # Route 1: this user's waste records — GET /foodWaste/<user_id>
    r_user = requests.get(f"{BASE_URL}/foodWaste/{user_id}")
    if r_user.status_code == 200:
        user_waste = r_user.json()
    else:
        st.error(f"Error fetching user waste: {r_user.json().get('error', 'Unknown error')}")

    # Route 2: cost summary — GET /foodWaste/<user_id>/cost
    r_cost = requests.get(f"{BASE_URL}/foodWaste/{user_id}/cost")
    if r_cost.status_code == 200:
        cost_data = r_cost.json()
    elif r_cost.status_code != 404:
        st.warning(f"Could not load cost data: {r_cost.json().get('error', 'Unknown error')}")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.stop()

#  User activity for "used" count
inventory = []
try:
    r_activity = requests.get(f"{BASE_URL}/user/{user_id}/activity")
    if r_activity.status_code == 200:
        inventory = r_activity.json().get("inventory", [])
except requests.exceptions.RequestException:
    pass 

# Totals 
total_wasted = len(user_waste)
total_used   = len(inventory)
total        = total_used + total_wasted

st.divider()

if total == 0:
    st.info("No food data found to display yet.")
    st.stop()

col1, col2 = st.columns(2)

# Chart 1: Used vs Wasted 
with col1:
    st.subheader("Food used vs wasted")

    if total_used == 0 and total_wasted == 0:
        st.info("No data available for this chart.")
    else:
        df_used_wasted = pd.DataFrame({
            "Status": ["Used", "Wasted"],
            "Count":  [total_used, total_wasted],
        })

        fig1 = px.pie(
            df_used_wasted,
            names="Status",
            values="Count",
            color="Status",
            color_discrete_map={"Used": "#1D9E75", "Wasted": "#D85A30"},
            hole=0.35,
        )
        fig1.update_traces(textposition="inside", textinfo="percent+label")
        fig1.update_layout(
            showlegend=True,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(size=14),
        )
        st.plotly_chart(fig1, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Items used", total_used)
        with col_b:
            st.metric("Items wasted", total_wasted)


# Chart 2: Wasted food by category 
with col2:
    st.subheader("Wasted food by category")

    if not waste_records:
        st.info("No waste category data available.")
    else:
        df_waste = pd.DataFrame(waste_records)

        if "Category" not in df_waste.columns or "Amount" not in df_waste.columns:
            st.warning("Waste data is missing Category or Amount fields.")
        else:
            df_category = (
                df_waste.groupby("Category")["Amount"]
                .sum()
                .reset_index()
                .rename(columns={"Amount": "Total Wasted"})
                .sort_values("Total Wasted", ascending=False)
            )

            fig2 = px.pie(
                df_category,
                names="Category",
                values="Total Wasted",
                hole=0.35,
            )
            fig2.update_traces(textposition="inside", textinfo="percent+label")
            fig2.update_layout(
                showlegend=True,
                margin=dict(t=20, b=20, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(size=14),
            )
            st.plotly_chart(fig2, use_container_width=True)

            st.dataframe(df_category, use_container_width=True)

# Cost summary 
st.divider()
st.subheader("Waste cost summary")

if cost_data:
    name       = f"{cost_data.get('FirstName', '')} {cost_data.get('LastName', '')}".strip()
    total_cost = float(cost_data.get("TotalCostWasted", 0.0))
    st.metric(
        label=f"Estimated value of food wasted by {name or f'user {user_id}'}",
        value=f"${total_cost:.2f}",
    )

    if waste_records:
        df_cost = pd.DataFrame(waste_records)
        if "LineCost" in df_cost.columns and "Category" in df_cost.columns:
            df_cost["LineCost"] = pd.to_numeric(df_cost["LineCost"], errors="coerce").fillna(0.0)

            df_cost_by_cat = (
                df_cost.groupby("Category")["LineCost"]
                .sum()
                .reset_index()
                .rename(columns={"LineCost": "Cost Wasted ($)"})
                .sort_values("Cost Wasted ($)", ascending=False)
            )
            df_cost_by_cat["Cost Wasted ($)"] = df_cost_by_cat["Cost Wasted ($)"].map("${:.2f}".format)
            st.dataframe(df_cost_by_cat, use_container_width=True)
else:
    st.info("No cost data available for this user.")