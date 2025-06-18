SELECT id,
       quantity,
       address,
       phone,
       date,
       status,
       product_id,
       customer_id
  FROM store_order;


SELECT 
    SUM(quantity) AS total_quantity,
    date,
    product_id,
    COUNT(customer_id) AS customer_count
FROM 
    store_order
WHERE 
    date >= '2024-11-06' AND 
    date <= '2024-11-13'
GROUP BY 
    product_id, date
HAVING 
    total_quantity >= 1;

    
SELECT 
    SUM(quantity) AS total_quantity,
    date,
    product_id,
    COUNT(customer_id) AS customer_count
FROM 
    store_order
WHERE 
    date >= DATE('now', '-30 days') AND 
    date <= DATE('now')
GROUP BY 
    product_id, date
HAVING 
    total_quantity >= 1;

SELECT 
    product_id,
    SUM(quantity) AS total_quantity
FROM 
    store_order
WHERE 
    date >= DATE('now', '-30 days') AND 
    date <= DATE('now')
GROUP BY 
    product_id
ORDER BY 
    total_quantity DESC
LIMIT 5;

UPDATE store_product
SET price = price * 1.1  
WHERE id IN (
    SELECT 
       id
    FROM (
        SELECT 
            id
        FROM 
            store_order
        WHERE 
            date >= DATE('now', '-30 days') AND 
            date <= DATE('now')
        GROUP BY 
            id
        ORDER BY 
            SUM(quantity) DESC
        LIMIT 5
    )
);
