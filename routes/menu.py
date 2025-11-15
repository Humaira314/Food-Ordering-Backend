from flask import Blueprint, request, jsonify
from db import get_db
from bson import ObjectId

menu_bp = Blueprint('menu', __name__)

def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable dict."""
    if doc and '_id' in doc:
        doc['id'] = str(doc['_id'])
        del doc['_id']
    return doc

@menu_bp.route('/', methods=['GET'])
def get_menu():
    db = get_db()
    if db is None:
        return jsonify({'msg': 'Database error'}), 500
    
    menu_items = db['menu']
    menu = list(menu_items.find())
    menu = [serialize_doc(item) for item in menu]
    return jsonify(menu)

@menu_bp.route('/', methods=['POST'])
def add_menu():
    # রোল চেক ছাড়া (ডেমোর জন্য)
    data = request.json
    db = get_db()
    if not db:
        return jsonify({'msg': 'Database error'}), 500
    try:
        menu_items = db['menu']
        menu_doc = {
            'name': data['name'],
            'description': data['description'],
            'price': float(data['price']),
            'category': data['category'],
            'emoji': data['emoji']
        }
        menu_items.insert_one(menu_doc)
        return jsonify({'msg': 'Item added successfully'})
    except Exception as e:
        return jsonify({'msg': 'Failed to add item', 'error': str(e)}), 400

@menu_bp.route('/<string:id>', methods=['PUT'])
def update_menu(id):
    # রোল চেক ছাড়া (ডেমোর জন্য)
    data = request.json
    db = get_db()
    if not db:
        return jsonify({'msg': 'Database error'}), 500
    try:
        menu_items = db['menu']
        update_data = {
            'name': data['name'],
            'description': data['description'],
            'price': float(data['price']),
            'category': data['category'],
            'emoji': data['emoji']
        }
        result = menu_items.update_one({'_id': ObjectId(id)}, {'$set': update_data})
        if result.modified_count > 0:
            return jsonify({'msg': 'Item updated successfully'})
        return jsonify({'msg': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'msg': 'Failed to update item', 'error': str(e)}), 400

@menu_bp.route('/<string:id>', methods=['DELETE'])
def delete_menu(id):
    # রোল চেক ছাড়া (ডেমোর জন্য)
    db = get_db()
    if db is None:
        return jsonify({'msg': 'Database error'}), 500
    try:
        menu_items = db['menu']
        result = menu_items.delete_one({'_id': ObjectId(id)})
        if result.deleted_count > 0:
            return jsonify({'msg': 'Item deleted successfully'})
        return jsonify({'msg': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'msg': 'Failed to delete item', 'error': str(e)}), 400