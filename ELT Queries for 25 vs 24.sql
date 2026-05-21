-- Slide 1: Category performance comparison for full-year 2024 vs full-year 2025, including gross profit
SELECT
  s.category,

  ROUND(SUM(CASE WHEN c.year = 2024 THEN f.net_sales ELSE 0 END), 0) AS dollars_2024,
  ROUND(SUM(CASE WHEN c.year = 2025 THEN f.net_sales ELSE 0 END), 0) AS dollars_2025,

  ROUND(
    SAFE_DIVIDE(
      SUM(CASE WHEN c.year = 2025 THEN f.net_sales ELSE 0 END)
      - SUM(CASE WHEN c.year = 2024 THEN f.net_sales ELSE 0 END),
      SUM(CASE WHEN c.year = 2024 THEN f.net_sales ELSE 0 END)
    ),
    3
  ) AS dollars_pct_diff,

  SUM(CASE WHEN c.year = 2024 THEN f.units_sold ELSE 0 END) AS units_2024,
  SUM(CASE WHEN c.year = 2025 THEN f.units_sold ELSE 0 END) AS units_2025,

  ROUND(
    SAFE_DIVIDE(
      SUM(CASE WHEN c.year = 2025 THEN f.units_sold ELSE 0 END)
      - SUM(CASE WHEN c.year = 2024 THEN f.units_sold ELSE 0 END),
      SUM(CASE WHEN c.year = 2024 THEN f.units_sold ELSE 0 END)
    ),
    3
  ) AS units_pct_diff,

  ROUND(SUM(CASE WHEN c.year = 2024 THEN f.gross_profit ELSE 0 END), 0) AS gross_profit_2024,
  ROUND(SUM(CASE WHEN c.year = 2025 THEN f.gross_profit ELSE 0 END), 0) AS gross_profit_2025,

  ROUND(
    SAFE_DIVIDE(
      SUM(CASE WHEN c.year = 2025 THEN f.gross_profit ELSE 0 END)
      - SUM(CASE WHEN c.year = 2024 THEN f.gross_profit ELSE 0 END),
      SUM(CASE WHEN c.year = 2024 THEN f.gross_profit ELSE 0 END)
    ),
    3
  ) AS gross_profit_pct_diff,

  ROUND(
    SAFE_DIVIDE(
      SUM(CASE WHEN c.year = 2024 THEN f.net_sales ELSE 0 END),
      SUM(CASE WHEN c.year = 2024 THEN f.units_sold ELSE 0 END)
    ),
    2
  ) AS asp_2024,

  ROUND(
    SAFE_DIVIDE(
      SUM(CASE WHEN c.year = 2025 THEN f.net_sales ELSE 0 END),
      SUM(CASE WHEN c.year = 2025 THEN f.units_sold ELSE 0 END)
    ),
    2
  ) AS asp_2025,

  ROUND(
    SAFE_DIVIDE(
      SAFE_DIVIDE(
        SUM(CASE WHEN c.year = 2025 THEN f.net_sales ELSE 0 END),
        SUM(CASE WHEN c.year = 2025 THEN f.units_sold ELSE 0 END)
      )
      -
      SAFE_DIVIDE(
        SUM(CASE WHEN c.year = 2024 THEN f.net_sales ELSE 0 END),
        SUM(CASE WHEN c.year = 2024 THEN f.units_sold ELSE 0 END)
      ),
      SAFE_DIVIDE(
        SUM(CASE WHEN c.year = 2024 THEN f.net_sales ELSE 0 END),
        SUM(CASE WHEN c.year = 2024 THEN f.units_sold ELSE 0 END)
      )
    ),
    3
  ) AS asp_pct_diff

FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales` f
JOIN `mountainland-ski.Mountainland_Ski.skus` s
  ON f.sku_id = s.sku_id
JOIN `mountainland-ski.Mountainland_Ski.calendar_weeks` c
  ON f.week_start_date = c.week_start_date
WHERE c.year IN (2024, 2025)
GROUP BY s.category
ORDER BY dollars_2025 DESC;


-- Monthly company performance for 2024 and 2025, aggregated across all categories, products, retailers, and stores
-- (Makes a nice monthly line chart for ELT slide deck.)
SELECT
  c.year,
  c.month,
  FORMAT_DATE('%b', MIN(f.week_start_date)) AS month_name,

  ROUND(SUM(f.net_sales), 0) AS sales,
  SUM(f.units_sold) AS units,
  ROUND(SUM(f.gross_profit), 0) AS gross_profit,

  ROUND(
    SAFE_DIVIDE(SUM(f.net_sales), SUM(f.units_sold)),
    2
  ) AS asp

FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales` f
JOIN `mountainland-ski.Mountainland_Ski.calendar_weeks` c
  ON f.week_start_date = c.week_start_date

WHERE c.year IN (2024, 2025)

GROUP BY
  c.year,
  c.month

ORDER BY
  c.year,
  c.month;



-- Retailer performance comparison for full-year 2024 vs full-year 2025, including store counts
SELECT
  st.retailer_name,

  ROUND(SUM(CASE WHEN c.year = 2024 THEN f.net_sales ELSE 0 END), 0) AS sales_2024,
  ROUND(SUM(CASE WHEN c.year = 2025 THEN f.net_sales ELSE 0 END), 0) AS sales_2025,

  ROUND(
    SAFE_DIVIDE(
      SUM(CASE WHEN c.year = 2025 THEN f.net_sales ELSE 0 END)
      - SUM(CASE WHEN c.year = 2024 THEN f.net_sales ELSE 0 END),
      SUM(CASE WHEN c.year = 2024 THEN f.net_sales ELSE 0 END)
    ),
    3
  ) AS sales_pct_chg,

  SUM(CASE WHEN c.year = 2024 THEN f.units_sold ELSE 0 END) AS units_2024,
  SUM(CASE WHEN c.year = 2025 THEN f.units_sold ELSE 0 END) AS units_2025,

  ROUND(
    SAFE_DIVIDE(
      SUM(CASE WHEN c.year = 2025 THEN f.units_sold ELSE 0 END)
      - SUM(CASE WHEN c.year = 2024 THEN f.units_sold ELSE 0 END),
      SUM(CASE WHEN c.year = 2024 THEN f.units_sold ELSE 0 END)
    ),
    3
  ) AS units_pct_chg,

  ROUND(
    SAFE_DIVIDE(
      SUM(CASE WHEN c.year = 2024 THEN f.net_sales ELSE 0 END),
      SUM(CASE WHEN c.year = 2024 THEN f.units_sold ELSE 0 END)
    ),
    2
  ) AS asp_2024,

  ROUND(
    SAFE_DIVIDE(
      SUM(CASE WHEN c.year = 2025 THEN f.net_sales ELSE 0 END),
      SUM(CASE WHEN c.year = 2025 THEN f.units_sold ELSE 0 END)
    ),
    2
  ) AS asp_2025,

  ROUND(
    SAFE_DIVIDE(
      SAFE_DIVIDE(
        SUM(CASE WHEN c.year = 2025 THEN f.net_sales ELSE 0 END),
        SUM(CASE WHEN c.year = 2025 THEN f.units_sold ELSE 0 END)
      )
      -
      SAFE_DIVIDE(
        SUM(CASE WHEN c.year = 2024 THEN f.net_sales ELSE 0 END),
        SUM(CASE WHEN c.year = 2024 THEN f.units_sold ELSE 0 END)
      ),
      SAFE_DIVIDE(
        SUM(CASE WHEN c.year = 2024 THEN f.net_sales ELSE 0 END),
        SUM(CASE WHEN c.year = 2024 THEN f.units_sold ELSE 0 END)
      )
    ),
    3
  ) AS asp_pct_chg,

  COUNT(DISTINCT CASE WHEN c.year = 2024 THEN f.sku_id END) AS sku_count_2024,
  COUNT(DISTINCT CASE WHEN c.year = 2025 THEN f.sku_id END) AS sku_count_2025,

  ROUND(
    SAFE_DIVIDE(
      COUNT(DISTINCT CASE WHEN c.year = 2025 THEN f.sku_id END)
      - COUNT(DISTINCT CASE WHEN c.year = 2024 THEN f.sku_id END),
      COUNT(DISTINCT CASE WHEN c.year = 2024 THEN f.sku_id END)
    ),
    3
  ) AS sku_pct_chg,

  COUNT(DISTINCT CASE WHEN c.year = 2024 THEN st.store_id END) AS store_count_2024,
  COUNT(DISTINCT CASE WHEN c.year = 2025 THEN st.store_id END) AS store_count_2025,

  ROUND(
    SAFE_DIVIDE(
      COUNT(DISTINCT CASE WHEN c.year = 2025 THEN st.store_id END)
      - COUNT(DISTINCT CASE WHEN c.year = 2024 THEN st.store_id END),
      COUNT(DISTINCT CASE WHEN c.year = 2024 THEN st.store_id END)
    ),
    3
  ) AS store_pct_chg

FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales` f
JOIN `mountainland-ski.Mountainland_Ski.stores` st
  ON f.store_id = st.store_id
JOIN `mountainland-ski.Mountainland_Ski.calendar_weeks` c
  ON f.week_start_date = c.week_start_date

WHERE c.year IN (2024, 2025)

GROUP BY st.retailer_name

ORDER BY sales_2025 DESC;

-- Weekly company-level performance across the full dataset
-- Output includes date, year, quarter, week number, units, sales dollars, and ASP.
-- This should produce one row per week in the dataset.

SELECT
  f.week_start_date,
  c.year,
  c.quarter,
  c.week_of_year,

  SUM(f.units_sold) AS units,

  ROUND(SUM(f.net_sales), 0) AS dollars,

  ROUND(
    SAFE_DIVIDE(
      SUM(f.net_sales),
      SUM(f.units_sold)
    ),
    2
  ) AS asp

FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales` f
JOIN `mountainland-ski.Mountainland_Ski.calendar_weeks` c
  ON f.week_start_date = c.week_start_date

GROUP BY
  f.week_start_date,
  c.year,
  c.quarter,
  c.week_of_year

ORDER BY
  f.week_start_date;

  -- Category and subcategory performance comparison for full-year 2024 vs full-year 2025
SELECT
  s.category,
  s.subcategory,

  ROUND(SUM(CASE WHEN c.year = 2024 THEN f.net_sales ELSE 0 END), 0) AS dollars_2024,
  ROUND(SUM(CASE WHEN c.year = 2025 THEN f.net_sales ELSE 0 END), 0) AS dollars_2025,

  ROUND(
    SAFE_DIVIDE(
      SUM(CASE WHEN c.year = 2025 THEN f.net_sales ELSE 0 END)
      - SUM(CASE WHEN c.year = 2024 THEN f.net_sales ELSE 0 END),
      SUM(CASE WHEN c.year = 2024 THEN f.net_sales ELSE 0 END)
    ),
    3
  ) AS dollars_pct_diff,

  SUM(CASE WHEN c.year = 2024 THEN f.units_sold ELSE 0 END) AS units_2024,
  SUM(CASE WHEN c.year = 2025 THEN f.units_sold ELSE 0 END) AS units_2025,

  ROUND(
    SAFE_DIVIDE(
      SUM(CASE WHEN c.year = 2025 THEN f.units_sold ELSE 0 END)
      - SUM(CASE WHEN c.year = 2024 THEN f.units_sold ELSE 0 END),
      SUM(CASE WHEN c.year = 2024 THEN f.units_sold ELSE 0 END)
    ),
    3
  ) AS units_pct_diff,

  ROUND(
    SAFE_DIVIDE(
      SUM(CASE WHEN c.year = 2024 THEN f.net_sales ELSE 0 END),
      SUM(CASE WHEN c.year = 2024 THEN f.units_sold ELSE 0 END)
    ),
    2
  ) AS asp_2024,

  ROUND(
    SAFE_DIVIDE(
      SUM(CASE WHEN c.year = 2025 THEN f.net_sales ELSE 0 END),
      SUM(CASE WHEN c.year = 2025 THEN f.units_sold ELSE 0 END)
    ),
    2
  ) AS asp_2025,

  ROUND(
    SAFE_DIVIDE(
      SAFE_DIVIDE(
        SUM(CASE WHEN c.year = 2025 THEN f.net_sales ELSE 0 END),
        SUM(CASE WHEN c.year = 2025 THEN f.units_sold ELSE 0 END)
      )
      -
      SAFE_DIVIDE(
        SUM(CASE WHEN c.year = 2024 THEN f.net_sales ELSE 0 END),
        SUM(CASE WHEN c.year = 2024 THEN f.units_sold ELSE 0 END)
      ),
      SAFE_DIVIDE(
        SUM(CASE WHEN c.year = 2024 THEN f.net_sales ELSE 0 END),
        SUM(CASE WHEN c.year = 2024 THEN f.units_sold ELSE 0 END)
      )
    ),
    3
  ) AS asp_pct_diff

FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales` f
JOIN `mountainland-ski.Mountainland_Ski.skus` s
  ON f.sku_id = s.sku_id
JOIN `mountainland-ski.Mountainland_Ski.calendar_weeks` c
  ON f.week_start_date = c.week_start_date
WHERE c.year IN (2024, 2025)
GROUP BY s.category, s.subcategory
ORDER BY dollars_2025 DESC;


-- Top 5 SKUs by gross profit for full-year 2025
-- Includes sales, units, pricing metrics, and gross margin %

SELECT
  s.synthetic_name,

  ROUND(SUM(f.net_sales), 0) AS sales,
  SUM(f.units_sold) AS units,

  ROUND(MIN(f.selling_price), 2) AS min_asp,
  ROUND(MAX(f.selling_price), 2) AS max_asp,
  ROUND(AVG(f.selling_price), 2) AS avg_asp,

  ROUND(SUM(f.gross_profit), 0) AS gross_profit,

  ROUND(
    SAFE_DIVIDE(
      SUM(f.gross_profit),
      SUM(f.net_sales)
    ),
    3
  ) AS gross_margin_pct

FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales` f

JOIN `mountainland-ski.Mountainland_Ski.skus` s
  ON f.sku_id = s.sku_id

JOIN `mountainland-ski.Mountainland_Ski.calendar_weeks` c
  ON f.week_start_date = c.week_start_date

WHERE c.year = 2025

GROUP BY
  s.synthetic_name

ORDER BY
  gross_profit DESC

LIMIT 5;

-- Bottom 5 SKUs by gross profit for full-year 2025
-- Includes sales, units, pricing metrics, and gross margin %

SELECT
  s.synthetic_name,

  ROUND(SUM(f.net_sales), 0) AS sales,
  SUM(f.units_sold) AS units,

  ROUND(MIN(f.selling_price), 2) AS min_asp,
  ROUND(MAX(f.selling_price), 2) AS max_asp,
  ROUND(AVG(f.selling_price), 2) AS avg_asp,

  ROUND(SUM(f.gross_profit), 0) AS gross_profit,

  ROUND(
    SAFE_DIVIDE(
      SUM(f.gross_profit),
      SUM(f.net_sales)
    ),
    3
  ) AS gross_margin_pct

FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales` f

JOIN `mountainland-ski.Mountainland_Ski.skus` s
  ON f.sku_id = s.sku_id

JOIN `mountainland-ski.Mountainland_Ski.calendar_weeks` c
  ON f.week_start_date = c.week_start_date

WHERE c.year = 2025

GROUP BY
  s.synthetic_name

ORDER BY
  gross_profit ASC

LIMIT 5;


-- Monthly unit sales trend for:
-- Racetiger SL x Filip Pagowski RM Skis 2026
-- Use output for a monthly line chart in Excel

SELECT
  c.month,
  FORMAT_DATE('%b', MIN(f.week_start_date)) AS month_name,

  SUM(f.units_sold) AS units

FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales` f

JOIN `mountainland-ski.Mountainland_Ski.skus` s
  ON f.sku_id = s.sku_id

JOIN `mountainland-ski.Mountainland_Ski.calendar_weeks` c
  ON f.week_start_date = c.week_start_date

WHERE c.year = 2025
  AND s.synthetic_name = 'Racetiger SL x Filip Pagowski RM Skis 2026'

GROUP BY
  c.month

ORDER BY
  c.month;