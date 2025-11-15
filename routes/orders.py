from flask import Blueprint, request, jsonify
from db import get_db
from bson import ObjectId
from datetime import datetime

orders_bp = Blueprint('orders', __name__)

def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable dict."""
    if doc and '_id' in doc:
        doc['id'] = str(doc['_id'])
        del doc['_id']
    if 'timestamp' in doc and isinstance(doc['timestamp'], datetime):
        doc['timestamp'] = doc['timestamp'].isoformat()
    return doc

@orders_bp.route('/', methods=['POST'])
def place_order():
    # রোল চেক ছাড়া (ডেমোর জন্য)
    data = request.json
    db = get_db()
    if not db:
        return jsonify({'msg': 'Database error'}), 500
    try:
        orders = db['orders']
        order_doc = {
            'user_id': data.get('user_id', '1'),  # ডামি user_id
            'items': data['items'],
            'total': float(data['total']),
            'status': 'Pending',
            'rider': None,
            'timestamp': datetime.utcnow()
        }
        orders.insert_one(order_doc)
        return jsonify({'msg': 'Order placed successfully'})
    except Exception as e:
        return jsonify({'msg': 'Failed to place order', 'error': str(e)}), 400

@orders_bp.route('/my', methods=['GET'])
def get_my_orders():
    # রোল চেক ছাড়া (ডেমোর জন্য)
    user_id = request.args.get('user_id', '1')  # ডামি user_id from query
    db = get_db()
    if db is None:
        return jsonify({'msg': 'Database error'}), 500
    
    orders = db['orders']
    order_list = list(orders.find({'user_id': user_id}))
    order_list = [serialize_doc(order) for order in order_list]
    return jsonify(order_list)

@orders_bp.route('/', methods=['GET'])
def get_all_orders():
    # রোল চেক ছাড়া (ডেমোর জন্য)
    db = get_db()
    if db is None:
        return jsonify({'msg': 'Database error'}), 500
    
    orders = db['orders']
    order_list = list(orders.find())
    order_list = [serialize_doc(order) for order in order_list]
    return jsonify(order_list)

@orders_bp.route('/<string:id>/assign', methods=['PUT'])
def assign_rider(id):
    # রোল চেক ছাড়া (ডেমোর জন্য)
    data = request.json
    db = get_db()
    if db is None:
        return jsonify({'msg': 'Database error'}), 500
    try:
        orders = db['orders']
        update_data = {
            'rider': data['rider'],
            'status': f"Assigned to {data['rider']}"
        }
        result = orders.update_one({'_id': ObjectId(id)}, {'$set': update_data})
        if result.modified_count > 0:
            return jsonify({'msg': 'Rider assigned successfully'})
        return jsonify({'msg': 'Order not found'}), 404
    except Exception as e:
        return jsonify({'msg': 'Failed to assign rider', 'error': str(e)}), 400