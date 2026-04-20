from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for foodGlobal routes
foodGlobal = Blueprint("foodGlobal", __name__)


# GET all details for a specific food item in FoodGlobal
#ex:http://localhost:4000/foodGlobal/1
#Janice-1
@foodGlobal.route("/<int:food_id>", methods=["GET"])
def get_food_global(food_id):
    cursor = None
    try:
        cursor = get_db().cursor(dictionary=True)
        current_app.logger.info(f'GET /foodGlobal/{food_id}')

        cursor.execute("""
            SELECT fg.FoodId, fg.Name, fg.UnitPrice,
                   fg.DefaultSealedShelfLife, fg.DefaultOpenShelfLife,
                   c.CategoryId, c.Name AS Category, c.WasteTip
            FROM FoodGlobal fg
            JOIN Category c ON fg.CategoryId = c.CategoryId
            WHERE fg.FoodId = %s
        """, (food_id,))

        food_item = cursor.fetchone()

        if not food_item:
            return jsonify({"error": "Food item not found"}), 404

        current_app.logger.info(f'Retrieved food item for food_id {food_id}')
        return jsonify(food_item), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_food_global: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()


# POST: ADD a new food item to FoodGlobal (also logs to AuditLog)
#ex: http://localhost:4000/foodGlobal
#Janice-1
@foodGlobal.route("/", methods=["POST"])
def add_food_global():
    cursor = None
    try:
        db_conn = get_db()
        cursor = get_db().cursor(dictionary=True)
        current_app.logger.info('POST /foodGlobal')

        data = request.get_json()
        name = data.get("Name")
        unit_price = data.get("UnitPrice")
        cat_id = data.get("CategoryId")
        default_sealed = data.get("DefaultSealedShelfLife")
        default_opened = data.get("DefaultOpenShelfLife")

        if not all([name, unit_price, cat_id]):
            return jsonify({"error": "Missing required fields: Name, UnitPrice, CategoryId"}), 400

        cursor.execute("""
            INSERT INTO FoodGlobal (Name, UnitPrice, CategoryId, DefaultSealedShelfLife, DefaultOpenShelfLife)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, unit_price, cat_id, default_sealed, default_opened))

        new_food_id = cursor.lastrowid

        #log to auditLog
        cursor.execute("""
            INSERT INTO AuditLog (UserId, ChangeName, Datetime, Description)
            VALUES (%s, %s, NOW(), %s)
        """, (
            1,
            name,
            f"New food item '{name}' (FoodId: {new_food_id}) added to FoodGlobal."
        ))

        db_conn.commit()
        current_app.logger.info(f'Added new food item with FoodId {new_food_id}')
        return jsonify({"message": "Food item added successfully", "FoodId": new_food_id}), 201
    except Error as e:
        current_app.logger.error(f'Database error in add_food_global: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()



@foodGlobal.route("/", methods=["GET"])
def get_all_food_global():
    cursor = None
    try:
        cursor = get_db().cursor(dictionary=True)
        current_app.logger.info('GET /foodGlobal')

        cursor.execute("""
            SELECT fg.FoodId, fg.Name, fg.UnitPrice,
                   fg.DefaultSealedShelfLife, fg.DefaultOpenShelfLife,
                   c.CategoryId, c.Name AS Category, c.WasteTip
            FROM FoodGlobal fg
            JOIN Category c ON fg.CategoryId = c.CategoryId
        """)

        foods = cursor.fetchall()
        current_app.logger.info(f'Retrieved {len(foods)} food items')
        return jsonify(foods), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_food_global: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

#PUT:Update a food item in FoodGlobal(also add a log to AuditLog)
#ex:http://localhost:4000/foodGlobal/1
#Janice-2
@foodGlobal.route("/<int:food_id>", methods=["PUT"])
def update_food_global(food_id):
    cursor = None
    try:
        db_conn = get_db()
        cursor = db_conn.cursor(dictionary=True)
        current_app.logger.info(f'PUT /foodGlobal/{food_id}')

        data = request.get_json()
        name = data.get("Name")
        unit_price = data.get("UnitPrice")
        cat_id = data.get("CategoryId")
        default_sealed = data.get("DefaultSealedShelfLife")
        default_opened = data.get("DefaultOpenShelfLife")

        cursor.execute("""
            UPDATE FoodGlobal
            SET Name = COALESCE(%s, Name),
                UnitPrice = COALESCE(%s, UnitPrice),
                CategoryId = COALESCE(%s, CategoryId),
                DefaultSealedShelfLife = COALESCE(%s, DefaultSealedShelfLife),
                DefaultOpenShelfLife = COALESCE(%s, DefaultOpenShelfLife)
            WHERE FoodId = %s
        """, (name, unit_price, cat_id, default_sealed, default_opened, food_id))

        if cursor.rowcount == 0:
            return jsonify({"error": "Food item not found"}), 404

        #log in auditLog
        cursor.execute("""
            INSERT INTO AuditLog (UserId, ChangeName, Datetime, Description)
            VALUES (%s, %s, NOW(), %s)
        """, (
            1,  # hardcode an EmpId for now since Janice is the engineer
            name or f"FoodId {food_id}",
            f"FoodGlobal item FoodId {food_id} was updated."
        ))

        db_conn.commit()
        current_app.logger.info(f'Updated food item {food_id}')
        return jsonify({"message": f"Food item {food_id} updated successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in update_food_global: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()


#DELETE a food item from FoodGlobal(also logs to AuditLog)
#example: http://localhost:4000/foodGlobal/1 where 1 is the id of the food item 
#janice-2
@foodGlobal.route("/<int:food_id>", methods=["DELETE"])
def delete_food_global(food_id):
    cursor = None
    try:
        db_conn = get_db()
        cursor = db_conn.cursor(dictionary=True)
        current_app.logger.info(f'DELETE /{food_id}')

        cursor.execute("SELECT Name FROM FoodGlobal WHERE FoodId = %s", (food_id,))
        food_item = cursor.fetchone()

        if not food_item:
            return jsonify({"error": "Food item not found"}), 404

        cursor.execute("DELETE FROM FoodGlobal WHERE FoodId = %s", (food_id,))

        #auditLog
        cursor.execute("""
            INSERT INTO AuditLog (UserId, ChangeName, Datetime, Description)
            VALUES (%s, %s, NOW(), %s)
        """, (
            1,
            food_item["Name"],
            f"FoodGlobal item '{food_item['Name']}' (FoodId: {food_id}) was deleted."
        ))

        db_conn.commit()
        current_app.logger.info(f'Deleted food item {food_id}')
        return jsonify({"message": f"Food item {food_id} deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in delete_food_global: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()