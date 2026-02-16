-- Sample e-commerce database

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

-- Sample data
INSERT INTO customers (first_name, last_name, email, city, state, country) VALUES
('John', 'Doe', 'john.doe@email.com', 'New York', 'NY', 'USA'),
('Jane', 'Smith', 'jane.smith@email.com', 'Los Angeles', 'CA', 'USA'),
('Bob', 'Johnson', 'bob.johnson@email.com', 'Chicago', 'IL', 'USA'),
('Alice', 'Williams', 'alice.williams@email.com', 'Houston', 'TX', 'USA'),
('Charlie', 'Brown', 'charlie.brown@email.com', 'Phoenix', 'AZ', 'USA');

INSERT INTO products (product_name, category, price, stock_quantity) VALUES
('Laptop Pro 15', 'Electronics', 1299.99, 50),
('Wireless Mouse', 'Electronics', 29.99, 200),
('USB-C Cable', 'Accessories', 12.99, 500),
('Desk Chair', 'Furniture', 249.99, 30),
('Standing Desk', 'Furniture', 599.99, 15);

INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES
(1, '2024-01-15 10:30:00', 1329.98, 'completed'),
(2, '2024-01-16 14:20:00', 249.99, 'completed'),
(3, '2024-01-17 09:15:00', 949.98, 'shipped'),
(4, '2024-01-18 16:45:00', 89.99, 'processing'),
(5, '2024-01-19 11:30:00', 1949.97, 'completed');

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 1299.99),
(1, 2, 1, 29.99),
(2, 4, 1, 249.99),
(3, 1, 1, 1299.99),
(4, 2, 3, 29.99);

-- Create read-only user
CREATE USER readonly_user WITH PASSWORD 'readonly_pass';
GRANT CONNECT ON DATABASE guardsql_db TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly_user;

-- Grant write access to query_logs
GRANT INSERT ON query_logs TO readonly_user;
GRANT USAGE, SELECT ON SEQUENCE query_logs_id_seq TO readonly_user;
