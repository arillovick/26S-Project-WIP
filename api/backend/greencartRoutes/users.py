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
@users.route("/<int:userId>/groceryList", methods=["POST"])
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
@users.route("/<int:userId>/groceryList", methods=["PUT"])
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

#route 4: returns account state, inventory, notification preferences, and recent activity [Janice-4, Vector-6]
@users.route("/<int:userId>/activity", methods=["GET"])
def get_user_activity(userId):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /users/{userId}/activity")
        #GET user account info and notification pref
        cursor.execute("""
            SELECT UserId, FirstName, LastName, Email, FamilySize, PaymentMethod, Notifications
            FROM User
            WHERE UserId = %s
        """, (userId,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        #GET their current pantry inventory
        cursor.execute("""
            SELECT pi.PantryItemId, fg.Name AS FoodName, pi.StorageLocation, pi.ExpirationDate, pi.DateBought
            FROM PantryItem pi
            JOIN FoodGlobal fg ON pi.FoodId = fg.FoodId
            JOIN Pantry p ON pi.PantryId = p.PantryId
            WHERE p.UserId = %s
        """, (userId,))
        inventory = cursor.fetchall()

        #GET their recent wasted food activity
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
        cursor.close()
        
# Returns all users who paid with a specific payment method [Vector-5]
@users.route("/users/paymentMethod/<string:paymentMethod>", methods=["GET"])
def get_users_payment_method(payment_method):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f'GET /users/paymentMethod/{payment_method}')
        query = '''SELECT u.UserId, u.FirstName, u.LastName, u.PaymentMethod
            FROM User u
            WHERE u.PaymentMethod = %s'''
        cursor.execute(query, (payment_method,))
        users = cursor.fetchall()
        return jsonify(users), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_users_payment_method: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
