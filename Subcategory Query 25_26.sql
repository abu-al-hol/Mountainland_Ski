SELECT
  s.category,
  s.subcategory,

  ROUND(SUM(CASE WHEN c.year = 2025 THEN f.net_sales ELSE 0 END), 0) AS dollars_2025,
  ROUND(SUM(CASE WHEN c.year = 2026 THEN f.net_sales ELSE 0 END), 0) AS dollars_2026,

  ROUND(
    SAFE_DIVIDE(
      SUM(CASE WHEN c.year = 2026 THEN f.net_sales ELSE 0 END)
      - SUM(CASE WHEN c.year = 2025 THEN f.net_sales ELSE 0 END),
      SUM(CASE WHEN c.year = 2025 THEN f.net_sales ELSE 0 END)
    ),
    3
  ) AS dollars_pct_diff,

  SUM(CASE WHEN c.year = 2025 THEN f.units_sold ELSE 0 END) AS units_2025,
  SUM(CASE WHEN c.year = 2026 THEN f.units_sold ELSE 0 END) AS units_2026,

  ROUND(
    SAFE_DIVIDE(
      SUM(CASE WHEN c.year = 2026 THEN f.units_sold ELSE 0 END)
      - SUM(CASE WHEN c.year = 2025 THEN f.units_sold ELSE 0 END),
      SUM(CASE WHEN c.year = 2025 THEN f.units_sold ELSE 0 END)
    ),
    3
  ) AS units_pct_diff,

  ROUND(
    SAFE_DIVIDE(
      SUM(CASE WHEN c.year = 2025 THEN f.net_sales ELSE 0 END),
      SUM(CASE WHEN c.year = 2025 THEN f.units_sold ELSE 0 END)
    ),
    2
  ) AS asp_2025,

  ROUND(
    SAFE_DIVIDE(
      SUM(CASE WHEN c.year = 2026 THEN f.net_sales ELSE 0 END),
      SUM(CASE WHEN c.year = 2026 THEN f.units_sold ELSE 0 END)
    ),
    2
  ) AS asp_2026,

  ROUND(
    SAFE_DIVIDE(
      SAFE_DIVIDE(
        SUM(CASE WHEN c.year = 2026 THEN f.net_sales ELSE 0 END),
        SUM(CASE WHEN c.year = 2026 THEN f.units_sold ELSE 0 END)
      )
      -
      SAFE_DIVIDE(
        SUM(CASE WHEN c.year = 2025 THEN f.net_sales ELSE 0 END),
        SUM(CASE WHEN c.year = 2025 THEN f.units_sold ELSE 0 END)
      ),
      SAFE_DIVIDE(
        SUM(CASE WHEN c.year = 2025 THEN f.net_sales ELSE 0 END),
        SUM(CASE WHEN c.year = 2025 THEN f.units_sold ELSE 0 END)
      )
    ),
    3
  ) AS asp_pct_diff

FROM `mountainland-ski.Mountainland_Ski.fact_weekly_sales` f
JOIN `mountainland-ski.Mountainland_Ski.skus` s
  ON f.sku_id = s.sku_id
JOIN `mountainland-ski.Mountainland_Ski.calendar_weeks` c
  ON f.week_start_date = c.week_start_date
WHERE c.year IN (2025, 2026)
  AND c.week_of_year <= 21
GROUP BY s.category, s.subcategory
ORDER BY dollars_2026 DESC;