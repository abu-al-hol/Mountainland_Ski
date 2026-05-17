import streamlit as st
import sqlite3
import pandas as pd
import random
import os
from datetime import datetime, timedelta

DB_NAME = "ski_catalog.db"

CATEGORIES = {
    "Skis": ["All-Mountain", "Powder", "Touring", "Park"],
    "Snowboards": ["All-Mountain", "Powder", "Splitboard"],
    "Boots": ["Ski Boots", "Snowboard Boots", "Touring Boots"],
    "Jackets": ["Shell", "Insulated", "Down", "Softshell"],
    "Ski Pants": ["Shell Pants", "Insulated Pants", "Bib Pants"],
    "Gloves": ["Gloves", "Mittens", "Liners"],
    "Base Layers": ["Tops", "Bottoms", "One-Piece"],
    "Helmets": ["Ski Helmet", "Snowboard Helmet"],
    "Goggles": ["Low Light", "All Conditions", "Replacement Lens"],
    "Poles": ["Alpine", "Touring", "Adjustable"],
    "Packs": ["Ski Pack", "Avalanche Pack", "Day Pack"],
    "Accessories": ["Beanies", "Socks", "Neck Gaiters", "Tools", "Replacement Parts"],
}

STORE_MARKETS = [
    ("West", "CO", "Denver", "Large", 95),
    ("West", "CO", "Boulder", "Medium", 98),
    ("West", "UT", "Salt Lake City", "Large", 96),
    ("West", "UT", "Park City", "Small", 100),
    ("West", "CA", "Truckee", "Small", 96),
    ("West", "CA", "Sacramento", "Large", 70),
    ("West", "WA", "Seattle", "Large", 78),
    ("West", "OR", "Bend", "Medium", 90),
    ("Mountain", "ID", "Boise", "Medium", 78),
    ("Mountain", "MT", "Bozeman", "Small", 97),
    ("Mountain", "WY", "Jackson", "Small", 100),
    ("Northeast", "VT", "Burlington", "Small", 94),
    ("Northeast", "NH", "Concord", "Small", 88),
    ("Northeast", "ME", "Portland", "Medium", 82),
    ("Northeast", "MA", "Boston", "Large", 70),
    ("Midwest", "MN", "Minneapolis", "Large", 72),
    ("Midwest", "MI", "Grand Rapids", "Medium", 68),
    ("Midwest", "WI", "Madison", "Medium", 66),
    ("Southwest", "AZ", "Flagstaff", "Small", 80),
    ("Southwest", "NV", "Reno", "Medium", 86),
    ("Southwest", "NM", "Santa Fe", "Small", 76),
    ("South", "TX", "Austin", "Large", 30),
    ("Central", "IL", "Chicago", "Large", 45),
]

