from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

pantry = Blueprint("pantry", __name__)

# route 1: return all details/items for a particular pantry [Ashe-1; Bob-2,3]
@pantry.route("/pantry/<int:pantryId>", methods=["GET"])
def get_pantry_items(pantryId):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'GET /pantry/{pantryId}')
        query = '''SELECT fg.Name, pi.StorageLocation, pi.ExpirationDate
            FROM PantryItem pi
            JOIN Pantry p ON pi.PantryId = p.PantryId
            JOIN FoodGlobal fg ON pi.FoodId = fg.FoodId 
            WHERE pi.PantryId = %s 
            ORDER BY pi.ExpirationDate ASC'''
        cursor.execute(query, (pantryId,))
        pantryList = cursor.fetchall()
        return jsonify(pantryList), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_pantry_items: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()