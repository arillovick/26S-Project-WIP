import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()
st.title("My Grocery List")
st.write("### View and manage your shopping list here.")

userid = 1
BASE_URL = "http://api:4000"

# ── Helper ────────────────────────────────────────────────────────────────────
def api_get(path):
    try:
        r = requests.get(f"{BASE_URL}{path}")
        return r
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")
        return None

def to_float(val, default=0.0):
    """Safely cast API values to float — handles strings, None, and missing keys."""
    try:
        return float(val) if val is not None else default
    except (TypeError, ValueError):
        return default


# ── VIEW GROCERY LISTS WITH ITEMS ─────────────────────────────────────────────
st.subheader("Your Grocery Lists")
response = api_get(f"/users/{userid}/groceryList")
logger.info("Retrieving grocery list")
grocery_lists = []
if response and response.status_code == 200:
    grocery_lists = response.json()
    if grocery_lists:
        gl = grocery_lists[0]
        items        = gl.get("items", [])
        bought_count = sum(1 for i in items if i.get("Bought"))
        total_items  = len(items)

        budget = to_float(gl.get("Budget"))
        est    = to_float(gl.get("Est_total"))
        actual = to_float(gl.get("Actual_total"))

        label = (
            f"List {gl['ListId']} — {gl.get('Store', '—')}  |  "
            f"Budget: ${budget:.2f}  |  "
            f"Est: ${est:.2f}  |  "
            f"Actual: ${actual:.2f}  |  "
            f"{bought_count}/{total_items} items bought"
        )
        with st.expander(label):
            if items:
                st.dataframe(items, use_container_width=True)
            else:
                st.info("No items in this list yet.")
    else:
        st.info("You don't have any grocery lists yet.")
elif response:
    try:
        st.error(f"Error fetching grocery lists: {response.json().get('error', 'Unknown error')}")
    except Exception:
        st.error(f"Error fetching grocery lists: {response.text or 'Unknown error'}")

st.divider()

# ── CREATE LIST ───────────────────────────────────────────────────────────────
st.subheader("Create New Grocery List")

col1, col2, col3 = st.columns(3)
with col1:
    new_store = st.text_input("Store Name")
with col2:
    new_est_total = st.number_input("Estimated Total ($)", min_value=0.0, step=0.01, format="%.2f")
with col3:
    new_budget = st.number_input("Budget ($)", min_value=0.0, step=0.01, format="%.2f")

if st.button("Create List", type="primary"):
    if not new_store.strip():
        st.warning("Please enter a store name.")
    else:
        try:
            r = requests.post(
                f"{BASE_URL}/users/{userid}/groceryList",
                json={
                    "Store": new_store,
                    "Est_total": new_est_total,
                    "Budget": new_budget,
                    "Actual_total": 0.0
                },
            )
            if r.status_code == 201:
                st.success("Grocery list created.")
                st.rerun()
            else:
                try:
                    st.error(f"Error: {r.json().get('error', 'Unknown error')}")
                except Exception:
                    st.error(f"Error: {r.text or 'Unknown error'}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {str(e)}")

st.divider()

# ── UPDATE LIST ───────────────────────────────────────────────────────────────
st.subheader("Update a Grocery List")

col_a, col_b, col_c, col_d, col_e = st.columns(5)
with col_a:
    update_list_id = st.number_input("List ID", min_value=1, step=1, key="update_list_id")
with col_b:
    update_store = st.text_input("Store Name", key="update_store")
with col_c:
    update_est = st.number_input("Estimated Total ($)", min_value=0.0, step=0.01, format="%.2f", key="update_est")
with col_d:
    update_actual = st.number_input("Actual Total ($)", min_value=0.0, step=0.01, format="%.2f", key="update_actual")
with col_e:
    update_budget = st.number_input("Budget ($)", min_value=0.0, step=0.01, format="%.2f", key="update_budget")

