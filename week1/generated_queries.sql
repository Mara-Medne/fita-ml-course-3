-- Jautājums 1: Kopējais maksājumu apjoms pa organizācijām
SELECT o.id AS organisation_id, o.parent_vertical, SUM(p.amount) AS total_payments
FROM payments p
JOIN mandates m ON p.mandate_id = m.id
JOIN organisations o ON m.organisation_id = o.id
GROUP BY o.id, o.parent_vertical
ORDER BY total_payments DESC;

-- Jautājums 2: Cik mandātu katrai organizācijai
SELECT o.id AS organisation_id, o.parent_vertical, COUNT(m.id) AS mandate_count
FROM mandates m
JOIN organisations o ON m.organisation_id = o.id
GROUP BY o.id, o.parent_vertical
ORDER BY mandate_count DESC;

-- Jautājums 3: Vidējais maksājuma apjoms pa gadiem
SELECT YEAR(p.created_at) AS payment_year, AVG(p.amount) AS avg_payment
FROM payments p
GROUP BY YEAR(p.created_at)
ORDER BY payment_year;
