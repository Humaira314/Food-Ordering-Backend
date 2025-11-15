# MongoDB Schema Documentation

This project uses MongoDB with the following collections:

## Collections

### users

Stores user authentication and role information.

```json
{
  "_id": ObjectId("..."),
  "username": "john_doe",
  "password": "plain_text_password",  // Note: Should use hashing in production
  "role": "customer"  // Options: customer, admin, rider
}
```

### menu

Stores food items available for ordering.

```json
{
  "_id": ObjectId("..."),
  "name": "Pizza Margherita",
  "description": "Classic Italian pizza",
  "price": 12.99,
  "category": "main-course",  // Options: appetizers, main-course, desserts, drinks
  "emoji": "🍕"
}
```

### orders

Stores customer orders with items and delivery information.

```json
{
  "_id": ObjectId("..."),
  "user_id": "user_object_id_string",
  "items": [
    {
      "name": "Pizza",
      "quantity": 2,
      "price": 12.99
    }
  ],
  "total": 25.98,
  "status": "Pending",  // Options: Pending, Assigned to [rider], Delivered, etc.
  "rider": "rider1",  // Username of assigned rider or null
  "timestamp": ISODate("2025-11-16T...")
}
```

## Indexes (Recommended)

```javascript
// Users collection
db.users.createIndex({ username: 1 }, { unique: true });

// Orders collection
db.orders.createIndex({ user_id: 1 });
db.orders.createIndex({ rider: 1 });
db.orders.createIndex({ status: 1 });
db.orders.createIndex({ timestamp: -1 });
```
