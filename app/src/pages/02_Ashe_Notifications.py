import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from datetime import datetime, timedelta
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()
st.title("Expiry Notifications")
st.write("### Items in your pantry expiring within the next 2 days.")

BASE_URL = "http://api:4000"
pantry_id = 1

try:
    response = requests.get(f"{BASE_URL}/pantry/{pantry_id}")

    if response.status_code == 200:
        all_items = response.json()

        today = datetime.today().date()
        in_one_week = today + timedelta(days=2)

        expiring_soon = []
        for item in all_items:
            raw_date = item.get("ExpirationDate")
            if not raw_date:
                continue
            try:
                exp_date = datetime.strptime(raw_date, "%a, %d %b %Y %H:%M:%S %Z").date()
            except ValueError:
                try:
                    exp_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
                except ValueError:
                    continue

            if today <= exp_date <= in_one_week:
                days_left = (exp_date - today).days
                expiring_soon.append({
                    "Item": item.get("Name", "—"),
                    "Storage Location": item.get("StorageLocation", "—"),
                    "Expiration Date": exp_date.strftime("%B %d, %Y"),
                    "Days Left": days_left,
                })

        if expiring_soon:
            expiring_soon.sort(key=lambda x: x["Days Left"])

            urgent   = [i for i in expiring_soon if i["Days Left"] <= 2]
            upcoming = [i for i in expiring_soon if i["Days Left"] > 2]

            if urgent:
                st.error(f"{len(urgent)} item(s) expiring in 2 days or less!")
                for item in urgent:
                    days = item['Days Left']
                    label = "today" if days == 0 else "tomorrow" if days == 1 else f"in {days} days"
                    st.warning(
                        f"**{item['Item']}** — stored in *{item['Storage Location']}* "
                        f"— expires **{label}** ({item['Expiration Date']})"
                    )

            if upcoming:
                st.info(f"{len(upcoming)} item(s) expiring later this week.")
                for item in upcoming:
                    st.write(
                        f"- **{item['Item']}** — stored in *{item['Storage Location']}* "
                        f"— expires in {item['Days Left']} days ({item['Expiration Date']})"
                    )

            st.divider()
            st.subheader("Full expiry list")
            st.dataframe(expiring_soon, use_container_width=True)

        else:
            st.success("Nothing in your pantry is expiring within the next 2 days.")

    elif response.status_code == 404:
        st.warning("No pantry found for this user.")
    else:
        st.error(f"Error fetching pantry: {response.json().get('error', 'Unknown error')}")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")