# Mountainland Ski Retail Analytics Warehouse

> A synthetic retail analytics ecosystem built with Python, Streamlit, SQLite, SQL, and BigQuery-inspired cloud data concepts. The dataset is designed to simulate a realistic blend of retail sales and syndicated market data, giving students exposure to the types of analytical environments they are likely to encounter in industry.

Most students begin by learning foundational tools and techniques in analytics, databases, programming, and visualization. But when they enter the workforce, they are suddenly confronted with massive datasets, cloud platforms, complex business logic, and entirely new domains to understand. This project is designed to help bridge that gap.

At Mountainland Technical College, students spend nine months learning modern data technologies before completing a capstone project that integrates the full range of skills taught in the program. Projects like this one are intended to simulate real-world analytical ecosystems and provide hands-on experience with the workflows, tools, and problem-solving approaches that are critical for success in data and analytics careers.

Created for:
- Mountainland Technical College students
- analytics and BI learners
- retail data enthusiasts
- portfolio and warehouse engineering demonstrations

---

## 🏔️ Project Overview

This project simulates a premium outdoor/ski retail company called **Mountainland Ski Company**.

The system generates a realistic retail analytics warehouse including:

- product master data
- SKU-level assortment
- retailer/store networks
- weekly calendar dimensions
- synthetic sell-through market data
- promotions and seasonality
- profitability and pricing logic

The project was designed to teach:
- dimensional modeling
- retail analytics
- synthetic data engineering
- SQL
- business intelligence
- cloud warehouse concepts

while still feeling like a real-world enterprise dataset.

---

# 🌐 Fake Brand Website

The synthetic brand website for Mountainland Ski Company:

👉 https://mountainlandskico.github.io/retail/

Built by Darin Lewis, Instructor, Mountainland Technical College.

---

# 🧊 Warehouse Structure

The system generates a retail warehouse consisting of:

## Dimension Tables

### `product_families`
Master product catalog.

### `skus`
Generated SKU-level assortment:
- sizes
- colors
- pricing
- margins
- unit cost
- price tiers

### `stores`
Retail network including:
- REI
- Dick's Sporting Goods
- Scheels
- Evo (*Where I buy all my ski stuff and the source from where most product names and descriptions were copied.)
- independent mountain shops
- DTC online channels

### `calendar_weeks`
Weekly calendar dimension:
- holidays
- Black Friday
- Christmas
- preseason
- peak ski season
- spring clearance

---

## 📊 Fact Table

### `fact_weekly_sales`

Synthetic weekly sell-through market data including:
- units sold
- sales dollars
- promotions
- markdowns
- profitability
- inventory
- returns
- geographic demand patterns

The generated dataset behaves similarly to:
- syndicated market data
- modeled retailer sell-through
- outdoor retail analytics feeds

---

# 🛠️ Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- SQL
- DBeaver
- BigQuery concepts
- Retail dimensional modeling

---

# 🎯 Why This Project Exists

Most analytics students only ever interact with finished datasets.

This project demonstrates:
- how datasets are designed
- how warehouse schemas are created
- how synthetic data is generated
- how business logic shapes analytics

Students can:
- inspect the schema
- generate their own data
- modify assumptions
- run SQL queries
- build dashboards
- experiment with BI and forecasting

---

# ❄️ Realism Features

The generator includes:

## Geographic Demand Logic
Colorado, Utah, California, and mountain regions naturally over-index in snow sports sales.

## Seasonal Demand
- peak ski season
- preseason inventory build
- spring clearance
- holiday promotions

## Retail Channel Behavior
Different retailer types behave differently:
- specialty retail
- large retail
- DTC ecommerce
- independent shops

## Profitability Modeling
SKU-level:
- MSRP
- selling price
- unit cost
- gross profit
- markdown behavior

## Sparse Sales Generation
The fact table intentionally behaves like real retail:
- hero SKUs
- long-tail assortment
- seasonal spikes
- uneven demand

---

# 📦 Example Scale

Typical generated warehouse:

| Table | Approximate Size |
|---|---:|
| Product Families | 100–200 |
| SKUs | 2,000–5,000 |
| Stores | 200+ |
| Calendar Weeks | 150+ |
| Fact Sales Rows | 100k–1M+ |

---

# 🚀 Running the Project

This project was developed primarily in **PyCharm** using Python and Streamlit.
https://streamlit.io/
---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <your_repo_url>
```

---

## 2. Open in PyCharm

Open the project folder in PyCharm.

Recommended:
- Python 3.11+
- virtual environment enabled

---

## 3. Install Requirements

Open the terminal in PyCharm:

```bash
py -m pip install -r requirements.txt
```

---

## 4. Run Streamlit

In terminal:

```bash
py -m streamlit run catalog_builder.py
```

---

## 5. Open the App

Streamlit will automatically launch in your browser:

```text
http://localhost:8501
```

---

# 🧠 Typical Workflow

## 1. Add Product Families
Create products manually through the Streamlit UI. 

(I did this for ~144 product families; adding colors and sizes got me to generate over 4200 skus.)

## 2. Generate SKUs
Creates realistic size/color assortment.

## 3. Generate Stores
Builds a retailer network across the United States.

## 4. Generate Calendar
Creates a weekly retail calendar with seasonality and holidays.

## 5. Generate Weekly Sales
Builds synthetic retail market data.

## 6. Analyze in SQL / BI
Use:
- DBeaver
- SQLite
- Power BI
- Tableau
- BigQuery

---

# 🎓 Educational Goals

This project supports instruction in:

- SQL
- dimensional modeling
- star schemas
- business intelligence
- synthetic data generation
- forecasting
- retail analytics
- warehouse engineering
- Python for analytics

---

# 🔮 Future Ideas

Potential future enhancements:
- demand forecasting
- ML models
- inventory planning
- assortment optimization
- BigQuery warehouse loading
- Power BI dashboards
- Tableau analytics
- Snowflake implementation
- AI-driven demand simulation

---

# 👨‍💻 Author

Created by:

**Jacob Jarrard**  
Mountainland Technical College  
Data Technologies Program Lead
Category Insights / Analytics Engineering

Additional collaboration:

**Darin Lewis**

Mountainland Technical College
Evening Instructor
Big Data / AI 

---

# ⚠️ Disclaimer

This project uses entirely synthetic data and a fictional company.

Any resemblance to real companies, products, retailers, or datasets is coincidental and used strictly for educational purposes.
