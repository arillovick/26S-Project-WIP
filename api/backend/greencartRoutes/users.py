from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

users = Blueprint("users", __name__)


# Route 1: return all grocery lists with their items for a user [Ashe-2,4,6; Bob-1,6]
@users.route("/<int:userId>/groceryList", methods=["GET"])
def get_grocery_list(userId):
    cursor = None
    try:
        cursor = get_db().cursor(dictionary=True)
        current_app.logger.info(f"GET /users/{userId}/groceryList")

        list_query = '''SELECT gl.ListId, gl.Store, gl.Est_total, gl.Actual_total, gl.Budget,
            ROUND(gl.Actual_total - gl.Est_total, 2) AS Difference
            FROM GroceryList gl
            WHERE gl.OwnerId = %s
            ORDER BY gl.ListId ASC'''
        cursor.execute(list_query, (userId,))
        grocery_lists = list(cursor.fetchall())

        if not grocery_lists:
            return jsonify([]), 200

        # Schema column names: GroceryListId, ItemId, Price, WasBought
        item_query = '''SELECT gi.GroceryItemId, fg.Name, gi.Amount,
            gi.Price AS PriceAtTime, gi.WasBought AS Bought
            FROM GroceryItem gi
            JOIN FoodGlobal fg ON gi.ItemId = fg.FoodId
            WHERE gi.GroceryListId = %s'''

        for grocery_list in grocery_lists:
            cursor.execute(item_query, (grocery_list['ListId'],))
            grocery_list['items'] = cursor.fetchall()

        return jsonify(grocery_lists), 200

    except Error as e:
        current_app.logger.error(f'Database error in get_grocery_list: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()


# Route 2: create a new grocery list for a user [Ashe-2; Bob-1]
@users.route("/<int:userId>/groceryList", methods=["POST"])
def create_grocery_list(userId):
    cursor = None
    try:
        cursor = get_db().cursor(dictionary=True)
        current_app.logger.info(f"POST /users/{userId}/groceryList")
        data = request.get_json()

        required = ['Est_total', 'Budget', 'Store', 'Actual_total']
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400

        query = '''INSERT INTO GroceryList (OwnerId, Est_total, Budget, Store, Actual_total)
            VALUES (%s, %s, %s, %s, %s)'''
        cursor.execute(query, (
            userId,
            data['Est_total'],
            data['Budget'],
            data['Store'],
            data['Actual_total']
        ))
        get_db().commit()
        return jsonify({"message": "Grocery list created."}), 201

    except Error as e:
        current_app.logger.error(f"Database error in create_grocery_list: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()


# Route 3: update a specific grocery list [Ashe-2; Bob-6]
@users.route("/<int:userId>/groceryList/<int:listId>", methods=["PUT"])
def update_grocery_list(userId, listId):
    cursor = None
    try:
        cursor = get_db().cursor(dictionary=True)
        current_app.logger.info(f"PUT /users/{userId}/groceryList/{listId}")
        data = request.get_json()

        required = ['Est_total', 'Budget', 'Store', 'Actual_total']
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400

        query = '''UPDATE GroceryList
            SET Est_total = %s, Budget = %s, Store = %s, Actual_total = %s
            WHERE OwnerId = %s AND ListId = %s'''
        cursor.execute(query, (
            data['Est_total'],
            data['Budget'],
            data['Store'],
            data['Actual_total'],
            userId,
            listId
        ))
        get_db().commit()

        if cursor.rowcount == 0:
            return jsonify({"error": f"List {listId} not found for user {userId}"}), 404

        return jsonify({"message": "Grocery list updated."}), 200

    except Error as e:
        current_app.logger.error(f"Database error in update_grocery_list: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()


# Route 4: return account info, inventory, and recent waste activity [Janice-4, Vector-6]
@users.route("/<int:userId>/activity", methods=["GET"])
def get_user_activity(userId):
    cursor = None
    try:
        cursor = get_db().cursor(dictionary=True)
        current_app.logger.info(f"GET /users/{userId}/activity")

        cursor.execute("""
            SELECT UserId, FirstName, LastName, Email, FamilySize, PaymentMethod, Notifications
            FROM User
            WHERE UserId = %s
        """, (userId,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Schema: Pantry uses OwnerId not UserId; PantryItem has no StorageLocation
        cursor.execute("""
            SELECT pi.PantryItemId, fg.Name AS FoodName,
                   pi.ExpirationDate, pi.DateBought
            FROM PantryItem pi
            JOIN FoodGlobal fg ON pi.FoodId = fg.FoodId
            JOIN Pantry p ON pi.PantryId = p.PantryId
            WHERE p.OwnerId = %s
        """, (userId,))
        inventory = cursor.fetchall()

        cursor.execute("""
            SELECT wf.WastedFoodId, fg.Name AS FoodName, wf.DateThrownOut, wf.Amount
            FROM WastedFood wf
            JOIN FoodGlobal fg ON wf.FoodId = fg.FoodId
            WHERE wf.UserId = %s
            ORDER BY wf.DateThrownOut DESC
            LIMIT 10
        """, (userId,))
        recent_waste = cursor.fetchall()

        return jsonify({
            "user": user,
            "inventory": inventory,
            "recent_waste": recent_waste
        }), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_user_activity: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()


# Route 5: return all users who paid with a specific payment method [Vector-5]
@users.route("/paymentMethod/<string:paymentMethod>", methods=["GET"])
def get_users_payment_method(paymentMethod):
    cursor = None
    try:
        cursor = get_db().cursor(dictionary=True)
        current_app.logger.info(f'GET /users/paymentMethod/{paymentMethod}')

        query = '''SELECT u.UserId, u.FirstName, u.LastName, u.PaymentMethod
            FROM User u
            WHERE u.PaymentMethod = %s'''
        cursor.execute(query, (paymentMethod,))
        result = cursor.fetchall()
        return jsonify(result), 200

    except Error as e:
        current_app.logger.error(f'Database error in get_users_payment_method: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()