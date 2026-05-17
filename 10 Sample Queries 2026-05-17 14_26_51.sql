SELECT
    ROUND(SUM(net_sales), 0) AS total_sales,
    ROUND(SUM(gross_profit), 0) AS total_profit,
    SUM(units_sold) AS total_units,
    ROUND(AVG(selling_price), 2) AS avg_selling_price
FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales`;


SELECT
    s.category,
    ROUND(SUM(f.net_sales), 0) AS sales,
    SUM(f.units_sold) AS units,
    ROUND(AVG(f.selling_price), 2) AS avg_price
FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales` f
JOIN `mountainland-ski.Mountainland_Ski.skus` s
    ON f.sku_id = s.sku_id
GROUP BY s.category
ORDER BY sales DESC;


SELECT
    c.retail_season,
    ROUND(SUM(f.net_sales), 0) AS sales,
    SUM(f.units_sold) AS units
FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales` f
JOIN `mountainland-ski.Mountainland_Ski.calendar_weeks` c
    ON f.week_start_date = c.week_start_date
GROUP BY c.retail_season
ORDER BY sales DESC;


SELECT
    st.state,
    ROUND(SUM(f.net_sales), 0) AS sales,
    SUM(f.units_sold) AS units
FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales` f
JOIN `mountainland-ski.Mountainland_Ski.stores` st
    ON f.store_id = st.store_id
GROUP BY st.state
ORDER BY sales DESC
LIMIT 15;

SELECT
    st.retailer_name,
    ROUND(SUM(f.net_sales), 0) AS sales,
    ROUND(SUM(f.gross_profit), 0) AS gross_profit,
    SUM(f.units_sold) AS units
FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales` f
JOIN `mountainland-ski.Mountainland_Ski.stores` st
    ON f.store_id = st.store_id
GROUP BY st.retailer_name
ORDER BY sales DESC;

SELECT
    s.category,
    ROUND(AVG(f.selling_price), 2) AS avg_selling_price
FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales` f
JOIN `mountainland-ski.Mountainland_Ski.skus` s
    ON f.sku_id = s.sku_id
GROUP BY s.category
ORDER BY avg_selling_price DESC;


SELECT
    s.category,
    ROUND(SUM(f.net_sales), 0) AS sales,
    ROUND(SUM(f.gross_profit), 0) AS gross_profit,
    ROUND(SUM(f.gross_profit) / SUM(f.net_sales), 3) AS gross_margin_pct
FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales` f
JOIN `mountainland-ski.Mountainland_Ski.skus` s
    ON f.sku_id = s.sku_id
GROUP BY s.category
ORDER BY gross_margin_pct DESC;



SELECT
    s.synthetic_name,
    ROUND(SUM(f.net_sales), 0) AS sales,
    SUM(f.units_sold) AS units
FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales` f
JOIN `mountainland-ski.Mountainland_Ski.skus` s
    ON f.sku_id = s.sku_id
GROUP BY s.synthetic_name
ORDER BY sales DESC
LIMIT 25;

SELECT
    c.holiday_name,
    ROUND(SUM(f.net_sales), 0) AS sales
FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales` f
JOIN `mountainland-ski.Mountainland_Ski.calendar_weeks` c
    ON f.week_start_date = c.week_start_date
WHERE c.is_holiday_week = 1
GROUP BY c.holiday_name
ORDER BY sales DESC;


SELECT
    EXTRACT(YEAR FROM week_start_date) AS year,
    EXTRACT(MONTH FROM week_start_date) AS month,
    ROUND(SUM(net_sales), 0) AS sales
FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales`
GROUP BY year, month
ORDER BY year, month;


SELECT
    MIN(week_start_date) AS min_date,
    MAX(week_start_date) AS max_date
FROM `mountainland-ski.Mountainland_Ski.calendar_weeks`;




