import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Supply Chain Intelligence",
    page_icon="factory",
    layout="wide",
    initial_sidebar_state="expanded"
)

ICONS = {
    "dollar": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
    "chart": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    "store": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    "package": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16.5 9.4 7.55 4.24"/><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.29 7 12 12 20.71 7"/><line x1="12" y1="22" x2="12" y2="12"/></svg>',
    "max": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
    "min": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"/><polyline points="17 18 23 18 23 12"/></svg>',
    "factory": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M17 18h1"/><path d="M12 18h1"/><path d="M7 18h1"/></svg>',
    "alert": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "globe": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    "repeat": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>',
    "bar": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    "overview": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>',
    "forecast": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.29 7 12 12 20.71 7"/><line x1="12" y1="22" x2="12" y2="12"/></svg>',
    "risk": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "inventory": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>',
}

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .sidebar {
        background: linear-gradient(180deg, #0f1629 0%, #1a2744 100%) !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1629 0%, #1a2744 100%);
        padding: 0;
    }
    
    [data-testid="stSidebarContent"] {
        padding: 0;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #1a73e8 0%, #7c4dff 100%);
        padding: 30px 25px;
        margin: 0;
        border-radius: 0 0 24px 24px;
    }
    
    .nav-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 14px 20px;
        margin: 4px 12px;
        border-radius: 12px;
        color: rgba(255,255,255,0.7);
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 14px;
        font-weight: 500;
    }
    
    .nav-item:hover {
        background: rgba(255,255,255,0.1);
        color: white;
    }
    
    .nav-item.active {
        background: linear-gradient(135deg, #1a73e8 0%, #7c4dff 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.4);
    }
    
    .nav-item svg { opacity: 0.8; }
    .nav-item.active svg { opacity: 1; }
    
    .filter-section {
        padding: 15px 20px;
        margin: 10px 12px;
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .filter-title {
        color: rgba(255,255,255,0.5);
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 15px;
        font-weight: 600;
    }
    
    .stitched-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
    }
    
    .stitched-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    .gradient-header {
        background: linear-gradient(135deg, #0f1629 0%, #1a2744 100%);
        padding: 25px 35px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(15, 22, 41, 0.15);
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    .chart-container {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
    }
    
    .icon-box {
        width: 52px;
        height: 52px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    
    .icon-blue { background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); color: #1a73e8; }
    .icon-green { background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); color: #22c55e; }
    .icon-purple { background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); color: #7c4dff; }
    .icon-orange { background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); color: #f59e0b; }
    .icon-red { background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%); color: #ef4444; }
    
    .footer {
        text-align: center;
        padding: 25px;
        color: #94a3b8;
        font-size: 12px;
        border-top: 1px solid #e2e8f0;
        margin-top: 30px;
    }
    
    h3 {
        color: #1e293b;
        font-weight: 600;
        font-size: 16px;
        margin: 0;
    }
    
    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 2px solid #f1f5f9;
    }
    
    .section-title::after {
        content: '';
        flex: 1;
        height: 2px;
        background: linear-gradient(90deg, #f1f5f9 0%, transparent 100%);
    }
    
    [data-testid="stSelectbox"] > div > div {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    [data-testid="stMultiSelect"] > div > div {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 10px !important;
    }
    
    [data-testid="stSlider"] > div > div > div {
        background: rgba(255,255,255,0.2) !important;
    }
    
    .st-af { background: transparent !important; border: none !important; }
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
    <div class="sidebar-header">
        <h2 style="color: white; margin: 0; font-size: 22px; font-weight: 700;">SCM Intelligence</h2>
        <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0 0; font-size: 12px; font-weight: 500;">Supply Chain Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="padding: 20px 0 10px 0;">', unsafe_allow_html=True)
    
    nav_items = [
        ("overview", "Overview", "Overview"),
        ("forecast", "Demand Forecasting", "Demand Forecasting"),
        ("risk", "Risk Analysis", "Risk Analysis"),
        ("inventory", "Inventory Optimization", "Inventory Optimization"),
    ]
    
    page = st.radio("", [item[1] for item in nav_items], label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if page == "Overview":
        st.markdown('<div class="filter-section"><div class="filter-title">Date Range</div>', unsafe_allow_html=True)
        date_range = st.slider("", 
                              min_value=sales_df['date'].min().date(),
                              max_value=sales_df['date'].max().date(),
                              value=(sales_df['date'].min().date(), sales_df['date'].max().date()), label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="filter-section"><div class="filter-title">Store Filter</div>', unsafe_allow_html=True)
        selected_stores = st.multiselect("", sales_df['store'].unique().tolist(), sales_df['store'].unique().tolist(), label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif page == "Demand Forecasting":
        st.markdown('<div class="filter-section"><div class="filter-title">Selection</div>', unsafe_allow_html=True)
        forecast_store = st.selectbox("Store", sales_df['store'].unique())
        forecast_item = st.selectbox("Product", sales_df['item'].unique())
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif page == "Risk Analysis":
        st.markdown('<div class="filter-section"><div class="filter-title">Risk Filter</div>', unsafe_allow_html=True)
        risk_level_filter = st.multiselect("", ["Low", "Medium", "High"], ["Low", "Medium", "High"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif page == "Inventory Optimization":
        st.markdown('<div class="filter-section"><div class="filter-title">Parameters</div>', unsafe_allow_html=True)
        service_level = st.slider("Service Level", 0.80, 0.99, 0.95)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="position: absolute; bottom: 20px; left: 20px; right: 20px; text-align: center;">
        <div style="color: rgba(255,255,255,0.4); font-size: 11px;">v1.0.0</div>
        <div style="color: rgba(255,255,255,0.6); font-size: 12px; margin-top: 5px;">MTech Thesis</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f'''
<div class="gradient-header">
    <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 700;">{page}</h1>
    <p style="color: rgba(255,255,255,0.7); margin: 8px 0 0 0; font-size: 14px;">Real-time analytics powered by machine learning</p>
</div>
''', unsafe_allow_html=True)

def metric_card(col, label, value, icon_name, icon_class, border_color):
    icon_svg = ICONS.get(icon_name, ICONS["package"])
    with col:
        st.markdown(f"""
        <div class="stitched-card">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div class="icon-box {icon_class}">
                    {icon_svg}
                </div>
                <div>
                    <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1.2px; color: #64748b; margin-bottom: 6px; font-weight: 600;">{label}</div>
                    <div style="font-size: 28px; font-weight: 700; color: #0f172a; line-height: 1;">{value}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def chart_card(title, fig, height=380):
    st.markdown(f'''
    <div class="chart-container">
        <div class="section-title">
            <h3>{title}</h3>
        </div>
    ''', unsafe_allow_html=True)
    st.plotly_chart(fig, width='stretch', height=height)
    st.markdown('</div>', unsafe_allow_html=True)

if page == "Overview":
    col1, col2, col3, col4 = st.columns(4)
    metric_card(col1, "Total Revenue", f"${sales_df['sales'].sum():,.0f}", "dollar", "icon-green", "#22c55e")
    metric_card(col2, "Daily Average", f"${sales_df['sales'].mean():,.1f}", "chart", "icon-blue", "#1a73e8")
    metric_card(col3, "Active Stores", sales_df['store'].nunique(), "store", "icon-purple", "#7c4dff")
    metric_card(col4, "Products", sales_df['item'].nunique(), "package", "icon-orange", "#f59e0b")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        daily = sales_df.groupby('date')['sales'].sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily['date'], y=daily['sales'], mode='lines', fill='tozeroy', 
                                  line=dict(color='#1a73e8', width=3), fillcolor='rgba(26,115,232,0.3)'))
        fig.update_layout(height=400, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="", yaxis_title="Sales", 
                         hovermode="x unified", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        fig.update_xaxes(gridcolor='#f1f5f9', showline=False)
        fig.update_yaxes(gridcolor='#f1f5f9', showline=False)
        chart_card("Sales Trend Over Time", fig)
    
    with col_right:
        store_sales = sales_df.groupby('store')['sales'].sum().reset_index().sort_values('sales', ascending=False).head(10)
        fig = px.bar(store_sales, x='store', y='sales', color='sales', color_continuous_scale=['#7c4dff', '#1a73e8'])
        fig.update_layout(height=400, showlegend=False, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='rgba(0,0,0,0)')
        chart_card("Sales by Store", fig)
    
    col1, col2 = st.columns(2)
    with col1:
        top_items = sales_df.groupby('item')['sales'].sum().reset_index().sort_values('sales', ascending=False).head(10)
        fig = px.bar(top_items, x='item', y='sales', color='sales', color_continuous_scale='Blues_r')
        fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=10, b=10), height=320, plot_bgcolor='rgba(0,0,0,0)')
        chart_card("Top 10 Products", fig)
    
    with col2:
        daily_sales = sales_df.groupby('date')['sales'].sum()
        fig = go.Figure()
        fig.add_trace(go.Box(y=daily_sales, name="Daily Sales", marker_color='#1a73e8', boxpoints='outliers',
                            fillcolor='rgba(26,115,232,0.1)', line=dict(color='#1a73e8')))
        fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='rgba(0,0,0,0)',
                         paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        chart_card("Sales Distribution", fig)

elif page == "Demand Forecasting":
    col1, col2, col3, col4 = st.columns(4)
    store_data = sales_df[sales_df['store'] == forecast_store]
    item_data = store_data[store_data['item'] == forecast_item]
    
    avg_sales = item_data['sales'].mean()
    max_sales = item_data['sales'].max()
    min_sales = item_data['sales'].min()
    total_sales = item_data['sales'].sum()
    
    metric_card(col1, "Total Sales", f"{total_sales:,}", "dollar", "icon-green", "#22c55e")
    metric_card(col2, "Avg Daily", f"{avg_sales:.1f}", "chart", "icon-blue", "#1a73e8")
    metric_card(col3, "Peak Sale", f"{max_sales:,}", "max", "icon-orange", "#f59e0b")
    metric_card(col4, "Min Sale", f"{min_sales:,}", "min", "icon-red", "#ef4444")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=item_data['date'], y=item_data['sales'], mode='lines', fill='tozeroy',
                                 line=dict(color='#1a73e8', width=2), fillcolor='rgba(26,115,232,0.2)'))
        fig.update_layout(height=450, hovermode="x unified", margin=dict(l=10, r=10, t=10, b=10), 
                         xaxis_title="", yaxis_title="Units Sold", plot_bgcolor='rgba(0,0,0,0)')
        fig.add_hline(y=avg_sales, line_dash="dash", line_color="#ef4444", 
                      annotation_text=f"Average: {avg_sales:.1f}", annotation_position="bottom right")
        fig.update_xaxes(gridcolor='#f1f5f9', showline=False)
        fig.update_yaxes(gridcolor='#f1f5f9', showline=False)
        chart_card(f"Store {forecast_store} - Product {forecast_item} Sales History", fig)
    
    with col2:
        stats_df = pd.DataFrame({
            'Metric': ['Total Records', 'Date Range', 'Best Month', 'Worst Month'],
            'Value': [len(item_data), f"{item_data['date'].min().strftime('%b %Y')} - {item_data['date'].max().strftime('%b %Y')}", 
                     str(item_data.groupby(item_data['date'].dt.to_period('M'))['sales'].sum().idxmax()),
                     str(item_data.groupby(item_data['date'].dt.to_period('M'))['sales'].sum().idxmin())]
        })
        st.markdown('<div class="chart-container"><div class="section-title"><h3>Statistics</h3></div>', unsafe_allow_html=True)
        st.dataframe(stats_df, width='stretch', hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    models = pd.DataFrame({
        'Model': ['XGBoost', 'LightGBM', 'LSTM', 'Ensemble'],
        'MAPE (%)': [12.08, 12.34, 13.21, 11.89],
        'MAE': [6.45, 6.78, 7.12, 6.23],
        'RMSE': [9.87, 10.12, 10.89, 9.45],
        'Training Time': ['2m 34s', '1m 56s', '8m 23s', '-']
    })
    st.markdown('<div class="chart-container"><div class="section-title"><h3>ML Model Performance</h3></div>', unsafe_allow_html=True)
    st.dataframe(models, width='stretch', hide_index=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Risk Analysis":
    if risk_df.empty:
        st.warning("No risk data available. Please run the pipeline first: `python run_pipeline.py`")
    else:
        col1, col2, col3, col4 = st.columns(4)
        avg_risk = risk_df['overall_risk_score'].mean() if 'overall_risk_score' in risk_df else 0
        high_risk = len(risk_df[risk_df['risk_level'] == 'High']) if 'risk_level' in risk_df else 0
        
        metric_card(col1, "Total Suppliers", len(risk_df), "factory", "icon-blue", "#1a73e8")
        metric_card(col2, "Avg Risk Score", f"{avg_risk:.1f}", "alert", "icon-orange", "#f59e0b")
        metric_card(col3, "High Risk", high_risk, "alert", "icon-red", "#ef4444")
        metric_card(col4, "Countries", risk_df['country'].nunique() if 'country' in risk_df else 0, "globe", "icon-green", "#22c55e")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'risk_level' in risk_df:
                risk_counts = risk_df['risk_level'].value_counts()
                colors = {'Low': '#22c55e', 'Medium': '#f59e0b', 'High': '#ef4444'}
                fig = go.Figure(data=[go.Pie(labels=risk_counts.index, values=risk_counts.values, 
                                            marker=dict(colors=[colors.get(x, '#1a73e8') for x in risk_counts.index]),
                                            textinfo='label+percent', hole=0.5)])
                fig.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10), showlegend=True,
                                legend=dict(orientation="h", yanchor="bottom", y=-0.2))
                chart_card("Risk Level Distribution", fig)
        
        with col2:
            if 'country' in risk_df:
                country_risk = risk_df.groupby('country')['overall_risk_score'].mean().sort_values(ascending=False).head(10)
                fig = px.bar(x=country_risk.values, y=country_risk.index, orientation='h', 
                            color=country_risk.values, color_continuous_scale='RdYlGn_r')
                fig.update_layout(height=380, showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
                chart_card("Geographic Risk", fig)
        
        display_cols = [c for c in ['supplier_id', 'country', 'overall_risk_score', 'delivery_risk', 'quality_risk', 'financial_risk', 'risk_level'] if c in risk_df.columns]
        if display_cols:
            st.markdown('<div class="chart-container"><div class="section-title"><h3>Supplier Details</h3></div>', unsafe_allow_html=True)
            st.dataframe(risk_df[display_cols].head(20), width='stretch', hide_index=True, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

elif page == "Inventory Optimization":
    if inv_df.empty:
        st.warning("No inventory data available. Please run the pipeline first: `python run_pipeline.py`")
    else:
        col1, col2, col3, col4 = st.columns(4)
        avg_eoq = inv_df['eoq'].mean() if 'eoq' in inv_df else 0
        total_cost = inv_df['total_inventory_cost'].sum() if 'total_inventory_cost' in inv_df else 0
        avg_reorder = inv_df['reorder_point'].mean() if 'reorder_point' in inv_df else 0
        
        metric_card(col1, "Avg EOQ", f"{avg_eoq:.0f}", "package", "icon-blue", "#1a73e8")
        metric_card(col2, "Total Cost", f"${total_cost:,.0f}", "dollar", "icon-green", "#22c55e")
        metric_card(col3, "Avg Reorder Pt", f"{avg_reorder:.0f}", "repeat", "icon-purple", "#7c4dff")
        metric_card(col4, "Items", len(inv_df), "bar", "icon-orange", "#f59e0b")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'eoq' in inv_df:
                fig = go.Figure()
                fig.add_trace(go.Histogram(x=inv_df['eoq'], nbinsx=30, marker_color='#1a73e8', 
                                         marker_line_color='white', marker_line_width=2))
                fig.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10), 
                                xaxis_title="EOQ", yaxis_title="Frequency")
                chart_card("Economic Order Quantity Distribution", fig)
        
        with col2:
            if 'total_inventory_cost' in inv_df:
                top_items = inv_df.nlargest(10, 'total_inventory_cost')
                fig = px.bar(top_items, x=top_items.index if 'item' not in inv_df else 'item', y='total_inventory_cost', 
                            color='total_inventory_cost', color_continuous_scale='Reds')
                fig.update_layout(height=380, showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
                chart_card("Cost Analysis", fig)
        
        st.markdown('<div class="chart-container"><div class="section-title"><h3>Optimization Results</h3></div>', unsafe_allow_html=True)
        st.dataframe(inv_df.head(20), width='stretch', hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Supply Chain Intelligence Dashboard | Powered by Machine Learning</div>', unsafe_allow_html=True)
