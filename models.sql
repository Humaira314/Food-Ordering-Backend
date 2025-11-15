
-- Users table for authentication
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('customer', 'admin', 'rider') DEFAULT 'customer'
);

-- Menu table for food items
CREATE TABLE menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(255),
    emoji VARCHAR(50)
);

-- Orders table for order management
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    items JSON NOT NULL,  -- Stores items as JSON (e.g., [{"name": "Pizza", "quantity": 2, "price": 500}])
    total DECIMAL(10,2) NOT NULL,
    status VARCHAR(255) DEFAULT 'Pending',
    rider VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
