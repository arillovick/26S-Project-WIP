from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

bob = Blueprint("bob", __name__)

# route 1: return all details/items for a particular pantry [Ashe-1; Bob-2,3]
@bob.route("/pantry/<int:pantryId>", methods=["GET"])
def get_pantry_items(pantry_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'GET /pantry/{pantry_id}')
        query = '''SELECT fg.Name, pi.StorageLocation, pi.ExpirationDate
            FROM PantryItem pi
            JOIN Pantry p ON pi.PantryId = p.PantryId
            JOIN FoodGlobal fg ON pi.FoodId = fg.FoodId 
            WHERE pi.PantryId = %s 
            ORDER BY pi.ExpirationDate ASC'''
        cursor.execute(query, (pantry_id,))
        pantry_list = cursor.fetchall()
        return jsonify(pantry_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_pantry_items: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# route 2: return all details/items for a particular grocery list [Ashe-2,4,6; Bob-1,6]
@bob.route("/users/<int:userId>/groceryList", methods=["GET"])
def get_grocery_list(user_id):
    cursor = get_db().cursor(dictionary=True)
    try: 
        current_app.logger.info('GET /users/{user_id}/grocery_list')
        query = '''SELECT gl.ListId, gl.Store, gl.Est_total, gl.Actual_total, gl.Budget,
            ROUND(gl.Actual_total - gl.Est_total, 2) AS Difference
            FROM GroceryList gl
            WHERE gl.OwnerId = %s
            ORDER BY gl.ListId ASC'''
        cursor.execute(query, (user_id,))
        grocery_list = cursor.fetchall()
        return jsonify(grocery_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_grocery_list: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# route 3: returns spending vs. budgeting info by category [Bob-5]
@bob.route("/groceryList/<int:userId>/categorySpend", methods=["GET"])
def get_budget_info(user_id):
    cursor = get_db().cursor(dictionary=True)
    try: 
        current_app.logger.info(f'GET /grocery_list/{user_id}/category_spend')
        query = '''SELECT c.Name AS CategoryName, SUM(gi.Price * gi.Amount) AS ActualSpent,
        AVG(gl.Budget) AS AvgBudget
        FROM GroceryItem gi
        JOIN GroceryList gl ON gi.GroceryListId = gl.ListId
        JOIN FoodGlobal fg ON gi.ItemId = fg.FoodId
        JOIN Category c ON fg.CatId = c.CategoryId
        WHERE gl.OwnerId = %s
        GROUP BY c.Name
        ORDER BY ActualSpent DESC'''
        cursor.execute(query, (user_id,))
        budget_info = cursor.fetchall()
        return jsonify(budget_info), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_grocery_list: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# route 4: creates a new grocery list for a user [Ashe-2; Bob-1]
@bob.route("/users/<int:userId>/groceryList", methods=["POST"])
def create_grocery_list(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"POST /users/{user_id}/grocery_list")
        data = request.get_json()
        query = '''
        INSERT INTO GroceryList (OwnerId, Est_total, Budget, Store, Actual_total)
        VALUES (%s, %s, %s, %s, %s)'''
        cursor.execute(query, (user_id, data['Est_total'], data['Budget'], data['Store'], data['Actual_total']))
        get_db().commit()
        return jsonify({"message": "Grocery list created."}), 201
    except Error as e:
        current_app.logger.error(f"Database error in create_grocery_list: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# route 5: add a new pantry item anytime after a shopping list [Bob-4]
@bob.route("/pantryItem", methods=["POST"])
def add_pantry_item():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"POST /pantry_item")
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