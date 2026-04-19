from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for food routes
food = Blueprint("food", __name__)


# Get a specific food item by its ID with optional filtering by category
# Example: http://localhost:4000/food/1
@food.route("/<int:food_id>", methods=["GET"])
def get_food(food_id):
    cursor = None
    try:
        cursor = get_db().cursor(dictionary=True)
        current_app.logger.info(f'GET /food/{food_id}')

        category = request.args.get("category")

        query = "SELECT * FROM FoodGlobal WHERE FoodId = %s"
        params = [food_id]

        if category:
            query += " AND Category = %s"
            params.append(category)

        cursor.execute(query, params)
        food_item = cursor.fetchone()

        if not food_item:
            return jsonify({"error": "Food item not found"}), 404

        current_app.logger.info(f'Retrieved food for food_id {food_id}')
        return jsonify(food_item), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_food: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

