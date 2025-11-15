from flask import Blueprint, request, jsonify
from db import get_db
from bson import ObjectId

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    db = get_db()
    if db is None:
        return jsonify({'msg': 'Database error'}), 500
    try:
        users = db['users']
        # Check if user exists
        if users.find_one({'username': data['username']}):
            return jsonify({'msg': 'User already exists'}), 400
        
        user_doc = {
            'username': data['username'],
            'password': data['password'],  # পাসওয়ার্ড হ্যাশিং ছাড়া
            'role': data.get('role', 'customer')
        }
        users.insert_one(user_doc)
        return jsonify({'msg': 'User registered successfully'})
    except Exception as e:
        return jsonify({'msg': 'Registration failed', 'error': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    db = get_db()
    if db is None:
        return jsonify({'msg': 'Database error'}), 500
    
    users = db['users']
    user = users.find_one({'username': data['username']})
    
    if user and user['password'] == data['password']:  # সিম্পল পাসওয়ার্ড চেক (ইনসিকিউর)
        role = user['role']
        if role == 'admin':
            token = 'admin_token'
        elif role == 'rider':
            token = 'rider_token'
        else:
            token = 'customer_token'
        return jsonify({'token': token, 'role': role, 'user_id': str(user['_id'])})
    return jsonify({'msg': 'Invalid credentials'}), 400

@auth_bp.route('/me', methods=['GET'])
def me():
    # JWT ছাড়া, সিম্পল রেসপন্স
    return jsonify({'id': 1, 'role': 'customer', 'username': 'testuser'})