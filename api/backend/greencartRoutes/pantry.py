from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

pantry = Blueprint("pantry", __name__)

# route 1: return all details/items for a particular pantry [Ashe-1; Bob-2,3]
@pantry.route("/<int:pantryId>", methods=["GET"])
def get_pantry_items(pantryId):
    cursor = None
    try:
        cursor = get_db().cursor(dictionary=True)
        current_app.logger.info(f'GET /pantry/{pantryId}')

        days = request.args.get("days", type=int)

        query = '''SELECT fg.Name, pi.StorageLocation, pi.ExpirationDate
                   FROM PantryItem pi
                   JOIN FoodGlobal fg ON pi.FoodId = fg.FoodId
                   WHERE pi.PantryId = %s'''
        params = [pantryId]

        if days is not None:
            query += " AND pi.ExpirationDate <= CURDATE() + INTERVAL %s DAY"
            params.append(days)

        query += " ORDER BY pi.ExpirationDate ASC"

        cursor.execute(query, params)
        pantryList = cursor.fetchall()

        if not pantryList:
            return jsonify({"error": f"No items found for pantry {pantryId}"}), 404

        return jsonify(pantryList), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_pantry_items: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()