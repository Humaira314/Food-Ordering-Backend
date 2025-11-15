from flask import Flask, send_from_directory, abort
from flask_cors import CORS
from routes.auth import auth_bp
from routes.menu import menu_bp
from routes.orders import orders_bp
from routes.riders import riders_bp
from dotenv import load_dotenv
from db import get_db
load_dotenv()
import os


def _build_frontend_path(*parts: str) -> str:
    """Return an absolute path inside the Forntend directory."""
    # Look for Forntend in the same directory as app.py
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Forntend'))
    return os.path.join(base_dir, *parts)


CUSTOMER_DIR = _build_frontend_path('customer panel')
ADMIN_DIR = _build_frontend_path('Admin panel')
RIDER_DIR = _build_frontend_path('rider panel')

app = Flask(__name__, static_folder=CUSTOMER_DIR, static_url_path='')
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

# Configure CORS to allow Vercel frontend
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://food-ordering-gray.vercel.app",
            "https://food-ordering-backend-b3k6.onrender.com",
            "http://127.0.0.1:5000",  # For local development
            "http://localhost:5000"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# 🧩 API Blueprints register করা
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(menu_bp, url_prefix='/api/menu')
app.register_blueprint(orders_bp, url_prefix='/api/orders')
app.register_blueprint(riders_bp, url_prefix='/api/riders')


def _safe_send(directory: str, filename: str):
    file_path = os.path.join(directory, filename)
    if not os.path.exists(file_path):
        abort(404)
    return send_from_directory(directory, filename)


@app.route('/')
def serve_home():
    return _safe_send(CUSTOMER_DIR, 'index.html')


@app.route('/admin')
def serve_admin_index():
    return _safe_send(ADMIN_DIR, 'index.html')


@app.route('/admin/<path:path>')
def serve_admin_assets(path: str):
    return send_from_directory(ADMIN_DIR, path)


@app.route('/rider')
def serve_rider_index():
    return _safe_send(RIDER_DIR, 'index.html')


@app.route('/rider/<path:path>')
def serve_rider_assets(path: str):
    return send_from_directory(RIDER_DIR, path)


# 🔍 Test route — Flask ঠিক চলছে কিনা দেখতে
@app.route('/ping')
def ping():
    return {'message': 'Server is working!'}


if __name__ == '__main__':
    # Test MongoDB connection on startup
    print("\n🔄 Testing MongoDB connection...")
    db = get_db()
    if db is not None:
        print("🎉 Ready to accept requests!\n")
    else:
        print("⚠️  Server starting without database connection!\n")
    
    app.run(debug=True, port=5000)

