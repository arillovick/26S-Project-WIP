from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

grocery_items = Blueprint("grocery_items", __name__)

# route 8: remove specific item from a grocery list [Bob-1]
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