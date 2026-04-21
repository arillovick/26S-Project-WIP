from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

grocery_items = Blueprint("grocery_items", __name__)

# Remove specific item from a grocery list [Bob-1]
@grocery_items.route("/<int:itemId>", methods=["DELETE"])
def delete_grocery_item(itemId):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"DELETE /groceryItem/{itemId}")
        query = '''DELETE FROM GroceryItem
            WHERE ItemId = %s'''
        cursor.execute(query, (itemId,))
        get_db().commit()
        return jsonify({"message": "Grocery item deleted from list."}), 200
    except Error as e:
        current_app.logger.error(f"Database error in delete_grocery_item: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# Add a new item to a grocery list [Ashe-2]
# Example: POST /groceryItem/
@grocery_items.route("/", methods=["POST"])
def add_grocery_item():
    cursor = None
    try:
        cursor = get_db().cursor(dictionary=True)
        current_app.logger.info("POST /groceryItem/")

        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required"}), 400

        required = ['GroceryListId', 'Name', 'Amount', 'Price']
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400

        # Look up FoodId from FoodGlobal by name
        cursor.execute(
            "SELECT FoodId FROM FoodGlobal WHERE Name = %s LIMIT 1",
            (data['Name'],)
        )
        food = cursor.fetchone()
        if not food:
            return jsonify({"error": f"Food item '{data['Name']}' not found in database"}), 404

        cursor.execute(
            '''INSERT INTO GroceryItem (GroceryListId, ItemId, Name, Price, Amount, WasBought)
               VALUES (%s, %s, %s, %s, %s, %s)''',
            (
                data['GroceryListId'],
                food['FoodId'],
                data['Name'],
                data['Price'],
                data['Amount'],
                data.get('WasBought', False)
            )
        )
        get_db().commit()
        return jsonify({"message": "Item added to grocery list."}), 201

    except Error as e:
        current_app.logger.error(f"Database error in add_grocery_item: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()