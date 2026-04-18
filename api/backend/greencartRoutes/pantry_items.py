from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

pantry_items = Blueprint("pantry_items", __name__)

# route 1: add a new pantry item anytime after a shopping list [Bob-4]
@pantry_items.route("/pantryItem", methods=["POST"])
def add_pantry_item():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"POST /pantryItem")
        data = request.get_json()
        query = '''INSERT INTO PantryItem (PantryId, StorageLocation, FoodId, DateBought, ExpirationDate)
            VALUES (%s, %s, %s, %s, %s)'''
        cursor.execute(query, (data['PantryId'], data['StorageLocation'], data['FoodId'], data['DateBought'], data['ExpirationDate']))
        get_db().commit()
        return jsonify({"message": "Pantry item added."}), 201
    except Error as e:
        current_app.logger.error(f"Database error in add_pantry_item: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# route 2: update an item's storage location and/or expiration date [Bob-2,3]
@pantry_items.route("/pantryItem/<int:pantryItemId>", methods=["PUT"])
def update_pantry_item(pantryItemId):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"PUT /pantryItem/{pantryItemId}")
        data = request.get_json()
        query = '''UPDATE PantryItem
        SET StorageLocation = %s
        WHERE PantryItemId = %s'''
        cursor.execute(query, (data['StorageLocation'], pantryItemId))
        get_db().commit()
        return jsonify({"message": "Pantry item updated."}), 200
    except Error as e:
        current_app.logger.error(f"Database error in update_pantry_item: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# route 3: remove pantry item once used or thrown out [Bob-3]
@pantry_items.route("/pantryItem/<int:pantryItemId>", methods=["DELETE"])
def delete_pantry_item(pantryItemId):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"DELETE /pantryItem/{pantryItemId}")
        query = '''DELETE FROM PantryItem
            WHERE PantryItemId = %s'''
        cursor.execute(query, (pantryItemId,))
        get_db().commit()
        return jsonify({"message": "Pantry item removed from pantry."}), 200
    except Error as e:
        current_app.logger.error(f"Database error in delete_pantry_item: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()