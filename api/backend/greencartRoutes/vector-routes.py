from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

vector = Blueprint("vector", __name__)



# Returns all users who paid with a specific payment method [Vector-5]
@vector.route("/users/paymentMethod/<string:paymentMethod>", methods=["GET"])
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