RETAILERS = [
    ("REI", 45, "Large Retail", "Outdoor Specialty"),
    ("Dick's Sporting Goods", 40, "Large Retail", "Sporting Goods"),
    ("Scheels", 20, "Large Retail", "Sporting Goods"),
    ("Evo", 8, "Specialty Retail", "Snow Specialty"),
    ("Backcountry", 1, "Online Retail", "Online Marketplace"),
    ("Christy Sports", 20, "Specialty Retail", "Snow Specialty"),
    ("Sun & Ski Sports", 20, "Specialty Retail", "Outdoor Specialty"),
    ("Independent Mountain Shop", 60, "Small Retail", "Local Specialty"),
    ("Summit Ridge Online", 1, "Owned Direct", "DTC Online"),
]


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_families (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_brand TEXT,
            synthetic_brand TEXT,
            original_name TEXT,
            synthetic_name TEXT,
            category TEXT,
            subcategory TEXT,
            gender TEXT,
            season_year INTEGER,
            msrp REAL,
            current_price REAL,
            sizes TEXT,
            colors TEXT,
            description TEXT,
            features TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skus (
            sku_id TEXT PRIMARY KEY,
            product_family_id INTEGER,
            synthetic_name TEXT,
            category TEXT,
            subcategory TEXT,
            gender TEXT,
            size TEXT,
            color TEXT,
            msrp REAL,
            current_price REAL,
            baseline_price REAL,
            gross_margin_pct REAL,
            unit_cost REAL,
            price_tier TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            store_id TEXT PRIMARY KEY,
            retailer_name TEXT,
            store_name TEXT,
            channel TEXT,
            retailer_tier TEXT,
            store_type TEXT,
            region TEXT,
            state TEXT,
            city TEXT,
            market_size TEXT,
            snow_market_score INTEGER,
            is_online INTEGER,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calendar_weeks (
            week_start_date TEXT PRIMARY KEY,
            week_end_date TEXT,
            year INTEGER,
            month INTEGER,
            quarter INTEGER,
            week_of_year INTEGER,
            season TEXT,
            retail_season TEXT,
            is_holiday_week INTEGER,
            holiday_name TEXT,
            is_black_friday_week INTEGER,
            is_christmas_week INTEGER,
            is_presidents_day_week INTEGER,
            is_memorial_day_week INTEGER,
            is_labor_day_week INTEGER,
            is_peak_ski_season INTEGER,
            is_preseason INTEGER,
            is_spring_clearance INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_weekly_sales (
            sales_id INTEGER PRIMARY KEY AUTOINCREMENT,
            week_start_date TEXT,
            store_id TEXT,
            sku_id TEXT,
            units_sold INTEGER,
            baseline_price REAL,
            discount_pct REAL,
            selling_price REAL,
            gross_sales REAL,
            net_sales REAL,
            unit_cost REAL,
            cogs REAL,
            gross_profit REAL,
            inventory_on_hand INTEGER,
            units_returned INTEGER,
            promo_flag INTEGER,
            markdown_flag INTEGER,
            stockout_flag INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def migrate_skus_table():
    conn = connect_db()
    cursor = conn.cursor()

    columns_to_add = {
        "baseline_price": "REAL",
        "gross_margin_pct": "REAL",
        "unit_cost": "REAL",
        "price_tier": "TEXT",
    }

    cursor.execute("PRAGMA table_info(skus)")
    existing_columns = [column[1] for column in cursor.fetchall()]

    for column_name, column_type in columns_to_add.items():
        if column_name not in existing_columns:
            cursor.execute(f"ALTER TABLE skus ADD COLUMN {column_name} {column_type}")

    conn.commit()
    conn.close()


def save_product(product):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO product_families (
            source_brand, synthetic_brand, original_name, synthetic_name,
            category, subcategory, gender, season_year, msrp, current_price,
            sizes, colors, description, features, notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        product["source_brand"],
        product["synthetic_brand"],
        product["original_name"],
        product["synthetic_name"],
        product["category"],
        product["subcategory"],
        product["gender"],
        product["season_year"],
        product["msrp"],
        product["current_price"],
        product["sizes"],
        product["colors"],
        product["description"],
        product["features"],
        product["notes"],
    ))

    conn.commit()
    conn.close()


def load_products():
    conn = connect_db()
    df = pd.read_sql_query("""
        SELECT *
        FROM product_families
        ORDER BY id DESC
    """, conn)
    conn.close()
    return df


def split_values(text):
    if text is None or str(text).strip() == "":
        return ["One Size"]
    return [x.strip() for x in str(text).split(",") if x.strip()]


def get_margin_and_price_tier(category, msrp):
    msrp = float(msrp) if msrp else 0.0

    if category in ["Jackets", "Ski Pants", "Gloves", "Base Layers", "Accessories"]:
        gross_margin_pct = random.uniform(0.52, 0.66)
    elif category in ["Skis", "Snowboards", "Boots", "Bindings"]:
        gross_margin_pct = random.uniform(0.35, 0.50)
    elif category in ["Helmets", "Goggles", "Packs", "Poles"]:
        gross_margin_pct = random.uniform(0.45, 0.60)
    else:
        gross_margin_pct = random.uniform(0.40, 0.55)

    if msrp < 75:
        price_tier = "Value"
    elif msrp < 200:
        price_tier = "Mid"
    elif msrp < 500:
        price_tier = "Premium"
    else:
        price_tier = "Elite"

    unit_cost = msrp * (1 - gross_margin_pct)

    return gross_margin_pct, unit_cost, price_tier


def generate_skus():
    conn = connect_db()
    cursor = conn.cursor()

    products = load_products()
    cursor.execute("DELETE FROM skus")

    for _, row in products.iterrows():
        sizes = split_values(row["sizes"])
        colors = split_values(row["colors"])

        for size in sizes:
            for color in colors:
                baseline_price = row["msrp"]

                gross_margin_pct, unit_cost, price_tier = get_margin_and_price_tier(
                    row["category"],
                    baseline_price,
                )

                sku_id = (
                    f"SR-"
                    f"{int(row['id']):05d}-"
                    f"{str(size).upper().replace(' ', '')}-"
                    f"{str(color)[:3].upper().replace(' ', '')}"
                )

                cursor.execute("""
                    INSERT OR REPLACE INTO skus (
                        sku_id, product_family_id, synthetic_name, category,
                        subcategory, gender, size, color, msrp, current_price,
                        baseline_price, gross_margin_pct, unit_cost, price_tier
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    sku_id,
                    int(row["id"]),
                    row["synthetic_name"],
                    row["category"],
                    row["subcategory"],
                    row["gender"],
                    size,
                    color,
                    row["msrp"],
                    row["current_price"],
                    baseline_price,
                    gross_margin_pct,
                    unit_cost,
                    price_tier,
                ))

    conn.commit()
    conn.close()


def load_skus():
    conn = connect_db()
    df = pd.read_sql_query("""
        SELECT *
        FROM skus
        ORDER BY sku_id
    """, conn)
    conn.close()
    return df


def generate_stores():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM stores")

    store_number = 1

    for retailer_name, store_count, retailer_tier, store_type in RETAILERS:
        for _ in range(store_count):
            if retailer_name in ["Backcountry", "Summit Ridge Online"]:
                region, state, city, market_size, snow_score = ("Online", "US", "Online", "National", 85)
                channel = "Online"
                is_online = 1
                store_name = retailer_name
            else:
                region, state, city, market_size, snow_score = random.choice(STORE_MARKETS)
                channel = "Retail"
                is_online = 0
                store_name = f"{retailer_name} - {city}"

            store_id = f"STORE-{store_number:04d}"

            cursor.execute("""
                INSERT INTO stores (
                    store_id, retailer_name, store_name, channel, retailer_tier,
                    store_type, region, state, city, market_size,
                    snow_market_score, is_online, status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                store_id,
                retailer_name,
                store_name,
                channel,
                retailer_tier,
                store_type,
                region,
                state,
                city,
                market_size,
                snow_score,
                is_online,
                "Active",
            ))

            store_number += 1

    conn.commit()
    conn.close()


def load_stores():
    conn = connect_db()
    df = pd.read_sql_query("""
        SELECT *
        FROM stores
        ORDER BY store_id
    """, conn)
    conn.close()
    return df


def get_holiday_flags(week_start):
    flags = {
        "is_holiday_week": 0,
        "holiday_name": "",
        "is_black_friday_week": 0,
        "is_christmas_week": 0,
        "is_presidents_day_week": 0,
        "is_memorial_day_week": 0,
        "is_labor_day_week": 0,
    }

    month = week_start.month
    day = week_start.day

    if month == 12 and 20 <= day <= 31:
        flags["is_holiday_week"] = 1
        flags["holiday_name"] = "Christmas"
        flags["is_christmas_week"] = 1

    if month == 11 and 20 <= day <= 30:
        flags["is_holiday_week"] = 1
        flags["holiday_name"] = "Black Friday"
        flags["is_black_friday_week"] = 1

    if month == 2 and 14 <= day <= 21:
        flags["is_holiday_week"] = 1
        flags["holiday_name"] = "Presidents Day"
        flags["is_presidents_day_week"] = 1

    if month == 5 and 24 <= day <= 31:
        flags["is_holiday_week"] = 1
        flags["holiday_name"] = "Memorial Day"
        flags["is_memorial_day_week"] = 1

    if month == 9 and 1 <= day <= 10:
        flags["is_holiday_week"] = 1
        flags["holiday_name"] = "Labor Day"
        flags["is_labor_day_week"] = 1

    return flags


def generate_calendar():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM calendar_weeks")

    start_date = datetime(2023, 5, 1)
    end_date = datetime(2026, 5, 31)

    current_date = start_date

    while current_date <= end_date:
        week_end = current_date + timedelta(days=6)

        year = current_date.year
        month = current_date.month
        quarter = (month - 1) // 3 + 1
        week_of_year = int(current_date.strftime("%U"))

        if month in [12, 1, 2]:
            season = "Winter"
        elif month in [3, 4, 5]:
            season = "Spring"
        elif month in [6, 7, 8]:
            season = "Summer"
        else:
            season = "Fall"

        if month in [12, 1, 2]:
            retail_season = "Peak Ski Season"
        elif month in [8, 9, 10]:
            retail_season = "Preseason"
        elif month in [3, 4]:
            retail_season = "Spring Clearance"
        else:
            retail_season = "Off Season"

        holiday_flags = get_holiday_flags(current_date)

        cursor.execute("""
            INSERT INTO calendar_weeks (
                week_start_date, week_end_date, year, month, quarter,
                week_of_year, season, retail_season, is_holiday_week,
                holiday_name, is_black_friday_week, is_christmas_week,
                is_presidents_day_week, is_memorial_day_week, is_labor_day_week,
                is_peak_ski_season, is_preseason, is_spring_clearance
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            current_date.strftime("%Y-%m-%d"),
            week_end.strftime("%Y-%m-%d"),
            year,
            month,
            quarter,
            week_of_year,
            season,
            retail_season,
            holiday_flags["is_holiday_week"],
            holiday_flags["holiday_name"],
            holiday_flags["is_black_friday_week"],
            holiday_flags["is_christmas_week"],
            holiday_flags["is_presidents_day_week"],
            holiday_flags["is_memorial_day_week"],
            holiday_flags["is_labor_day_week"],
            1 if retail_season == "Peak Ski Season" else 0,
            1 if retail_season == "Preseason" else 0,
            1 if retail_season == "Spring Clearance" else 0,
        ))

        current_date += timedelta(days=7)

    conn.commit()
    conn.close()


def load_calendar():
    conn = connect_db()
    df = pd.read_sql_query("""
        SELECT *
        FROM calendar_weeks
        ORDER BY week_start_date
    """, conn)
    conn.close()
    return df


st.set_page_config(page_title="Ski Catalog Builder", layout="wide")
create_tables()
migrate_skus_table()

st.title("Ski Catalog Builder")

st.header("Add Product Family")

col1, col2 = st.columns(2)

with col1:
    source_brand = st.text_input("Source Brand", "Black Diamond")
    synthetic_brand = st.text_input("Synthetic Brand", "Summit Ridge")
    original_name = st.text_input("Original Product Name")
    synthetic_name = st.text_input("Synthetic Product Name")

    category = st.selectbox("Category", list(CATEGORIES.keys()))
    subcategory = st.selectbox("Subcategory", CATEGORIES[category])

with col2:
    gender = st.selectbox("Gender Segment", ["Unisex", "Men's", "Women's", "Youth"])
    season_year = st.number_input("Season Year", min_value=2020, max_value=2035, value=2026)
    msrp = st.number_input("MSRP", min_value=0.0, step=10.0)
    current_price = st.number_input("Current Price", min_value=0.0, step=10.0)
    sizes = st.text_input("Sizes / Lengths", "S, M, L, XL")
    colors = st.text_input("Colors", "Black")

description = st.text_area("Description")
features = st.text_area("Features")
notes = st.text_area("Notes")

if st.button("Save Product Family"):
    product = {
        "source_brand": source_brand,
        "synthetic_brand": synthetic_brand,
        "original_name": original_name,
        "synthetic_name": synthetic_name,
        "category": category,
        "subcategory": subcategory,
        "gender": gender,
        "season_year": season_year,
        "msrp": msrp,
        "current_price": current_price,
        "sizes": sizes,
        "colors": colors,
        "description": description,
        "features": features,
        "notes": notes,
    }

    save_product(product)
    st.success(f"Saved: {synthetic_name}")

st.divider()

st.header("Current Product Families")

products_df = load_products()

if not products_df.empty:
    st.dataframe(products_df, use_container_width=True)
else:
    st.info("No products saved yet.")

st.divider()

st.header("Generate SKU Table")

if st.button("Generate SKUs"):
    generate_skus()
    st.success("SKU table generated.")

skus_df = load_skus()

if not skus_df.empty:
    st.metric("Total SKUs", len(skus_df))
    st.dataframe(skus_df, use_container_width=True)
else:
    st.info("No SKUs generated yet.")

st.divider()

st.header("Generate Store Table")

if st.button("Generate Stores"):
    generate_stores()
    st.success("Store table generated.")

stores_df = load_stores()

if not stores_df.empty:
    st.metric("Total Stores", len(stores_df))

    st.subheader("Stores")
    st.dataframe(stores_df, use_container_width=True)

    st.subheader("Store Count by Retailer")
    retailer_summary = stores_df.groupby("retailer_name").size().reset_index(name="store_count")
    st.dataframe(retailer_summary, use_container_width=True)

    st.subheader("Store Count by Region")
    region_summary = stores_df.groupby("region").size().reset_index(name="store_count")
    st.dataframe(region_summary, use_container_width=True)
else:
    st.info("No stores generated yet.")

st.divider()

st.header("Generate Calendar Table")

if st.button("Generate Calendar"):
    generate_calendar()
    st.success("Calendar table generated.")

calendar_df = load_calendar()

if not calendar_df.empty:
    st.metric("Total Weeks", len(calendar_df))

    st.subheader("Calendar Weeks")
    st.dataframe(calendar_df, use_container_width=True)

    st.subheader("Holiday Weeks")
    holiday_df = calendar_df[calendar_df["is_holiday_week"] == 1]
    st.dataframe(holiday_df, use_container_width=True)
else:
    st.info("No calendar generated yet.")

def get_category_season_multiplier(category, retail_season):
    if category in ["Skis", "Snowboards", "Boots", "Bindings"]:
        if retail_season == "Peak Ski Season":
            return 4.0
        elif retail_season == "Preseason":
            return 2.2
        elif retail_season == "Spring Clearance":
            return 1.3
        else:
            return 0.25

    if category in ["Jackets", "Ski Pants", "Gloves", "Base Layers"]:
        if retail_season == "Peak Ski Season":
            return 3.0
        elif retail_season == "Preseason":
            return 2.0
        elif retail_season == "Spring Clearance":
            return 1.5
        else:
            return 0.45

    if category in ["Helmets", "Goggles", "Poles", "Packs"]:
        if retail_season == "Peak Ski Season":
            return 2.5
        elif retail_season == "Preseason":
            return 1.8
        elif retail_season == "Spring Clearance":
            return 1.2
        else:
            return 0.4

    if category == "Accessories":
        if retail_season == "Peak Ski Season":
            return 1.8
        elif retail_season == "Preseason":
            return 1.4
        elif retail_season == "Spring Clearance":
            return 1.1
        else:
            return 0.8

    return 1.0


def get_base_velocity(category, price_tier):
    base = {
        "Accessories": 2.2,
        "Gloves": 1.6,
        "Base Layers": 1.4,
        "Helmets": 1.1,
        "Goggles": 1.1,
        "Jackets": 0.9,
        "Ski Pants": 0.8,
        "Poles": 0.8,
        "Packs": 0.7,
        "Boots": 0.5,
        "Skis": 0.45,
        "Snowboards": 0.4,
    }.get(category, 0.8)

    tier_factor = {
        "Value": 1.4,
        "Mid": 1.15,
        "Premium": 0.85,
        "Elite": 0.55,
    }.get(price_tier, 1.0)

    return base * tier_factor


def get_discount(calendar_row):
    discount_pct = 0.0
    promo_flag = 0
    markdown_flag = 0

    if calendar_row["is_black_friday_week"] == 1:
        discount_pct = random.uniform(0.15, 0.35)
        promo_flag = 1

    elif calendar_row["is_christmas_week"] == 1:
        discount_pct = random.uniform(0.05, 0.20)
        promo_flag = 1

    elif calendar_row["is_spring_clearance"] == 1:
        discount_pct = random.uniform(0.20, 0.45)
        promo_flag = 1
        markdown_flag = 1

    elif random.random() < 0.08:
        discount_pct = random.uniform(0.05, 0.18)
        promo_flag = 1

    return discount_pct, promo_flag, markdown_flag

def generate_weekly_sales(target_rows=1000000):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM fact_weekly_sales")

    skus = load_skus()
    stores = load_stores()
    calendar = load_calendar()

    if skus.empty or stores.empty or calendar.empty:
        conn.close()
        return 0

    sku_records = skus.to_dict("records")
    store_records = stores.to_dict("records")
    calendar_records = calendar.to_dict("records")

    total_weeks = len(calendar_records)
    rows_per_week = max(1, target_rows // total_weeks)

    rows_inserted = 0
    insert_rows = []

    for week in calendar_records:
        weekly_rows_inserted = 0
        attempts = 0
        max_attempts = rows_per_week * 30

        while weekly_rows_inserted < rows_per_week and attempts < max_attempts:
            attempts += 1

            store = random.choice(store_records)
            sku = random.choice(sku_records)

            category = sku["category"]
            price_tier = sku["price_tier"]

            season_multiplier = get_category_season_multiplier(category, week["retail_season"])
            snow_factor = store["snow_market_score"] / 75

            if store["is_online"] == 1:
                store_factor = 2.25
            elif store["retailer_tier"] == "Specialty Retail":
                store_factor = 1.20
            elif store["retailer_tier"] == "Small Retail":
                store_factor = 0.75
            else:
                store_factor = 1.0

            base_velocity = get_base_velocity(category, price_tier)
            expected_units = base_velocity * season_multiplier * snow_factor * store_factor

            if week["is_black_friday_week"] == 1:
                expected_units *= random.uniform(1.6, 2.8)

            if week["is_christmas_week"] == 1 and category in ["Accessories", "Gloves", "Base Layers", "Jackets"]:
                expected_units *= random.uniform(1.3, 2.0)

            expected_units *= random.uniform(0.15, 2.00)
            units_sold = int(round(expected_units))

            if units_sold <= 0:
                continue

            baseline_price = float(sku["baseline_price"] or sku["msrp"] or 0)
            unit_cost = float(sku["unit_cost"] or 0)

            discount_pct, promo_flag, markdown_flag = get_discount(week)

            selling_price = baseline_price * (1 - discount_pct)
            gross_sales = baseline_price * units_sold
            net_sales = selling_price * units_sold
            cogs = unit_cost * units_sold
            gross_profit = net_sales - cogs

            units_returned = 0
            if random.random() < 0.025:
                units_returned = random.randint(1, max(1, min(units_sold, 2)))

            inventory_on_hand = random.randint(0, 40)
            stockout_flag = 1 if inventory_on_hand <= 2 and units_sold >= 3 else 0

            insert_rows.append((
                week["week_start_date"],
                store["store_id"],
                sku["sku_id"],
                units_sold,
                baseline_price,
                discount_pct,
                selling_price,
                gross_sales,
                net_sales,
                unit_cost,
                cogs,
                gross_profit,
                inventory_on_hand,
                units_returned,
                promo_flag,
                markdown_flag,
                stockout_flag,
            ))

            rows_inserted += 1
            weekly_rows_inserted += 1

            if len(insert_rows) >= 10000:
                cursor.executemany("""
                    INSERT INTO fact_weekly_sales (
                        week_start_date, store_id, sku_id, units_sold,
                        baseline_price, discount_pct, selling_price,
                        gross_sales, net_sales, unit_cost, cogs,
                        gross_profit, inventory_on_hand, units_returned,
                        promo_flag, markdown_flag, stockout_flag
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, insert_rows)

                conn.commit()
                insert_rows = []

    if insert_rows:
        cursor.executemany("""
            INSERT INTO fact_weekly_sales (
                week_start_date, store_id, sku_id, units_sold,
                baseline_price, discount_pct, selling_price,
                gross_sales, net_sales, unit_cost, cogs,
                gross_profit, inventory_on_hand, units_returned,
                promo_flag, markdown_flag, stockout_flag
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, insert_rows)

    conn.commit()
    conn.close()

    return rows_inserted

def load_weekly_sales_sample():
    conn = connect_db()
    df = pd.read_sql_query("""
        SELECT *
        FROM fact_weekly_sales
        LIMIT 1000
    """, conn)
    conn.close()
    return df


def load_weekly_sales_summary():
    conn = connect_db()

    summary = pd.read_sql_query("""
        SELECT
            COUNT(*) AS row_count,
            SUM(units_sold) AS total_units,
            SUM(net_sales) AS total_net_sales,
            SUM(gross_profit) AS total_gross_profit
        FROM fact_weekly_sales
    """, conn)

    by_year = pd.read_sql_query("""
        SELECT
            cw.year,
            SUM(f.units_sold) AS total_units,
            SUM(f.net_sales) AS total_net_sales,
            SUM(f.gross_profit) AS total_gross_profit
        FROM fact_weekly_sales f
        JOIN calendar_weeks cw
            ON f.week_start_date = cw.week_start_date
        GROUP BY cw.year
        ORDER BY cw.year
    """, conn)

    by_category = pd.read_sql_query("""
        SELECT
            s.category,
            SUM(f.units_sold) AS total_units,
            SUM(f.net_sales) AS total_net_sales,
            SUM(f.gross_profit) AS total_gross_profit
        FROM fact_weekly_sales f
        JOIN skus s
            ON f.sku_id = s.sku_id
        GROUP BY s.category
        ORDER BY total_net_sales DESC
    """, conn)

    conn.close()
    return summary, by_year, by_category

def export_tables_to_csv():
    export_folder = "exports"
    os.makedirs(export_folder, exist_ok=True)

    conn = connect_db()

    tables = [
        "skus",
        "stores",
        "calendar_weeks",
        "fact_weekly_sales"
    ]

    exported_files = []

    for table in tables:
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        output_path = os.path.join(export_folder, f"{table}.csv")
        df.to_csv(output_path, index=False)
        exported_files.append(output_path)

    conn.close()
    return exported_files

st.divider()

st.header("Generate Weekly Sales Fact Table")

max_sales_rows = st.number_input(
    "Maximum sales rows to generate",
    min_value=10000,
    max_value=5000000,
    value=1000000,
    step=100000
)

if st.button("Generate Weekly Sales"):
    rows_created = generate_weekly_sales(target_rows=int(max_sales_rows))
    st.success(f"Weekly sales fact table generated with {rows_created:,} rows.")

sales_summary, sales_by_year, sales_by_category = load_weekly_sales_summary()
sales_sample_df = load_weekly_sales_sample()

if not sales_summary.empty and sales_summary["row_count"].iloc[0] > 0:
    st.metric("Fact Sales Rows", f"{int(sales_summary['row_count'].iloc[0]):,}")
    st.metric("Total Units Sold", f"{int(sales_summary['total_units'].iloc[0]):,}")
    st.metric("Total Net Sales", f"${sales_summary['total_net_sales'].iloc[0]:,.0f}")
    st.metric("Total Gross Profit", f"${sales_summary['total_gross_profit'].iloc[0]:,.0f}")

    st.subheader("Sales by Year")
    st.dataframe(sales_by_year, use_container_width=True)

    st.subheader("Sales by Category")
    st.dataframe(sales_by_category, use_container_width=True)

    st.subheader("Sales Sample")
    st.dataframe(sales_sample_df, use_container_width=True)
else:
    st.info("No weekly sales generated yet.")

st.divider()

st.header("Export Tables to CSV")

if st.button("Export CSV Files"):
    exported_files = export_tables_to_csv()

    st.success("CSV export completed.")

    st.subheader("Exported Files")
    for file in exported_files:
        st.write(file)