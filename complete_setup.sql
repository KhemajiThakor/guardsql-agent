-- Complete Database Setup for GuardSQL
-- Run with: sudo -u postgres psql -f complete_setup.sql

-- Note: DROP DATABASE removed for Docker compatibility
-- The database is created by docker-compose environment variables

DROP USER IF EXISTS readonly_user;

-- Create tables
CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    city VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS query_logs (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    generated_sql TEXT,
    status VARCHAR(50) NOT NULL,
    error_message TEXT,
    execution_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample customers
INSERT INTO customers (first_name, last_name, email, city, state, country) VALUES
('John', 'Doe', 'john.doe@email.com', 'New York', 'NY', 'USA'),
('Jane', 'Smith', 'jane.smith@email.com', 'Los Angeles', 'CA', 'USA'),
('Bob', 'Johnson', 'bob.johnson@email.com', 'Chicago', 'IL', 'USA'),
('Alice', 'Williams', 'alice.williams@email.com', 'Houston', 'TX', 'USA'),
('Charlie', 'Brown', 'charlie.brown@email.com', 'Phoenix', 'AZ', 'USA'),
('David', 'Miller', 'david.miller@email.com', 'Austin', 'TX', 'USA'),
('Emma', 'Davis', 'emma.davis@email.com', 'San Francisco', 'CA', 'USA'),
('Frank', 'Wilson', 'frank.wilson@email.com', 'Seattle', 'WA', 'USA'),
('Grace', 'Moore', 'grace.moore@email.com', 'Boston', 'MA', 'USA'),
('Henry', 'Taylor', 'henry.taylor@email.com', 'Miami', 'FL', 'USA');

-- Insert sample products
INSERT INTO products (product_name, category, price, stock_quantity) VALUES
('Laptop Pro 15', 'Electronics', 1299.99, 50),
('Wireless Mouse', 'Electronics', 29.99, 200),
('USB-C Cable', 'Accessories', 12.99, 500),
('Desk Chair', 'Furniture', 249.99, 30),
('Standing Desk', 'Furniture', 599.99, 15),
('Monitor 27"', 'Electronics', 399.99, 40),
('Keyboard Mechanical', 'Electronics', 149.99, 100),
('Webcam HD', 'Electronics', 79.99, 75),
('Desk Lamp', 'Furniture', 45.99, 120),
('Mouse Pad', 'Accessories', 19.99, 300),
('Headphones', 'Electronics', 199.99, 60),
('Phone Stand', 'Accessories', 24.99, 150),
('Cable Organizer', 'Accessories', 14.99, 200),
('Laptop Stand', 'Accessories', 49.99, 80),
('External SSD 1TB', 'Electronics', 129.99, 90);

-- Insert sample orders
INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES
(1, '2024-01-15 10:30:00', 1329.98, 'completed'),
(2, '2024-01-16 14:20:00', 249.99, 'completed'),
(3, '2024-01-17 09:15:00', 949.98, 'shipped'),
(4, '2024-01-18 16:45:00', 89.99, 'processing'),
(5, '2024-01-19 11:30:00', 1949.97, 'completed'),
(6, '2024-01-20 13:15:00', 579.98, 'completed'),
(7, '2024-01-21 15:45:00', 399.99, 'shipped'),
(8, '2024-01-22 10:00:00', 229.98, 'completed'),
(9, '2024-01-23 12:30:00', 1499.98, 'processing'),
(10, '2024-01-24 14:15:00', 149.99, 'completed');

-- Insert sample order items
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 1299.99),
(1, 2, 1, 29.99),
(2, 4, 1, 249.99),
(3, 1, 1, 1299.99),
(4, 2, 3, 29.99),
(5, 5, 1, 599.99),
(5, 1, 1, 1299.99),
(5, 3, 5, 12.99),
(6, 6, 1, 399.99),
(6, 7, 1, 149.99),
(6, 2, 1, 29.99),
(7, 6, 1, 399.99),
(8, 11, 1, 199.99),
(8, 2, 1, 29.99),
(9, 1, 1, 1299.99),
(9, 11, 1, 199.99),
(10, 7, 1, 149.99);

-- Create read-only user
CREATE USER readonly_user WITH PASSWORD 'readonly_pass';
GRANT CONNECT ON DATABASE guardsql_db TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly_user;

-- Grant write access to query_logs
GRANT INSERT, SELECT ON query_logs TO readonly_user;
GRANT USAGE, SELECT ON SEQUENCE query_logs_id_seq TO readonly_user;

-- Verify
SELECT 'Customers: ' || COUNT(*) FROM customers;
SELECT 'Products: ' || COUNT(*) FROM products;
SELECT 'Orders: ' || COUNT(*) FROM orders;
SELECT 'Setup Complete!' as status;
