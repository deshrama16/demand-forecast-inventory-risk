# Demand Forecasting & Inventory Risk Control Tower

ML-powered demand forecasting and inventory risk control tower for store-level replenishment decisions using time-based validation and Streamlit

An end-to-end machine learning and decision-support system for **weekly retail demand forecasting, inventory risk detection, and replenishment prioritization**.

The project uses the public **Rossmann Store Sales** dataset to simulate an Amazon-inspired retail operations scenario. Historical store-level sales are transformed into weekly demand signals, machine learning models forecast next-week demand, and the forecasts are translated into inventory coverage, risk scores, and replenishment recommendations through an interactive Streamlit dashboard.

> **Note:** This is an Amazon-inspired public-data case study and does not use Amazon internal data, systems, inventory policies, or proprietary information.

---

## Business Problem

Retail businesses need to answer two connected questions:

1. **How much demand should we expect next week?**
2. **Which stores are most likely to face inventory risk and require replenishment?**

Accurate demand forecasting alone does not directly tell an operations team where to intervene.

This project therefore extends forecasting into a **decision-support pipeline**:

**Historical Sales → Demand Forecast → Inventory Risk → Replenishment Recommendation**

The goal is to demonstrate how machine learning predictions can be converted into actionable operational decisions.

---

## Project Overview

The system performs five major tasks:

* Analyzes historical store-level sales and customer behavior
* Builds weekly demand forecasting features using lagged sales, rolling statistics, and calendar information
* Compares a naïve forecasting baseline with Random Forest and CatBoost
* Converts demand forecasts into simulated inventory risk metrics
* Provides a Streamlit control tower for identifying high-risk store-weeks and prioritizing replenishment

---

## Methodology

### 1. Data Preparation

The Rossmann dataset contains daily sales information across multiple stores along with store characteristics.

The data was:

* Merged with store-level attributes
* Converted into a proper time series
* Filtered to focus on operating stores
* Enriched with calendar features
* Aggregated from daily to weekly store-level demand

Key variables include:

* Sales
* Customers
* Promotions
* Store Type
* Assortment
* Competition Distance
* Promo2

---

### 2. Exploratory Data Analysis

The analysis investigates:

* Overall sales trends
* Monthly demand patterns
* Promotion and sales relationships
* Customer traffic vs. sales
* Store-level performance
* Store-to-store demand variability
* Store Type differences
* Weekly demand behavior

One key finding was the strong relationship between customer traffic and sales, highlighting the importance of demand intensity when analyzing store performance.

---

### 3. Demand Forecasting

The forecasting problem is formulated as:

> **Predict next week's store-level sales using information available up to the current week.**

Features include:

* 1-week lagged sales
* 2-week lagged sales
* 4-week lagged sales
* 4-week rolling mean
* 4-week rolling standard deviation
* Month
* Quarter
* Week of year
* Store Type
* Assortment
* Competition Distance
* Promo2

Rolling features are calculated using only historical observations to avoid future information leakage.

---

## Models

Three approaches were evaluated:

### Naïve Baseline

The baseline assumes:

> **Next week's sales = current week's sales**

This establishes a simple benchmark against which the machine learning models are evaluated.

### Random Forest

A Random Forest Regressor was trained using lagged demand, rolling statistics, seasonality, and store characteristics.

### CatBoost

CatBoost was evaluated as an alternative tree-based model capable of handling categorical store attributes directly.

---

## Model Performance

Models were evaluated using a **time-based validation split**, with the most recent three months reserved for validation.

| Model          |    WAPE ↓ |      R² ↑ |
| -------------- | --------: | --------: |
| Naïve Baseline |    26.90% |     0.394 |
| Random Forest  | **8.39%** |     0.905 |
| CatBoost       |     8.68% | **0.911** |

Random Forest achieved the lowest WAPE and was therefore selected for the downstream inventory risk system.

Compared with the naïve baseline, Random Forest reduced WAPE from **26.90% to 8.39%**, representing approximately a **68.8% reduction in forecast error**.

