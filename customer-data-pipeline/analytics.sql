-- Each query below is preceded by a marker line that gives its report heading.
-- Cancelled orders are excluded from revenue.

-- name: Monthly revenue
SELECT DATE_FORMAT(o.order_date, '%Y-%m') AS month,
       COUNT(DISTINCT o.order_id)          AS orders,
       ROUND(SUM(i.quantity * i.unit_price), 2) AS revenue
FROM cdp_orders o
JOIN cdp_order_items i ON i.order_id = o.order_id
WHERE o.status <> 'cancelled'
GROUP BY month
ORDER BY month;

-- name: Top 5 customers by spend
SELECT c.full_name, c.city,
       COUNT(DISTINCT o.order_id)          AS orders,
       ROUND(SUM(i.quantity * i.unit_price), 2) AS total_spent
FROM cdp_customers c
JOIN cdp_orders o      ON o.customer_id = c.customer_id
JOIN cdp_order_items i ON i.order_id = o.order_id
WHERE o.status <> 'cancelled'
GROUP BY c.customer_id, c.full_name, c.city
ORDER BY total_spent DESC
LIMIT 5;

-- name: Revenue by product category
SELECT p.category,
       SUM(i.quantity)                     AS units_sold,
       ROUND(SUM(i.quantity * i.unit_price), 2) AS revenue
FROM cdp_products p
JOIN cdp_order_items i ON i.product_id = p.product_id
JOIN cdp_orders o      ON o.order_id = i.order_id
WHERE o.status <> 'cancelled'
GROUP BY p.category
ORDER BY revenue DESC;

-- name: Revenue by city
SELECT c.city,
       ROUND(SUM(i.quantity * i.unit_price), 2) AS revenue
FROM cdp_customers c
JOIN cdp_orders o      ON o.customer_id = c.customer_id
JOIN cdp_order_items i ON i.order_id = o.order_id
WHERE o.status <> 'cancelled'
GROUP BY c.city
ORDER BY revenue DESC;

-- name: Repeat customer rate
SELECT COUNT(*) AS customers_with_orders,
       SUM(order_count > 1) AS repeat_customers,
       ROUND(100 * SUM(order_count > 1) / COUNT(*), 1) AS repeat_rate_pct
FROM (
    SELECT customer_id, COUNT(*) AS order_count
    FROM cdp_orders
    WHERE status <> 'cancelled'
    GROUP BY customer_id
) AS per_customer;
