-- 1. Which retailers had the highest sales by retail season?


-- 2. How did each retailer's monthly sales trend over time?


-- 3. Which retailers had the highest gross margin percentage?


-- 4. For each retailer, which product categories generated the most sales?


-- 5. Which retailer and category combinations sold the most during holiday weeks?


-- 6. Which products had the lowest total sales across the entire dataset?


-- 7. For products in the Park subcategory of the Skis category, show total sales, units, profit, number of colorways, and number of sizes by product.


-- 8. How did "Racetiger SL x Filip Pagowski RM Skis 2026" perform in 2026 YTD by size and colorway?


-- 9. MTNLD has been accused of maintaining a sexist product mix. What percentage of total units sold came from each gender segment by year?
-- Note: I am giving you this one because it contains a CTE: Common Table Expression. Note the "WITH clause at the top".
WITH gender_units_by_year AS (
    SELECT
        EXTRACT(YEAR FROM f.week_start_date) AS year,
        s.gender,
        SUM(f.units_sold) AS total_units
    FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales` f
    JOIN `mountainland-ski.Mountainland_Ski.skus` s
        ON f.sku_id = s.sku_id
    GROUP BY
        year,
        s.gender
)

SELECT
    year,
    gender,
    total_units,
    ROUND(
        total_units * 100.0 / SUM(total_units) OVER (PARTITION BY year),
        2
    ) AS pct_of_year_units
FROM gender_units_by_year
ORDER BY
    year,
    pct_of_year_units DESC;

-- 10. Your boss wants a year-to-date comparison table showing how each category and subcategory is performing in 2026 compared with 2025.
-- Build a query that compares dollars, units, and average selling price for 2025 vs. 2026.
-- Only include weeks 1 through 21 in both years so the comparison is fair.
-- Your final table should be grouped by category and subcategory, and sorted by 2026 dollars from highest to lowest.