if st.button("Update List", type="primary"):
    if not update_store.strip():
        st.warning("Please enter a store name.")
    else:
        try:
            r = requests.put(
                f"{BASE_URL}/users/{userid}/groceryList/{int(update_list_id)}",
                json={
                    "Store": update_store,
                    "Est_total": update_est,
                    "Actual_total": update_actual,
                    "Budget": update_budget
                },
            )
            if r.status_code == 200:
                st.success("Grocery list updated.")
                st.rerun()
            else:
                try:
                    st.error(f"Error: {r.json().get('error', 'Unknown error')}")
                except Exception:
                    st.error(f"Error: {r.text or 'Unknown error'}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {str(e)}")

st.divider()

# ── ADD ITEM TO LIST ──────────────────────────────────────────────────────────
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
                f"{BASE_URL}/users/{userid}/groceryList/{int(target_list_id)}/items",
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
                try:
                    st.error(f"Error: {r.json().get('error', 'Unknown error')}")
                except Exception:
                    st.error(f"Error: {r.text or 'Unknown error'}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {str(e)}")

st.divider()

# ── REMOVE ITEM FROM LIST ─────────────────────────────────────────────────────
st.subheader("Remove Item from a List")

col_a, col_b = st.columns(2)
with col_a:
    remove_list_id = st.number_input("List ID", min_value=1, step=1, key="remove_list_id")
with col_b:
    remove_item_id = st.number_input("Item ID to Remove", min_value=1, step=1)

if st.button("Remove Item", type="primary"):
    try:
        r = requests.delete(
            f"{BASE_URL}/users/{userid}/groceryList/{int(remove_list_id)}/items/{int(remove_item_id)}"
        )
        if r.status_code == 200:
            st.success(f"Item {int(remove_item_id)} removed.")
            st.rerun()
        else:
            try:
                st.error(f"Error: {r.json().get('error', 'Unknown error')}")
            except Exception:
                st.error(f"Error: {r.text or 'Unknown error'}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")

st.divider()

# ── BUDGET TRACKER ────────────────────────────────────────────────────────────
st.subheader("Budget Tracker")

budget = st.number_input(
    "Set your weekly grocery budget ($)",
    min_value=0.0,
    step=5.0,
    format="%.2f",
    value=st.session_state.get("budget", 0.0),
    key="budget",
)

total_spent = 0.0
item_rows = []

if grocery_lists:
    for gl in grocery_lists:
        list_id     = gl.get("ListId")
        list_budget = to_float(gl.get("Budget"))
        actual      = to_float(gl.get("Actual_total"))
        est         = to_float(gl.get("Est_total"))
        difference  = to_float(gl.get("Difference"))
        items       = gl.get("items", [])

        # Use item-level prices where available for a more accurate total
        if items:
            item_total = sum(
                to_float(i.get("Amount")) * to_float(i.get("PriceAtTime"))
                for i in items
            )
        else:
            item_total = actual if actual else est

        total_spent += item_total

        item_rows.append({
            "List ID":     list_id,
            "Store":       gl.get("Store", "—"),
            "Items":       len(items),
            "Bought":      sum(1 for i in items if i.get("Bought")),
            "Estimated":   f"${est:.2f}",
            "Actual":      f"${actual:.2f}",
            "Items Total": f"${item_total:.2f}",
            "List Budget": f"${list_budget:.2f}",
            "Difference":  f"${difference:.2f}",
        })

if item_rows:
    st.dataframe(item_rows, use_container_width=True)

col_left, col_right = st.columns(2)
with col_left:
    st.metric("Total across all lists", f"${total_spent:.2f}")
with col_right:
    if budget > 0:
        remaining = budget - total_spent
        if remaining >= 0:
            st.metric("Remaining budget", f"${remaining:.2f}", delta=f"+${remaining:.2f}")
            st.success(f"You are ${remaining:.2f} under budget.")
        else:
            over = abs(remaining)
            st.metric("Over budget by", f"${over:.2f}", delta=f"-${over:.2f}", delta_color="inverse")
            st.error(f"You are ${over:.2f} over your budget.")
    else:
        st.info("Enter a budget above to see how your list compares.")