> WAPE was prioritized because the downstream application is focused on demand planning and inventory decisions, where aggregate forecast error is particularly relevant.

---

## Inventory Risk Engine

Forecasting demand is only the first step.

The project converts predicted demand into operational risk indicators including:

* Forecast demand
* Simulated inventory
* Inventory coverage ratio
* Demand volatility
* Combined risk score
* Risk level
* Estimated replenishment requirement

Stores are categorized into:

* 🔴 **HIGH** — immediate replenishment attention
* 🟠 **MEDIUM** — monitor inventory position
* 🟢 **LOW** — no immediate intervention required

The resulting system allows the user to move from:

**"What will demand be?"**

to:

**"Where should inventory intervention happen first?"**

---

## Streamlit Control Tower

The project includes an interactive Streamlit dashboard with three main views:

### Overview

Provides a high-level view of:

* Forecast demand
* Estimated replenishment requirement
* High-risk store-weeks
* Low-risk store-weeks
* Overall risk distribution

### Store Risk Profile

Allows users to select an individual store and examine:

* Forecast demand
* Simulated inventory
* Inventory coverage
* Risk level
* Replenishment requirement
* Historical risk trends

### Risk Control Center

Provides an operational view of the highest-risk store-weeks and allows users to filter stores by risk level.

The control center is designed to answer:

> **Which stores require attention, and how much replenishment may be required?**

---

## Dashboard Screenshots

### Overview

![Dashboard Overview](screenshots/overview.png)

### Store Risk Profile

![Store Risk Profile](screenshots/store_risk_profile.png)

### Risk Control Center

![Risk Control Center](screenshots/risk_control_center.png)

---

## ⚠️ Important Assumptions & Limitations

The public Rossmann dataset does **not contain actual inventory-on-hand data**.

Therefore, the inventory and replenishment components are a **prototype decision-support layer** built on analytical assumptions.

Key assumptions include:

* Current inventory is simulated using recent demand
* Safety stock uses a prototype 95% service-level assumption
* Risk thresholds are analytical assumptions
* Replenishment quantities are estimated rather than actual purchase orders
* The system does not model supplier lead times, warehouse capacity, or transportation constraints

These assumptions are intentionally stated because the project demonstrates how a forecasting model can be extended into an inventory-risk framework without claiming access to real operational inventory data.

---

## Tech Stack

**Programming & Data**

* Python
* Pandas
* NumPy

**Visualization**

* Matplotlib
* Seaborn

**Machine Learning**

* Scikit-learn
* CatBoost

**Application**

* Streamlit

**Development**

* Jupyter Notebook
* GitHub

---

## Repository Structure

```text
├── notebook/
│   └── demand_forecasting_inventory_risk.ipynb
│
├── app/
│   └── app.py
│
├── screenshots/
│   ├── overview.png
│   ├── store_risk_profile.png
│   └── risk_control_center.png
│
├── data/
│   ├── train.csv
│   ├── store.csv
│   ├── weekly_sales.csv
│   ├── risk_output.csv
│   ├── risk_summary.csv
│   └── store_summary.csv
│
├── requirements.txt
└── README.md
```

---

## How to Run

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd amazon-demand-inventory-control-tower
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit application

```bash
streamlit run app/app.py
```

The application will open in your browser.

---

## Key Takeaways

This project demonstrates an end-to-end data science workflow:

**Business Problem → Data Preparation → EDA → Feature Engineering → Time-Based Validation → ML Forecasting → Error Analysis → Risk Modeling → Replenishment Decisions → Interactive Dashboard**

The key outcome is not simply the forecasting model, but the transformation of model predictions into a **store-level operational decision-support system**.

---

## Dataset

The project uses the publicly available **Rossmann Store Sales** dataset.

The dataset contains historical daily sales and store-level information used for demand forecasting and retail analysis.

---

## Author

**Rama Deshpande**

BTech Student, IIT Guwahati

Interested in Data Science, Machine Learning, and applying analytics to real-world operational problems.

