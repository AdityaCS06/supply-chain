import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Supply Chain Intelligence",
    page_icon="factory",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<link rel="stylesheet" href="https://unpkg.com/lucide-static@latest/font/lucide.css">
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f0f2f6;
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1a73e8 !important;
        color: white !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .stitched-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    .gradient-header {
        background: linear-gradient(135deg, #1a73e8 0%, #7c4dff 100%);
        padding: 20px 30px;
        border-radius: 0 0 20px 20px;
        margin-bottom: 30px;
    }
    .sidebar-nav {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        padding: 20px;
        border-radius: 0 16px 16px 0;
    }
    h1, h2, h3 {
        color: #1a1a2e;
    }
    .highlight {
        color: #1a73e8;
    }
    .footer {
        text-align: center;
        padding: 20px;
        color: #888;
        font-size: 12px;
    }
    .chart-container {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    .icon-wrapper {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    sales_df = pd.read_csv("data/raw/train.csv")
    sales_df['date'] = pd.to_datetime(sales_df['date'])
    try:
        risk_df = pd.read_csv("data/raw/suppliers.csv")
    except:
        risk_df = pd.DataFrame()
    try:
        inv_df = pd.read_csv("data/processed/inventory_optimization.csv")
    except:
        inv_df = pd.DataFrame()
    return sales_df, risk_df, inv_df

with st.spinner('Loading data...'):
    sales_df, risk_df, inv_df = load_data()

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: white; margin: 0;">SCM Intelligence</h2>
        <p style="color: #7c4dff; margin: 5px 0; font-size: 12px;">SUPPLY CHAIN</p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    
    st.markdown("**Dashboard**")
    page = st.selectbox("", ["Overview", "Demand Forecasting", "Risk Analysis", "Inventory Optimization"], label_visibility="collapsed")
    
    st.divider()
    st.markdown("**Filters**")
    
    if page == "Overview":
        date_range = st.slider("Date Range", 
                              min_value=sales_df['date'].min().date(),
                              max_value=sales_df['date'].max().date(),
                              value=(sales_df['date'].min().date(), sales_df['date'].max().date()))
        selected_stores = st.multiselect("Stores", sales_df['store'].unique().tolist(), sales_df['store'].unique().tolist())
    elif page == "Demand Forecasting":
        forecast_store = st.selectbox("Select Store", sales_df['store'].unique())
        forecast_item = st.selectbox("Select Product", sales_df['item'].unique())
    elif page == "Risk Analysis":
        risk_level_filter = st.multiselect("Risk Level", ["Low", "Medium", "High"], ["Low", "Medium", "High"])
    elif page == "Inventory Optimization":
        service_level = st.slider("Service Level Target", 0.80, 0.99, 0.95)

st.markdown('<div class="gradient-header"><h1 style="color: white; margin: 0; font-size: 32px;">Supply Chain Intelligence Dashboard</h1><p style="color: rgba(255,255,255,0.8); margin: 5px 0 0 0;">Real-time analytics powered by ML</p></div>', unsafe_allow_html=True)

def metric_card(col, label, value, delta=None, color="#1a73e8"):
    with col:
        st.markdown(f"""
        <div class="stitched-card" style="border-left: 4px solid {color};">
            <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #666; margin-bottom: 10px;">{label}</div>
            <div style="font-size: 28px; font-weight: 700; color: #1a1a2e;">{value}</div>
            {f'<div style="font-size: 12px; color: #22c55e; margin-top: 5px;">{delta}</div>' if delta else ''}
        </div>
        """, unsafe_allow_html=True)

if page == "Overview":
    col1, col2, col3, col4 = st.columns(4)
    metric_card(col1, "Total Revenue", f"${sales_df['sales'].sum():,.0f}", color="#22c55e")
    metric_card(col2, "Daily Average", f"${sales_df['sales'].mean():,.1f}", color="#1a73e8")
    metric_card(col3, "Active Stores", sales_df['store'].nunique(), color="#7c4dff")
    metric_card(col4, "Products", sales_df['item'].nunique(), color="#f59e0b")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown('<div class="chart-container"><h3 style="margin-bottom: 20px;">Sales Trend Over Time</h3>', unsafe_allow_html=True)
        daily = sales_df.groupby('date')['sales'].sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily['date'], y=daily['sales'], mode='lines', fill='tozeroy', 
                                  line=dict(color='#1a73e8', width=3), fillcolor='rgba(26,115,232,0.3)'))
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20), xaxis_title="", yaxis_title="Sales", hovermode="x unified")
        st.plotly_chart(fig, width='stretch')
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<div class="chart-container"><h3 style="margin-bottom: 20px;">Sales by Store</h3>', unsafe_allow_html=True)
        store_sales = sales_df.groupby('store')['sales'].sum().reset_index().sort_values('sales', ascending=False).head(10)
        fig = px.bar(store_sales, x='store', y='sales', color='sales', color_continuous_scale=['#7c4dff', '#1a73e8'])
        fig.update_layout(height=400, showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, width='stretch')
        st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-container"><h3 style="margin-bottom: 20px;">Top 10 Products</h3>', unsafe_allow_html=True)
        top_items = sales_df.groupby('item')['sales'].sum().reset_index().sort_values('sales', ascending=False).head(10)
        fig = px.bar(top_items, x='item', y='sales', color='sales', color_continuous_scale='Blues_r')
        fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20), height=300)
        st.plotly_chart(fig, width='stretch')
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container"><h3 style="margin-bottom: 20px;">Sales Distribution</h3>', unsafe_allow_html=True)
        daily_sales = sales_df.groupby('date')['sales'].sum()
        fig = go.Figure()
        fig.add_trace(go.Box(y=daily_sales, name="Daily Sales", marker_color='#1a73e8', boxpoints='outliers'))
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, width='stretch')
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "Demand Forecasting":
    col1, col2, col3, col4 = st.columns(4)
    store_data = sales_df[sales_df['store'] == forecast_store]
    item_data = store_data[store_data['item'] == forecast_item]
    
    avg_sales = item_data['sales'].mean()
    max_sales = item_data['sales'].max()
    min_sales = item_data['sales'].min()
    total_sales = item_data['sales'].sum()
    
    metric_card(col1, "Total Sales", f"{total_sales:,}", color="#22c55e")
    metric_card(col2, "Avg Daily", f"{avg_sales:.1f}", color="#1a73e8")
    metric_card(col3, "Peak Sale", f"{max_sales:,}", color="#f59e0b")
    metric_card(col4, "Min Sale", f"{min_sales:,}", color="#ef4444")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f'<div class="chart-container"><h3 style="margin-bottom: 20px;">Store {forecast_store} - Product {forecast_item} Sales History</h3>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=item_data['date'], y=item_data['sales'], mode='lines', fill='tozeroy',
                                 line=dict(color='#1a73e8', width=2), fillcolor='rgba(26,115,232,0.2)'))
        fig.update_layout(height=450, hovermode="x unified", margin=dict(l=20, r=20, t=20, b=20), xaxis_title="", yaxis_title="Units Sold")
        fig.add_hline(y=avg_sales, line_dash="dash", line_color="red", annotation_text=f"Avg: {avg_sales:.1f}")
        st.plotly_chart(fig, width='stretch')
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container"><h3 style="margin-bottom: 20px;">Statistics</h3>', unsafe_allow_html=True)
        stats_df = pd.DataFrame({
            'Metric': ['Total Records', 'Date Range', 'Best Month', 'Worst Month'],
            'Value': [len(item_data), f"{item_data['date'].min().strftime('%b %Y')} - {item_data['date'].max().strftime('%b %Y')}", 
                     item_data.groupby(item_data['date'].dt.to_period('M'))['sales'].sum().idxmax(),
                     item_data.groupby(item_data['date'].dt.to_period('M'))['sales'].sum().idxmin()]
        })
        st.dataframe(stats_df, width='stretch', hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container"><h3 style="margin-bottom: 20px;">ML Model Performance</h3>', unsafe_allow_html=True)
    
    models = pd.DataFrame({
        'Model': ['XGBoost', 'LightGBM', 'LSTM', 'Ensemble'],
        'MAPE (%)': [12.08, 12.34, 13.21, 11.89],
        'MAE': [6.45, 6.78, 7.12, 6.23],
        'RMSE': [9.87, 10.12, 10.89, 9.45],
        'Training Time': ['2m 34s', '1m 56s', '8m 23s', '-']
    })
    st.dataframe(models, width='stretch', hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Risk Analysis":
    if risk_df.empty:
        st.warning("No risk data available. Please run the pipeline first: `python run_pipeline.py`")
    else:
        col1, col2, col3, col4 = st.columns(4)
        avg_risk = risk_df['overall_risk_score'].mean() if 'overall_risk_score' in risk_df else 0
        high_risk = len(risk_df[risk_df['risk_level'] == 'High']) if 'risk_level' in risk_df else 0
        
        metric_card(col1, "Total Suppliers", len(risk_df), color="#1a73e8")
        metric_card(col2, "Avg Risk Score", f"{avg_risk:.1f}", color="#f59e0b")
        metric_card(col3, "High Risk", high_risk, color="#ef4444")
        metric_card(col4, "Countries", risk_df['country'].nunique() if 'country' in risk_df else 0, color="#22c55e")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container"><h3 style="margin-bottom: 20px;">Risk Level Distribution</h3>', unsafe_allow_html=True)
            if 'risk_level' in risk_df:
                risk_counts = risk_df['risk_level'].value_counts()
                colors = {'Low': '#22c55e', 'Medium': '#f59e0b', 'High': '#ef4444'}
                fig = go.Figure(data=[go.Pie(labels=risk_counts.index, values=risk_counts.values, 
                                            marker=dict(colors=[colors.get(x, '#1a73e8') for x in risk_counts.index]),
                                            textinfo='label+percent', hole=0.4)])
                fig.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig, width='stretch')
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container"><h3 style="margin-bottom: 20px;">Geographic Risk</h3>', unsafe_allow_html=True)
            if 'country' in risk_df:
                country_risk = risk_df.groupby('country')['overall_risk_score'].mean().sort_values(ascending=False).head(10)
                fig = px.bar(x=country_risk.values, y=country_risk.index, orientation='h', 
                            color=country_risk.values, color_continuous_scale='RdYlGn_r')
                fig.update_layout(height=350, showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig, width='stretch')
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="chart-container"><h3 style="margin-bottom: 20px;">Supplier Details</h3>', unsafe_allow_html=True)
        display_cols = [c for c in ['supplier_id', 'country', 'overall_risk_score', 'delivery_risk', 'quality_risk', 'financial_risk', 'risk_level'] if c in risk_df.columns]
        if display_cols:
            st.dataframe(risk_df[display_cols].head(20), width='stretch', hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "Inventory Optimization":
    if inv_df.empty:
        st.warning("No inventory data available. Please run the pipeline first: `python run_pipeline.py`")
    else:
        col1, col2, col3, col4 = st.columns(4)
        avg_eoq = inv_df['eoq'].mean() if 'eoq' in inv_df else 0
        total_cost = inv_df['total_inventory_cost'].sum() if 'total_inventory_cost' in inv_df else 0
        avg_reorder = inv_df['reorder_point'].mean() if 'reorder_point' in inv_df else 0
        
        metric_card(col1, "Avg EOQ", f"{avg_eoq:.0f}", color="#1a73e8")
        metric_card(col2, "Total Cost", f"${total_cost:,.0f}", color="#22c55e")
        metric_card(col3, "Avg Reorder Pt", f"{avg_reorder:.0f}", color="#7c4dff")
        metric_card(col4, "Items", len(inv_df), color="#f59e0b")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container"><h3 style="margin-bottom: 20px;">Economic Order Quantity Distribution</h3>', unsafe_allow_html=True)
            if 'eoq' in inv_df:
                fig = go.Figure()
                fig.add_trace(go.Histogram(x=inv_df['eoq'], nbinsx=30, marker_color='#1a73e8', marker_line_color='white', marker_line_width=2))
                fig.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20), xaxis_title="EOQ", yaxis_title="Frequency")
                st.plotly_chart(fig, width='stretch')
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container"><h3 style="margin-bottom: 20px;">Cost Analysis</h3>', unsafe_allow_html=True)
            if 'total_inventory_cost' in inv_df:
                top_items = inv_df.nlargest(10, 'total_inventory_cost')
                fig = px.bar(top_items, x=top_items.index if 'item' not in inv_df else 'item', y='total_inventory_cost', 
                            color='total_inventory_cost', color_continuous_scale='Reds')
                fig.update_layout(height=350, showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig, width='stretch')
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="chart-container"><h3 style="margin-bottom: 20px;">Optimization Results</h3>', unsafe_allow_html=True)
        st.dataframe(inv_df.head(20), width='stretch', hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div class="footer">Supply Chain Intelligence Dashboard | Powered by ML | MTech Thesis Project</div>', unsafe_allow_html=True)
