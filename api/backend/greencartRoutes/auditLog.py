from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

#create a Blueprint for auditLog routes
auditLog = Blueprint("auditLog", __name__)


#GET all timestamped audit log entries
# Example:http://localhost:4000/auditLog
#janice-3
@auditLog.route("/auditLog", methods=["GET"])
def get_all_audit_logs():
    cursor = None
    try:
        cursor = get_db().cursor(dictionary=True)
        current_app.logger.info('GET /auditLog')

        cursor.execute("""
            SELECT id, title, description, Datetime, change_name
            FROM AuditLog
            ORDER BY Datetime DESC
        """)

        logs = cursor.fetchall()
        current_app.logger.info(f'Retrieved {len(logs)} audit log entries')
        return jsonify(logs), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_audit_logs: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()


# GET a specific audit log entry by ID
# Example: http://localhost:4000/auditLog/1
# janice-3
@auditLog.route("/auditLog/<int:log_id>", methods=["GET"])
def get_audit_log(log_id):
    cursor = None
    try:
        cursor = get_db().cursor(dictionary=True)
        current_app.logger.info(f'GET /auditLog/{log_id}')

        cursor.execute("""
            SELECT id, title, description, Datetime, change_name
            FROM AuditLog
            WHERE id = %s
        """, (log_id,))

        log = cursor.fetchone()

        if not log:
            return jsonify({"error": "Audit log entry not found"}), 404

        current_app.logger.info(f'Retrieved audit log entry {log_id}')
        return jsonify(log), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_audit_log: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()