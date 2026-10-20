-- Schema for the customer data pipeline demo.
-- All tables use the cdp_ prefix so they never collide with other tables in the database.

DROP TABLE IF EXISTS cdp_order_items;
DROP TABLE IF EXISTS cdp_orders;
DROP TABLE IF EXISTS cdp_products;
DROP TABLE IF EXISTS cdp_customers;

CREATE TABLE cdp_customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name   VARCHAR(100) NOT NULL,
    email       VARCHAR(150) NOT NULL UNIQUE,
    city        VARCHAR(60)  NOT NULL,
    signup_date DATE         NOT NULL
);

CREATE TABLE cdp_products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100)  NOT NULL,
    category   VARCHAR(50)   NOT NULL,
    price      DECIMAL(10,2) NOT NULL
);

CREATE TABLE cdp_orders (
    order_id    INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT         NOT NULL,
    order_date  DATE        NOT NULL,
    status      VARCHAR(20) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES cdp_customers (customer_id)
);

CREATE TABLE cdp_order_items (
    item_id    INT AUTO_INCREMENT PRIMARY KEY,
    order_id   INT           NOT NULL,
    product_id INT           NOT NULL,
    quantity   INT           NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id)   REFERENCES cdp_orders (order_id),
    FOREIGN KEY (product_id) REFERENCES cdp_products (product_id)
);
