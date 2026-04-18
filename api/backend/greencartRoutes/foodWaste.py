from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for foodWaste routes
foodWaste = Blueprint("foodWaste", __name__)


# Get all food wasted by a specific user with optional filtering by time span
# Example: http://localhost:4000/foodWaste/1
@foodWaste.route("/<int:user_id>", methods=["GET"])
def get_user_food_waste(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /user/user_id/foodWaste')

        # Query parameters are added after the main part of the URL.
        # Example: http://localhost:4000/foodWaste/1?before=2024-01-01&after=2023-01-01
        before = request.args.get("before")
        after = request.args.get("after")

        query = "SELECT * FROM WastedFood WHERE UserId = %s"
        params = [user_id]

        if before:
            query += " AND DateThrownOut < %s"
            params.append(before)
        if after:
            query += " AND DateThrownOut > %s"
            params.append(after)

        cursor.execute(query, params)
        foodWaste_list = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(foodWaste_list)} wasted fooditems for user_id {user_id}')
        return jsonify(foodWaste_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_user_food_waste: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

