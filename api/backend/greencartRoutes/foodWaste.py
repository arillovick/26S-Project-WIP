from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for foodWaste routes
foodWaste = Blueprint("foodWaste", __name__)


# Get all food wasted by a specific user with optional filtering by time span
# Example: http://localhost:4000/foodWaste/1
@foodWaste.route("/foodWaste/<int:user_id>", methods=["GET"])
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

# Returns the cost of food wasted per user [Vector-2]
@foodWaste.route("/foodWaste/<int:userId>/cost", methods=["GET"])
def get_foodWaste_cost(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'GET /foodWaste/{user_id}/cost')
        query = '''SELECT u.UserId, u.FirstName, u.LastName,
            SUM(wf.Amount * fg.UnitPrice) AS TotalCostWasted
            FROM WastedFood wf
            JOIN User u ON wf.UserId = u.UserId
            JOIN FoodGlobal fg ON wf.FoodId = fg.FoodId
            WHERE wf.UserId = %s
            GROUP BY u.UserId, u.FirstName, u.LastName'''
        cursor.execute(query, (user_id,))
        cost_data = cursor.fetchall()
        return jsonify(cost_data), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_foodWaste_cost: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# Returns all food waste data from every user [Vector-1, 4]
@foodWaste.route("/foodWaste", methods=["GET"])
def get_wasted_food():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info('GET /wastedFood')
        query = '''SELECT fg.Name, wf.Amount, wf.DateThrownOut, c.Name AS Category
            FROM WastedFood wf
            JOIN FoodGlobal fg ON wf.FoodId = fg.FoodId
            JOIN Category c ON fg.CatId = c.CategoryId'''
        cursor.execute(query)
        wasted_food = cursor.fetchall()
        return jsonify(wasted_food), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_wasted_food: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

