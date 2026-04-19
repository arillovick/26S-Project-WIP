from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

users = Blueprint("users", __name__)

# route 1: return all details/items for a particular grocery list [Ashe-2,4,6; Bob-1,6]
@users.route("/<int:userId>/groceryList", methods=["GET"])
def get_grocery_list(userId):
    cursor = get_db().cursor(dictionary=True)
    try: 
        current_app.logger.info(f"GET /users/{userId}/groceryList")
        query = '''SELECT gl.ListId, gl.Store, gl.Est_total, gl.Actual_total, gl.Budget,
            ROUND(gl.Actual_total - gl.Est_total, 2) AS Difference
            FROM GroceryList gl
            WHERE gl.OwnerId = %s
            ORDER BY gl.ListId ASC'''
        cursor.execute(query, (userId,))
        groceryList = cursor.fetchall()
        return jsonify(groceryList), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_grocery_list: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# route 2: creates a new grocery list for a user [Ashe-2; Bob-1]
@users.route("/users/<int:userId>/groceryList", methods=["POST"])
def create_grocery_list(userId):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"POST /users/{userId}/groceryList")
        data = request.get_json()
        query = '''
            INSERT INTO GroceryList (OwnerId, Est_total, Budget, Store, Actual_total)
            VALUES (%s, %s, %s, %s, %s)'''
        cursor.execute(query, (userId, data['Est_total'], data['Budget'], data['Store'], data['Actual_total']))
        get_db().commit()
        return jsonify({"message": "Grocery list created."}), 201
    except Error as e:
        current_app.logger.error(f"Database error in create_grocery_list: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# route 3: update items (est total, store, budget, etc) in grocery list [Ashe-2; Bob-6]
@users.route("/users/<int:userId>/groceryList", methods=["PUT"])
def update_grocery_item(userId):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"PUT /users/{userId}/groceryList")
        data = request.get_json()
        query = '''UPDATE GroceryList
            SET Est_total = %s, Budget = %s, Store = %s
            WHERE OwnerId = %s'''
        cursor.execute(query, (data['Est_total'], data['Budget'], data['Store'], userId))
        get_db().commit()
        return jsonify({"message": "Grocery list updated."}), 200
    
    except Error as e:
        current_app.logger.error(f"Database error in update_grocery_item: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()