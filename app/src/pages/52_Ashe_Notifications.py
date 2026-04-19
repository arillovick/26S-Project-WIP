import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()
st.title("My Shopping List")
st.write("### View and manage your shopping list here.")

userid = 1
BASE_URL = "http://api:4000"

def api_get(path):
    try:
        r = requests.get(f"{BASE_URL}{path}")
        return r
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")
        return None

st.subheader("Your Grocery Lists")
response = api_get(f"/{userid}/groceryList")

grocery_lists = []
if response and response.status_code == 200:
    grocery_lists = response.json()
    if grocery_lists:
        st.dataframe(grocery_lists, use_container_width=True)
    else:
        st.info("You don't have any grocery lists yet.")
elif response:
    st.error(f"Error fetching grocery lists: {response.json().get('error', 'Unknown error')}")

st.divider()

st.subheader("Create New Grocery List")
list_name = st.text_input("Grocery List Name")

if st.button("Create List", type="primary"):
    if not list_name.strip():
        st.warning("Please enter a name for the list.")
    else:
        try:
            r = requests.post(
                f"{BASE_URL}/users/{userid}/groceryList",
                json={"name": list_name, "userId": userid},
            )
            if r.status_code == 201:
                st.success("Grocery list created.")
                st.rerun()
            else:
                st.error(f"Error: {r.json().get('error', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {str(e)}")

st.divider()

st.subheader("Delete Grocery List")
delete_list_id = st.number_input("Grocery List ID to Remove", min_value=1, step=1)

if st.button("Delete List", type="primary"):
    try:
        r = requests.delete(f"{BASE_URL}/groceryList/{int(delete_list_id)}")
        if r.status_code == 200:
            st.success("Grocery list deleted.")
            st.rerun()
        else:
            st.error(f"Error: {r.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")

st.divider()

st.subheader("Add Item to a List")

col1, col2, col3, col4 = st.columns(4)
with col1:
    target_list_id = st.number_input("List ID", min_value=1, step=1, key="add_list_id")
with col2:
    item_name = st.text_input("Item Name")
with col3:
    item_qty = st.number_input("Quantity", min_value=1, step=1, value=1)
with col4:
    item_price = st.number_input("Price per unit ($)", min_value=0.0, step=0.01, format="%.2f")

if st.button("Add Item", type="primary"):
    if not item_name.strip():
        st.warning("Please enter an item name.")
    else:
        try:
            r = requests.post(
                f"{BASE_URL}/groceryList/{int(target_list_id)}/items",
                json={
                    "name": item_name,
                    "amount": item_qty,
                    "priceAtTime": item_price,
                    "bought": False,
                },
            )
            if r.status_code == 201:
                st.success(f"Added '{item_name}' to list {int(target_list_id)}.")
                st.rerun()
            else:
                st.error(f"Error: {r.json().get('error', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {str(e)}")

st.divider()

st.subheader("Remove Item from a List")

col_a, col_b = st.columns(2)
with col_a:
    remove_list_id = st.number_input("List ID", min_value=1, step=1, key="remove_list_id")
with col_b:
    remove_item_id = st.number_input("Item ID to Remove", min_value=1, step=1)

if st.button("Remove Item", type="primary"):
    try:
        r = requests.delete(
            f"{BASE_URL}/groceryList/{int(remove_list_id)}/items/{int(remove_item_id)}"
        )
        if r.status_code == 200:
            st.success(f"Item {int(remove_item_id)} removed.")
            st.rerun()
        else:
            st.error(f"Error: {r.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")

st.divider()

st.subheader("Budget Tracker")

budget = st.number_input(
    "Set your weekly grocery budget ($)",
    min_value=0.0,
    step=5.0,
    format="%.2f",
    value=st.session_state.get("budget", 0.0),
    key="budget",
)

# Pull items for all lists and total them up
total_spent = 0.0
item_rows = []

if grocery_lists:
    for gl in grocery_lists:
        list_id = gl.get("ListId") or gl.get("list_id") or gl.get("id")
        if not list_id:
            continue
        r = api_get(f"/groceryList/{list_id}/items")
        if r and r.status_code == 200:
            items = r.json()
            for item in items:
                qty = item.get("Amount") or item.get("amount") or 0
                price = item.get("PriceAtTime") or item.get("priceAtTime") or 0.0
                line_total = qty * price
                total_spent += line_total
                item_rows.append({
                    "List ID": list_id,
                    "Item": item.get("Name") or item.get("name", "—"),
                    "Qty": qty,
                    "Unit price": f"${price:.2f}",
                    "Line total": f"${line_total:.2f}",
                })

if item_rows:
    st.dataframe(item_rows, use_container_width=True)

col_left, col_right = st.columns(2)
with col_left:
    st.metric("Estimated total", f"${total_spent:.2f}")
with col_right:
    if budget > 0:
        remaining = budget - total_spent
        if remaining >= 0:
            st.metric("Remaining budget", f"${remaining:.2f}", delta=f"+${remaining:.2f}")
            st.success(f"You are ${remaining:.2f} under budget.")
        else:
            over = abs(remaining)
            st.metric("Over budget by", f"${over:.2f}", delta=f"-${over:.2f}", delta_color="inverse")
            st.error(f"You are ${over:.2f} over your budget. Consider removing some items.")
    else:
        st.info("Enter a budget above to see how your list compares.")