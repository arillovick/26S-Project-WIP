from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

grocery_list = Blueprint("grocery_list", __name__)

# route 1: returns spending vs. budgeting info by category [Bob-5]
@grocery_list.route("/<int:userId>/categorySpend", methods=["GET"])
def get_budget_info(userId):
    cursor = get_db().cursor(dictionary=True)
    try: 
        current_app.logger.info(f'GET /groceryList/{userId}/categorySpend')
        query = '''SELECT c.Name AS CategoryName, SUM(gi.Price * gi.Amount) AS ActualSpent,
            ROUND(AVG(gl.Budget), 2) AS AvgBudget
            FROM GroceryItem gi
            JOIN GroceryList gl ON gi.GroceryListId = gl.ListId
            JOIN FoodGlobal fg ON gi.ItemId = fg.FoodId
            JOIN Category c ON fg.CategoryId = c.CategoryId
            WHERE gl.OwnerId = %s
            GROUP BY c.Name
            ORDER BY ActualSpent DESC'''
        cursor.execute(query, (userId,))
        budgetInfo = cursor.fetchall()
        return jsonify(budgetInfo), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_budget_info: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()