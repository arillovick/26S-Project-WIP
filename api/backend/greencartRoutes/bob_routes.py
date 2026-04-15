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
        current_app.logger.info(f"GET /users/{user_id}/groceryList")
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
        current_app.logger.info(f'GET /groceryList/{user_id}/categorySpend')
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
        current_app.logger.error(f'Database error in get_budget_info: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# route 4: creates a new grocery list for a user [Ashe-2; Bob-1]
@bob.route("/users/<int:userId>/groceryList", methods=["POST"])
def create_grocery_list(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"POST /users/{user_id}/groceryList")
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

# route 6: update items (est total, store, budget, etc) in grocery list [Ashe-2; Bob-6]
@bob.route("/users/<int:userId>/groceryList", methods=["PUT"])
def update_grocery_item(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"PUT /users/{user_id}/groceryList")
        data = request.get_json()
        query = '''UPDATE GroceryList
            SET Est_total = %s, Budget = %s, Store = %s
            WHERE OwnerId = %s'''
        cursor.execute(query, (data['Est_total'], data['Budget'], data['Store'], user_id))
        get_db().commit()
        return jsonify({"message": "Grocery list updated."}), 200
    
    except Error as e:
        current_app.logger.error(f"Database error in update_grocery_item: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# route 7: update an item's storage location and/or expiration date [Bob-2,3]
@bob.route("/pantryItem/<int:pantryItemId>", methods=["PUT"])
def update_pantry_item(pantry_item_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"PUT /pantryItem/{pantry_item_id}")
        data = request.get_json()
        query = '''UPDATE PantryItem
        SET StorageLocation = %s
        WHERE PantryItemId = %s'''
        cursor.execute(query, (data['StorageLocation'], pantry_item_id))
        get_db().commit()
        return jsonify({"message": "Pantry item updated."}), 200
    except Error as e:
        current_app.logger.error(f"Database error in update_pantry_item: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# route 8: remove specific item from a grocery list [Bob-1]
@bob.route("/groceryItem/<int:itemId>", methods=["DELETE"])
def delete_grocery_item(item_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"DELETE /groceryItem/{item_id}")
        query = '''DELETE FROM GroceryItem
            WHERE ItemId = %s'''
        cursor.execute(query, (item_id,))
        get_db().commit()
        return jsonify({"message": "Grocery item deleted from list."}), 200
    except Error as e:
        current_app.logger.error(f"Database error in delete_grocery_item: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# route 9: remove pantry item once used or thrown out [Bob-3]
@bob.route("/pantryItem/<int:pantryItemId>", methods=["DELETE"])
def delete_pantry_item(pantry_item_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"DELETE /pantryItem/{pantry_item_id}")
        query = '''DELETE FROM PantryItem
            WHERE PantryItemId = %s'''
        cursor.execute(query, (pantry_item_id,))
        get_db().commit()
        return jsonify({"message": "Pantry item removed from pantry."}), 200
    except Error as e:
        current_app.logger.error(f"Database error in delete_pantry_item: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()