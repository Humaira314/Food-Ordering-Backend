from flask import Blueprint, request, jsonify
from db import get_db
from bson import ObjectId
from datetime import datetime

riders_bp = Blueprint('riders', __name__)

def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable dict."""
    if doc and '_id' in doc:
        doc['id'] = str(doc['_id'])
        del doc['_id']
    if 'timestamp' in doc and isinstance(doc['timestamp'], datetime):
        doc['timestamp'] = doc['timestamp'].isoformat()
    return doc

# Example mock authentication function
def get_current_user():
    """Simulate authentication using headers (replace with real logic)."""
    token = request.headers.get('Authorization')
    if not token:
        return None
    # Simulate decoding token or checking session
    # You can replace this logic with your own authentication method
    if token == "rider_token":
        return {'username': 'rider1', 'role': 'rider'}
    elif token == "admin_token":
        return {'username': 'admin1', 'role': 'admin'}
    else:
        return None


@riders_bp.route('/assigned', methods=['GET'])
def get_assigned_orders():
    user = get_current_user()
    if not user:
        return jsonify({'msg': 'Unauthorized'}), 401
    if user['role'] != 'rider':
        return jsonify({'msg': 'Access denied'}), 403

    db = get_db()
    if db is None:
        return jsonify({'msg': 'Database error'}), 500

    orders = db['orders']
    order_list = list(orders.find({'rider': user['username']}))
    order_list = [serialize_doc(order) for order in order_list]

    return jsonify(order_list)


@riders_bp.route('/<string:id>/status', methods=['PUT'])
def update_status(id):
    user = get_current_user()
    if not user:
        return jsonify({'msg': 'Unauthorized'}), 401
    if user['role'] != 'rider':
        return jsonify({'msg': 'Access denied'}), 403

    data = request.json
    if not data or 'status' not in data:
        return jsonify({'msg': 'Missing status field'}), 400

    db = get_db()
    if db is None:
        return jsonify({'msg': 'Database error'}), 500

    try:
        orders = db['orders']
        result = orders.update_one({'_id': ObjectId(id)}, {'$set': {'status': data['status']}})
        if result.modified_count > 0:
            return jsonify({'msg': 'Status updated successfully'})
        return jsonify({'msg': 'Order not found'}), 404
    except Exception as e:
        return jsonify({'msg': 'Failed to update status', 'error': str(e)}), 400
