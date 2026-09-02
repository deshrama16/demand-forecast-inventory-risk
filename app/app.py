import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Demand & Inventory Risk System",
    page_icon="📦",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1rem;
        color: #666666;
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 650;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

risk_output = pd.read_csv("data/risk_output.csv")
store_summary = pd.read_csv("data/store_summary.csv")
risk_summary = pd.read_csv("data/risk_summary.csv")
top_replenishment = pd.read_csv("data/top_replenishment.csv")

# Convert date
risk_output["WeekStart"] = pd.to_datetime(
    risk_output["WeekStart"]
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Control Tower")

st.sidebar.markdown(
    """
    ### Navigation

    **Overview**
    
    **Store Risk Profile**
    
    **Risk Control Center**
    """
)

st.sidebar.divider()

st.sidebar.markdown("### Model")

st.sidebar.info(
    """
    **Model:** Random Forest Regressor
    
    **Forecast horizon:** 1 week
    
    **Validation WAPE:** 8.39%
    
    **Validation R²:** 0.905
    """
)

st.sidebar.divider()

st.sidebar.markdown("### Data")

st.sidebar.caption(
    "Public retail sales dataset used as an "
    "Amazon-inspired demand forecasting scenario."
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">📦 Demand Forecast & Inventory Risk Control Tower</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Predict demand • Detect inventory risk • Prioritize replenishment'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    **Predict demand • Detect inventory risk • Prioritize replenishment**
    
    An ML-powered decision-support prototype for demand and inventory planning.
    """
)

st.divider()

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_forecast = risk_output["Forecast_Demand"].sum()

total_replenishment = (
    risk_output["Recommended_Replenishment"].sum()
)

high_risk_count = (
    risk_output["Risk_Level"] == "HIGH"
).sum()

medium_risk_count = (
    risk_output["Risk_Level"] == "MEDIUM"
).sum()

low_risk_count = (
    risk_output["Risk_Level"] == "LOW"
).sum()

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Forecast Demand",
        f"{total_forecast:,.0f}"
    )

with col2:
    st.metric(
        "Recommended Replenishment",
        f"{total_replenishment:,.0f}"
    )

with col3:
    st.metric(
        "🔴 High-Risk Store-Weeks",
        f"{high_risk_count:,}"
    )

with col4:
    st.metric(
        "🟢 Low-Risk Store-Weeks",
        f"{low_risk_count:,}"
    )

st.divider()

# --------------------------------------------------
# RISK SUMMARY
# --------------------------------------------------

st.subheader("Risk Overview")

risk_display = risk_summary.copy()

st.dataframe(
    risk_display,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# STORE RISK PROFILE
# --------------------------------------------------

st.divider()

st.subheader("🔎 Store Risk Profile")

store_list = sorted(
    risk_output["Store"].unique()
)

selected_store = st.selectbox(
    "Select a store",
    store_list
)

selected_data = (
    risk_output[
        risk_output["Store"] == selected_store
    ]
    .sort_values("WeekStart")
)

latest = selected_data.iloc[-1]

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Forecast Demand",
        f"{latest['Forecast_Demand']:,.0f}"
    )

with col2:
    st.metric(
        "Simulated Inventory",
        f"{latest['Simulated_Inventory']:,.0f}"
    )

with col3:
    st.metric(
        "Inventory Coverage",
        f"{latest['Inventory_Coverage_Ratio']:.1%}"
    )

with col4:
    st.metric(
        "Risk Level",
        latest["Risk_Level"]
    )

with col5:
    st.metric(
        "Replenishment",
        f"{latest['Recommended_Replenishment']:,.0f}"
    )

st.markdown("### Recommended Action")

if latest["Risk_Level"] == "HIGH":
    st.error(
        f"🚨 EXPEDITE REPLENISHMENT — "
        f"Recommended quantity: "
        f"{latest['Recommended_Replenishment']:,.0f} units"
    )

elif latest["Risk_Level"] == "MEDIUM":
    st.warning(
        f"⚠️ MONITOR INVENTORY — "
        f"Recommended replenishment: "
        f"{latest['Recommended_Replenishment']:,.0f} units"
    )

else:
    st.success(
        "✅ NO IMMEDIATE ACTION REQUIRED"
    )

st.markdown("### Store Forecast & Risk History")

chart_data = selected_data[
    [
        "WeekStart",
        "Forecast_Demand",
        "Simulated_Inventory"
    ]
].set_index("WeekStart")

st.line_chart(
    chart_data,
    use_container_width=True
)

st.markdown("### Detailed Store History")

display_columns = [
    "WeekStart",
    "Forecast_Demand",
    "Simulated_Inventory",
    "Inventory_Coverage_Ratio",
    "Volatility_Ratio",
    "Combined_Risk_Score",
    "Risk_Level",
    "Recommended_Replenishment",
    "Recommendation"
]

st.dataframe(
    selected_data[display_columns],
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# HIGH-RISK CONTROL CENTER
# --------------------------------------------------

st.divider()

st.subheader("🚨 Inventory Risk Control Center")

st.markdown(
    "Prioritize stores requiring inventory intervention."
)

risk_filter = st.selectbox(
    "Filter by risk level",
    ["HIGH", "MEDIUM", "LOW", "ALL"]
)

if risk_filter == "ALL":
    filtered_risk = risk_output.copy()
else:
    filtered_risk = risk_output[
        risk_output["Risk_Level"] == risk_filter
    ].copy()

control_col1, control_col2, control_col3 = st.columns(3)

with control_col1:
    st.metric(
        "Stores / Observations",
        f"{len(filtered_risk):,}"
    )

with control_col2:
    st.metric(
        "Total Replenishment",
        f"{filtered_risk['Recommended_Replenishment'].sum():,.0f}"
    )

with control_col3:
    avg_coverage = filtered_risk[
        "Inventory_Coverage_Ratio"
    ].mean()

    st.metric(
        "Average Inventory Coverage",
        f"{avg_coverage:.1%}"
    )

control_table = (
    filtered_risk
    .sort_values(
        "Combined_Risk_Score",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    control_table[
        [
            "Store",
            "WeekStart",
            "Forecast_Demand",
            "Simulated_Inventory",
            "Inventory_Coverage_Ratio",
            "Volatility_Ratio",
            "Combined_Risk_Score",
            "Risk_Level",
            "Recommended_Replenishment",
            "Recommendation"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.markdown("### Risk Distribution")

risk_chart = (
    filtered_risk["Risk_Level"]
    .value_counts()
    .rename_axis("Risk_Level")
    .reset_index(name="Count")
)

st.bar_chart(
    risk_chart.set_index("Risk_Level")
)

# --------------------------------------------------
# METHODOLOGY
# --------------------------------------------------

st.divider()

st.subheader("📊 Methodology")

with st.expander("How does this system work?"):

    st.markdown(
        """
        ### 1. Demand Forecasting

        Historical weekly store sales are transformed into
        lag, rolling-demand and seasonality features.

        ### 2. Machine Learning

        Multiple models were evaluated:

        - Naive baseline
        - Random Forest
        - CatBoost

        Random Forest was selected because it achieved the
        lowest WAPE of **8.39%** on the time-based validation set.

        ### 3. Inventory Risk

        Forecast demand is combined with demand variability
        to estimate safety stock requirements.

        ### 4. Risk Scoring

        Inventory coverage and demand volatility are combined
        into an operational risk score.

        ### 5. Replenishment

        The system recommends replenishment when simulated
        inventory falls below the required inventory level.
        """
    )

st.subheader("⚠️ Key Assumptions")

with st.expander("View assumptions"):

    st.markdown(
        """
        - The public dataset does not contain actual inventory-on-hand data.
        - Current inventory is therefore simulated using **0.8 weeks of
          recent average demand**.
        - Safety stock uses a prototype 95% service-level assumption.
        - Risk thresholds are analytical assumptions created for this
          demonstration and do not represent Amazon's internal policies.
        - The project is an **Amazon-inspired case study using public data**,
          not an analysis of Amazon's internal systems or data.
        """
    )
st.divider()

st.caption(
    "Amazon-inspired Demand Forecasting & Inventory Risk "
    "Decision Support Prototype | Built with Python, "
    "Pandas, Scikit-learn, CatBoost & Streamlit"
)