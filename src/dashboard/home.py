import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Supply Chain ML", page_icon="chart_with_upwards_trend", layout="wide")

st.title("Supply Chain Intelligence Dashboard")

try:
    sales_df = pd.read_csv("data/raw/train.csv")
    sales_df['date'] = pd.to_datetime(sales_df['date'])

    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Forecasting", "Risk", "Inventory"])

    with tab1:
        st.header("Overview")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Sales", f"{sales_df['sales'].sum():,}")
        col2.metric("Avg Daily", f"{sales_df['sales'].mean():.1f}")
        col3.metric("Stores", sales_df['store'].nunique())
        col4.metric("Products", sales_df['item'].nunique())

        daily = sales_df.groupby('date')['sales'].sum().reset_index()
        st.plotly_chart(px.line(daily, x="date", y="sales"), use_container_width=True)

    with tab2:
        st.header("Forecasting - XGBoost MAPE: 12.08%")
        store = st.selectbox("Store", sales_df['store'].unique())
        item = st.selectbox("Product", sales_df['item'].unique())
        data = sales_df[(sales_df['store']==store) & (sales_df['item']==item)]
        if not data.empty:
            st.plotly_chart(px.line(data, x="date", y="sales"), use_container_width=True)

    with tab3:
        st.header("Risk Assessment")
        risk_df = pd.read_csv("data/raw/suppliers.csv")
        st.metric("Suppliers", len(risk_df))
        st.metric("Avg Risk", f"{risk_df['overall_risk_score'].mean():.1f}")
        st.plotly_chart(px.pie(risk_df, names="risk_level"), use_container_width=True)

    with tab4:
        st.header("Inventory Optimization")
        inv_df = pd.read_csv("data/processed/inventory_optimization.csv")
        st.metric("Avg EOQ", f"{inv_df['eoq'].mean():.0f}")
        st.metric("Total Cost", f"${inv_df['total_inventory_cost'].sum():,.0f}")
        st.dataframe(inv_df, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")
st.caption("Supply Chain ML - MTech Thesis")