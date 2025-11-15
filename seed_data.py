"""
Seed script to populate MongoDB with initial data for the food ordering system.
Run this script once to set up initial users, menu items, and sample orders.

Usage:
    python seed_data.py
"""

import os
from dotenv import load_dotenv
from db import get_db
from datetime import datetime

load_dotenv()


def seed_users(db):
    """Insert sample users (customer, admin, rider)."""
    users = db['users']
    
    # Check if users already exist
    if users.count_documents({}) > 0:
        print("⚠️  Users collection already has data. Skipping users...")
        return
    
    sample_users = [
        {
            'username': 'admin',
            'password': 'admin123',  # Plain text for demo - use hashing in production
            'role': 'admin'
        },
        {
            'username': 'customer1',
            'password': 'customer123',
            'role': 'customer'
        },
        {
            'username': 'rider1',
            'password': 'rider123',
            'role': 'rider'
        },
        {
            'username': 'rider2',
            'password': 'rider123',
            'role': 'rider'
        }
    ]
    
    result = users.insert_many(sample_users)
    print(f"✅ Inserted {len(result.inserted_ids)} users")


def seed_menu(db):
    """Insert sample menu items."""
    menu = db['menu']
    
    # Check if menu already has items
    if menu.count_documents({}) > 0:
        print("⚠️  Menu collection already has data. Skipping menu...")
        return
    
    sample_menu = [
        # Appetizers
        {
            'name': 'Spring Rolls',
            'description': 'Crispy vegetable spring rolls with sweet chili sauce',
            'price': 5.99,
            'category': 'appetizers',
            'emoji': '🥟'
        },
        {
            'name': 'Chicken Wings',
            'description': 'Spicy buffalo wings with ranch dressing',
            'price': 8.99,
            'category': 'appetizers',
            'emoji': '🍗'
        },
        {
            'name': 'Garlic Bread',
            'description': 'Toasted bread with garlic butter and herbs',
            'price': 4.50,
            'category': 'appetizers',
            'emoji': '🥖'
        },
        
        # Main Course
        {
            'name': 'Margherita Pizza',
            'description': 'Classic Italian pizza with tomato, mozzarella, and basil',
            'price': 12.99,
            'category': 'main-course',
            'emoji': '🍕'
        },
        {
            'name': 'Beef Burger',
            'description': 'Juicy beef patty with lettuce, tomato, and special sauce',
            'price': 10.99,
            'category': 'main-course',
            'emoji': '🍔'
        },
        {
            'name': 'Chicken Biryani',
            'description': 'Aromatic basmati rice with spiced chicken',
            'price': 14.99,
            'category': 'main-course',
            'emoji': '🍛'
        },
        {
            'name': 'Pad Thai',
            'description': 'Thai stir-fried noodles with shrimp and peanuts',
            'price': 13.99,
            'category': 'main-course',
            'emoji': '🍜'
        },
        {
            'name': 'Grilled Salmon',
            'description': 'Fresh Atlantic salmon with lemon butter sauce',
            'price': 18.99,
            'category': 'main-course',
            'emoji': '🐟'
        },
        
        # Desserts
        {
            'name': 'Chocolate Cake',
            'description': 'Rich chocolate layer cake with ganache',
            'price': 6.99,
            'category': 'desserts',
            'emoji': '🍰'
        },
        {
            'name': 'Ice Cream Sundae',
            'description': 'Vanilla ice cream with chocolate sauce and cherry',
            'price': 5.50,
            'category': 'desserts',
            'emoji': '🍨'
        },
        {
            'name': 'Tiramisu',
            'description': 'Italian coffee-flavored dessert',
            'price': 7.99,
            'category': 'desserts',
            'emoji': '🍮'
        },
        
        # Drinks
        {
            'name': 'Coca Cola',
            'description': 'Chilled soft drink (330ml)',
            'price': 2.50,
            'category': 'drinks',
            'emoji': '🥤'
        },
        {
            'name': 'Fresh Orange Juice',
            'description': 'Freshly squeezed orange juice',
            'price': 4.99,
            'category': 'drinks',
            'emoji': '🍊'
        },
        {
            'name': 'Iced Coffee',
            'description': 'Cold brew coffee with milk',
            'price': 4.50,
            'category': 'drinks',
            'emoji': '☕'
        },
        {
            'name': 'Mango Lassi',
            'description': 'Sweet yogurt drink with mango',
            'price': 3.99,
            'category': 'drinks',
            'emoji': '🥭'
        }
    ]
    
    result = menu.insert_many(sample_menu)
    print(f"✅ Inserted {len(result.inserted_ids)} menu items")


def seed_orders(db):
    """Insert sample orders."""
    orders = db['orders']
    users = db['users']
    
    # Check if orders already exist
    if orders.count_documents({}) > 0:
        print("⚠️  Orders collection already has data. Skipping orders...")
        return
    
    # Get customer user_id
    customer = users.find_one({'username': 'customer1'})
    if not customer:
        print("⚠️  No customer found. Skipping sample orders...")
        return
    
    customer_id = str(customer['_id'])
    
    sample_orders = [
        {
            'user_id': customer_id,
            'items': [
                {'name': 'Margherita Pizza', 'quantity': 2, 'price': 12.99},
                {'name': 'Coca Cola', 'quantity': 2, 'price': 2.50}
            ],
            'total': 30.98,
            'status': 'Pending',
            'rider': None,
            'timestamp': datetime.utcnow()
        },
        {
            'user_id': customer_id,
            'items': [
                {'name': 'Beef Burger', 'quantity': 1, 'price': 10.99},
                {'name': 'Chicken Wings', 'quantity': 1, 'price': 8.99},
                {'name': 'Iced Coffee', 'quantity': 1, 'price': 4.50}
            ],
            'total': 24.48,
            'status': 'Assigned to rider1',
            'rider': 'rider1',
            'timestamp': datetime.utcnow()
        }
    ]
    
    result = orders.insert_many(sample_orders)
    print(f"✅ Inserted {len(result.inserted_ids)} sample orders")


def main():
    """Main function to seed all collections."""
    print("\n🌱 Starting database seeding...\n")
    
    db = get_db()
    if db is None:
        print("❌ Failed to connect to MongoDB. Check your .env configuration.")
        return
    
    print(f"📦 Seeding database: {os.getenv('DB_NAME', 'food_ordering')}\n")
    
    try:
        seed_users(db)
        seed_menu(db)
        seed_orders(db)
        
        print("\n🎉 Database seeding completed successfully!")
        print("\n📊 Summary:")
        print(f"   - Users: {db['users'].count_documents({})}")
        print(f"   - Menu Items: {db['menu'].count_documents({})}")
        print(f"   - Orders: {db['orders'].count_documents({})}")
        
        print("\n🔐 Test Credentials:")
        print("   Admin: username=admin, password=admin123")
        print("   Customer: username=customer1, password=customer123")
        print("   Rider: username=rider1, password=rider123")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")


if __name__ == '__main__':
    main()
