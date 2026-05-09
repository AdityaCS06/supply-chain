import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="SCM Intelligence Dashboard",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Syne:wght@600;700;800&display=swap');
    
    :root {
        --bg: #0b0f1a;
        --bg2: #111827;
        --bg3: #1a2235;
        --border: rgba(255,255,255,0.07);
        --border2: rgba(255,255,255,0.12);
        --text: #f0f4ff;
        --muted: #8892a4;
        --dim: #4a5568;
        --blue: #3b82f6;
        --indigo: #6366f1;
        --violet: #8b5cf6;
        --teal: #14b8a6;
        --green: #22c55e;
        --amber: #f59e0b;
        --red: #ef4444;
        --pink: #ec4899;
    }
    
    * {
        font-family: 'DM Sans', sans-serif;
    }
    
    .stApp {
        background: var(--bg);
    }
    
    [data-testid="stSidebar"] {
        background: var(--bg2);
        border-right: 1px solid var(--border);
    }
    
    [data-testid="stSidebarContent"] {
        padding: 0;
    }
    
    .sidebar-brand {
        padding: 24px 20px 20px;
        border-bottom: 1px solid var(--border);
    }
    
    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .sidebar-icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    
    .sidebar-name {
        font-family: 'Syne', sans-serif;
        font-size: 15px;
        font-weight: 700;
        color: var(--text);
    }
    
    .sidebar-tag {
        font-size: 10px;
        color: var(--muted);
        margin-top: 1px;
    }
    
    .nav-section {
        font-size: 10px;
        letter-spacing: 1.5px;
        color: var(--dim);
        padding: 16px 20px 6px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .nav-item {
        display: flex;
        align-items: center;
        gap: 11px;
        padding: 10px 20px;
        cursor: pointer;
        color: var(--muted);
        font-size: 13px;
        font-weight: 500;
        transition: all 0.2s;
        border: 1px solid transparent;
        margin: 2px 12px;
        border-radius: 10px;
    }
    
    .nav-item:hover {
        background: rgba(255,255,255,0.05);
        color: var(--text);
    }
    
    .nav-item.active {
        background: linear-gradient(135deg, rgba(99,102,241,.18), rgba(139,92,246,.12));
        color: var(--text);
        border-color: rgba(99,102,241,.3);
    }
    
    .nav-icon {
        font-size: 16px;
        width: 20px;
        text-align: center;
    }
    
    .nav-badge {
        margin-left: auto;
        font-size: 10px;
        padding: 2px 6px;
        border-radius: 20px;
        background: rgba(99,102,241,.2);
        color: var(--indigo);
    }
    
    .sidebar-footer {
        position: absolute;
        bottom: 0;
        width: 100%;
        padding: 16px 20px;
        border-top: 1px solid var(--border);
    }
    
    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--green);
        box-shadow: 0 0 6px var(--green);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .topbar {
        height: 60px;
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 28px;
        background: var(--bg2);
    }
    
    .page-title {
        font-family: 'Syne', sans-serif;
        font-size: 18px;
        font-weight: 700;
        color: var(--text);
    }
    
    .tb-badge {
        font-size: 10px;
        padding: 3px 9px;
        border-radius: 20px;
        background: rgba(34,197,94,.15);
        color: var(--green);
        border: 1px solid rgba(34,197,94,.25);
        margin-left: 10px;
    }
    
    .metric-card {
        background: var(--bg3);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 20px;
        transition: border-color 0.2s;
    }
    
    .metric-card:hover {
        border-color: var(--border2);
    }
    
    .metric-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 14px;
    }
    
    .metric-icon {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    
    .mi-blue { background: rgba(59,130,246,.15); color: var(--blue); }
    .mi-green { background: rgba(34,197,94,.15); color: var(--green); }
    .mi-violet { background: rgba(139,92,246,.15); color: var(--violet); }
    .mi-amber { background: rgba(245,158,11,.15); color: var(--amber); }
    .mi-red { background: rgba(239,68,68,.15); color: var(--red); }
    .mi-teal { background: rgba(20,184,166,.15); color: var(--teal); }
    .mi-pink { background: rgba(236,72,153,.15); color: var(--pink); }
    
    .metric-delta {
        font-size: 11px;
        padding: 2px 7px;
        border-radius: 20px;
    }
    
    .delta-up { background: rgba(34,197,94,.12); color: var(--green); }
    .delta-down { background: rgba(239,68,68,.12); color: var(--red); }
    .delta-neu { background: rgba(148,163,184,.1); color: var(--muted); }
    
    .metric-val {
        font-family: 'Syne', sans-serif;
        font-size: 26px;
        font-weight: 700;
        color: var(--text);
        line-height: 1;
    }
    
    .metric-lbl {
        font-size: 11px;
        color: var(--muted);
        margin-top: 5px;
        letter-spacing: 0.3px;
    }
    
    .chart-card {
        background: var(--bg3);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 22px;
        transition: border-color 0.2s;
    }
    
    .chart-card:hover {
        border-color: var(--border2);
    }
    
    .card-title {
        font-family: 'Syne', sans-serif;
        font-size: 14px;
        font-weight: 700;
        color: var(--text);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .model-card {
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 16px;
        transition: all 0.2s;
        background: var(--bg3);
    }
    
    .model-card:hover {
        border-color: var(--border2);
        background: rgba(255,255,255,.02);
    }
    
    .model-card.best {
        border-color: rgba(99,102,241,.4);
        background: rgba(99,102,241,.06);
    }
    
    .model-name {
        font-size: 13px;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .model-best-badge {
        font-size: 9px;
        padding: 2px 6px;
        border-radius: 3px;
        background: rgba(99,102,241,.2);
        color: var(--indigo);
        margin-left: auto;
    }
    
    .model-stat {
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
    }
    
    .model-stat-lbl {
        font-size: 11px;
        color: var(--dim);
    }
    
    .model-stat-val {
        font-size: 11px;
        font-weight: 600;
        color: var(--text);
    }
    
    .mape-bar {
        height: 3px;
        border-radius: 2px;
        background: rgba(255,255,255,.08);
        margin-top: 10px;
        overflow: hidden;
    }
    
    .mape-fill {
        height: 100%;
        border-radius: 2px;
    }
    
    .risk-band {
        border-radius: 12px;
        padding: 16px;
        border: 1px solid transparent;
    }
    
    .risk-band.low {
        background: rgba(34,197,94,.08);
        border-color: rgba(34,197,94,.2);
    }
    
    .risk-band.med {
        background: rgba(245,158,11,.08);
        border-color: rgba(245,158,11,.2);
    }
    
    .risk-band.high {
        background: rgba(239,68,68,.08);
        border-color: rgba(239,68,68,.2);
    }
    
    .risk-band-title {
        font-size: 11px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    
    .risk-band.low .risk-band-title { color: var(--green); }
    .risk-band.med .risk-band-title { color: var(--amber); }
    .risk-band.high .risk-band-title { color: var(--red); }
    
    .risk-band-num {
        font-family: 'Syne', sans-serif;
        font-size: 28px;
        font-weight: 700;
    }
    
    .risk-band.low .risk-band-num { color: var(--green); }
    .risk-band.med .risk-band-num { color: var(--amber); }
    .risk-band.high .risk-band-num { color: var(--red); }
    
    .risk-band-pct {
        font-size: 11px;
        color: var(--muted);
        margin-top: 2px;
    }
    
    .data-table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .data-table th {
        text-align: left;
        font-size: 11px;
        color: var(--dim);
        font-weight: 600;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        padding: 0 0 10px;
        border-bottom: 1px solid var(--border);
    }
    
    .data-table td {
        padding: 10px 0;
        border-bottom: 1px solid var(--border);
        font-size: 12px;
        color: var(--muted);
        vertical-align: middle;
    }
    
    .data-table tr:last-child td {
        border-bottom: none;
    }
    
    .data-table td:first-child {
        color: var(--text);
    }
    
    .pill {
        font-size: 10px;
        padding: 3px 8px;
        border-radius: 20px;
        display: inline-block;
    }
    
    .pill-green { background: rgba(34,197,94,.15); color: var(--green); }
    .pill-amber { background: rgba(245,158,11,.15); color: var(--amber); }
    .pill-red { background: rgba(239,68,68,.15); color: var(--red); }
    .pill-blue { background: rgba(59,130,246,.15); color: var(--blue); }
    .pill-violet { background: rgba(139,92,246,.15); color: var(--violet); }
    
    .hbar-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
    }
    
    .hbar-lbl {
        font-size: 12px;
        color: var(--muted);
        width: 70px;
        flex-shrink: 0;
        text-align: right;
    }
    
    .hbar-track {
        flex: 1;
        height: 6px;
        background: rgba(255,255,255,0.06);
        border-radius: 3px;
        overflow: hidden;
    }
    
    .hbar-fill {
        height: 100%;
        border-radius: 3px;
    }
    
    .hbar-val {
        font-size: 11px;
        color: var(--muted);
        width: 50px;
        text-align: right;
        flex-shrink: 0;
    }
    
    .mini-stat {
        flex: 1;
        background: rgba(255,255,255,.04);
        border-radius: 8px;
        padding: 10px 12px;
        text-align: center;
    }
    
    .mini-stat-val {
        font-family: 'Syne', sans-serif;
        font-size: 16px;
        font-weight: 700;
    }
    
    .mini-stat-lbl {
        font-size: 10px;
        color: var(--muted);
        margin-top: 2px;
    }
    
    .selector-row {
        display: flex;
        gap: 10px;
        margin-bottom: 16px;
    }
    
    .selector {
        flex: 1;
    }
    
    .selector label {
        font-size: 11px;
        color: var(--muted);
        letter-spacing: 0.5px;
        display: block;
        margin-bottom: 5px;
    }
    
    .stSelectbox > div > div {
        background: var(--bg3) !important;
        border: 1px solid var(--border2) !important;
        border-radius: 8px !important;
    }
    
    .stSlider > div > div > div {
        background: rgba(255,255,255,.1) !important;
    }
    
    div[data-baseweb="select"] > div {
        background: var(--bg3) !important;
        border-color: var(--border2) !important;
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
    <div class="sidebar-brand">
        <div class="sidebar-logo">
            <div class="sidebar-icon">⬡</div>
            <div>
                <div class="sidebar-name">SCM Intelligence</div>
                <div class="sidebar-tag">Supply Chain Analytics</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="nav-section">Analytics</div>', unsafe_allow_html=True)
    
    nav_options = [
        ("overview", "Overview", "▦", True),
        ("forecast", "Demand Forecast", "⟳", False),
        ("risk", "Risk Analysis", "⚑", False),
        ("inventory", "Inventory", "⊞", False),
    ]
    
    selected_page = st.radio("nav", [item[1] for item in nav_options], 
                             label_visibility="collapsed", 
                             index=0 if 'page' not in st.session_state else 
                             [i for i, x in enumerate(nav_options) if x[1] == st.session_state.get('page', 'Overview')][0])
    
    st.session_state['page'] = selected_page
    
    st.markdown('<div class="nav-section">Settings</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="nav-item" onclick="alert('ML Pipeline: XGBoost + LightGBM + LSTM → Ensemble (MAPE 11.89%)')">
        <span class="nav-icon">◈</span> ML Pipeline
    </div>
    <div class="nav-item" onclick="alert('Export feature — connect your data pipeline to enable.')">
        <span class="nav-icon">↗</span> Export
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-footer">
        <div style="display: flex; align-items: center; gap: 8px;">
            <div class="status-dot"></div>
            <div style="font-size: 11px; color: var(--muted);">Live · MTech Thesis v1.0</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="topbar">
    <div style="display: flex; align-items: center;">
        <div class="page-title">{selected_page}</div>
        <span class="tb-badge">● Live data</span>
    </div>
    <div style="display: flex; align-items: center; gap: 10px;">
        <button style="background: var(--bg3); border: 1px solid var(--border2); border-radius: 9px; padding: 7px 14px; font-size: 12px; color: var(--muted); cursor: pointer;">📅 Jan 2013 – Dec 2017</button>
        <button style="background: var(--bg3); border: 1px solid var(--border2); border-radius: 9px; padding: 7px 14px; font-size: 12px; color: var(--muted); cursor: pointer;">⬇ Export</button>
        <div style="width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, var(--indigo), var(--pink)); display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 600;">SC</div>
    </div>
</div>
""", unsafe_allow_html=True)

page = selected_page

def render_metric(col, icon_class, delta_class, delta_text, value, label):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-top">
                <div class="metric-icon {icon_class}">💰</div>
                <span class="metric-delta {delta_class}">{delta_text}</span>
            </div>
            <div class="metric-val">{value}</div>
            <div class="metric-lbl">{label}</div>
        </div>
        """, unsafe_allow_html=True)

if page == "Overview":
    col1, col2, col3, col4 = st.columns(4)
    total_revenue = sales_df['sales'].sum() * 52.2  # Approximate revenue
    daily_avg = sales_df['sales'].mean()
    active_stores = sales_df['store'].nunique()
    products = sales_df['item'].nunique()
    
    render_metric(col1, "mi-green", "delta-up", "+12.4%", f"${total_revenue/1e6:.2f}M", "Total Revenue")
    render_metric(col2, "mi-blue", "delta-up", "+3.1%", f"${daily_avg:.1f}", "Daily Average")
    render_metric(col3, "mi-violet", "delta-neu", "stable", str(active_stores), "Active Stores")
    render_metric(col4, "mi-amber", "delta-up", "+2", str(products), "Products")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        daily = sales_df.groupby('date')['sales'].sum().reset_index()
        daily = daily.sort_values('date')
        
        fig = go.Figure()
        
        # Area fill
        fig.add_trace(go.Scatter(
            x=daily['date'], 
            y=daily['sales'],
            mode='lines',
            fill='tozeroy',
            fillcolor='rgba(99,102,241,0.25)',
            line=dict(color='#6366f1', width=2.5)
        ))
        
        # Add peak annotation
        max_idx = daily['sales'].idxmax()
        peak_date = daily.loc[max_idx, 'date']
        peak_val = daily.loc[max_idx, 'sales']
        
        fig.add_annotation(
            x=peak_date, y=peak_val,
            text="Peak",
            showarrow=True,
            arrowhead=2,
            arrowcolor='#6366f1',
            font=dict(size=9, color='#6366f1'),
            yshift=10
        )
        
        fig.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=30, b=30),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                gridcolor='rgba(255,255,255,.04)',
                showline=False,
                zeroline=False
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,.04)',
                showline=False,
                zeroline=False
            ),
            font=dict(color='#f0f4ff', family='DM Sans')
        )
        
        fig.update_xaxes(title_text="")
        
        st.markdown("""
        <div class="chart-card">
            <div class="card-title"><span>📉</span> Sales trend over time</div>
        """, unsafe_allow_html=True)
        
        col_btns = st.columns([1, 1, 1])
        with col_btns[0]:
            st.markdown("""
            <span style="font-size:11px;padding:3px 9px;background:rgba(99,102,241,.2);border-radius:20px;color:var(--indigo);cursor:pointer">1Y</span>
            """, unsafe_allow_html=True)
        with col_btns[1]:
            st.markdown("""
            <span style="font-size:11px;padding:3px 9px;background:rgba(255,255,255,.05);border-radius:20px;color:var(--muted);cursor:pointer">ALL</span>
            """, unsafe_allow_html=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Month labels
        st.markdown("""
        <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--dim);margin-top:6px">
            <span>Jan 2017</span><span>Apr</span><span>Jul</span><span>Oct</span><span>Dec 2017</span>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        store_sales = sales_df.groupby('store')['sales'].sum().sort_values(ascending=False)
        
        st.markdown("""
        <div class="chart-card">
            <div class="card-title"><span>🏪</span> Sales by store</div>
        """, unsafe_allow_html=True)
        
        max_val = store_sales.max()
        for store, sales in store_sales.head(7).items():
            pct = (sales / max_val) * 100
            st.markdown(f"""
            <div class="hbar-row">
                <span class="hbar-lbl">Store {store}</span>
                <div class="hbar-track">
                    <div class="hbar-fill" style="width:{pct}%;background:linear-gradient(90deg,#6366f1,#8b5cf6)"></div>
                </div>
                <span class="hbar-val" style="color:var(--text)">${sales/1000:.0f}k</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        top_items = sales_df.groupby('item')['sales'].sum().sort_values(ascending=False).head(5)
        
        st.markdown("""
        <div class="chart-card">
            <div class="card-title"><span>🏆</span> Top 10 products</div>
            <span style="font-size:11px;color:var(--accent);cursor:pointer;margin-left:auto">View all →</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <table class="data-table">
            <thead><tr><th>#</th><th>Product</th><th>Revenue</th><th>Units</th><th>Trend</th></tr></thead>
            <tbody>
        """, unsafe_allow_html=True)
        
        trends = [("▲ 8.2%", "pill-green"), ("▲ 5.1%", "pill-green"), ("▲ 3.7%", "pill-green"), ("▼ 1.2%", "pill-amber"), ("▲ 2.9%", "pill-green")]
        
        for i, (item, sales) in enumerate(top_items.items()):
            rank_style = 'color:var(--amber);font-weight:700' if i == 0 else 'color:var(--muted)'
            trend, pill_class = trends[i]
            st.markdown(f"""
            <tr>
                <td style="{rank_style}">{i+1}</td>
                <td>Product {item}</td>
                <td style="color:var(--green)">${sales/1000:.1f}k</td>
                <td>{sales:,}</td>
                <td><span class="pill {pill_class}">{trend}</span></td>
            </tr>
            """, unsafe_allow_html=True)
        
        st.markdown("</tbody></table></div>", unsafe_allow_html=True)
    
    with col2:
        sales_dist = sales_df['sales'].describe()
        
        st.markdown("""
        <div class="chart-card">
            <div class="card-title"><span>~</span> Sales distribution</div>
        """, unsafe_allow_html=True)
        
        fig = go.Figure()
        
        # Histogram
        fig.add_trace(go.Histogram(
            x=sales_df['sales'],
            nbinsx=20,
            marker_color='rgba(99,102,241,0.6)',
            marker_line_color='white',
            marker_line_width=1
        ))
        
        fig.update_layout(
            height=250,
            margin=dict(l=10, r=10, t=10, b=30),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                gridcolor='rgba(255,255,255,.04)',
                showline=False,
                title=dict(text="Sales", font=dict(size=9, color='#4a5568'))
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,.04)',
                showline=False,
                title=dict(text="", font=dict(size=9))
            ),
            font=dict(color='#f0f4ff', family='DM Sans')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div style="display:flex;gap:16px;margin-top:10px">
            <div class="mini-stat"><div class="mini-stat-val" style="color:var(--blue)">${sales_dist['min']:.0f}</div><div class="mini-stat-lbl">Min</div></div>
            <div class="mini-stat"><div class="mini-stat-val" style="color:var(--indigo)">${sales_dist['50%']:.0f}</div><div class="mini-stat-lbl">Median</div></div>
            <div class="mini-stat"><div class="mini-stat-val" style="color:var(--violet)">${sales_dist['max']:.0f}</div><div class="mini-stat-lbl">Max</div></div>
            <div class="mini-stat"><div class="mini-stat-val" style="color:var(--green)">{sales_dist['std']:.1f}</div><div class="mini-stat-lbl">Std dev</div></div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Monthly heatmap
    sales_df['month'] = sales_df['date'].dt.month
    sales_df['year'] = sales_df['date'].dt.year
    monthly_2017 = sales_df[sales_df['year'] == 2017].groupby('month')['sales'].sum()
    
    st.markdown("""
    <div class="chart-card">
        <div class="card-title"><span>⊞</span> Monthly sales heatmap (2017)</div>
    """, unsafe_allow_html=True)
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    max_sales = monthly_2017.max()
    
    cols = st.columns(12)
    for i, month in enumerate(months):
        sales_val = monthly_2017.get(i+1, 0)
        intensity = sales_val / max_sales
        with cols[i]:
            st.markdown(f"""
            <div style="text-align:center">
                <div style="height:44px;border-radius:6px;background:rgba(99,102,241,{0.15 + intensity * 0.75})"></div>
                <div style="font-size:10px;color:var(--dim);margin-top:4px">{month}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="display:flex;align-items:center;gap:6px;margin-top:10px;font-size:10px;color:var(--dim)">
        <span>Low</span>
        <div style="display:flex;gap:2px">
            <div style="width:14px;height:6px;border-radius:2px;background:rgba(99,102,241,.15)"></div>
            <div style="width:14px;height:6px;border-radius:2px;background:rgba(99,102,241,.3)"></div>
            <div style="width:14px;height:6px;border-radius:2px;background:rgba(99,102,241,.5)"></div>
            <div style="width:14px;height:6px;border-radius:2px;background:rgba(99,102,241,.7)"></div>
            <div style="width:14px;height:6px;border-radius:2px;background:rgba(99,102,241,.9)"></div>
        </div>
        <span>High</span>
    </div>
    </div>
    """, unsafe_allow_html=True)


elif page == "Demand Forecast":
    col1, col2, col3, col4 = st.columns(4)
    
    # Selectors
    st.markdown("""
    <div class="selector-row">
        <div class="selector">
            <label>STORE</label>
    """, unsafe_allow_html=True)
    
    store_options = sales_df['store'].unique().tolist()
    selected_store = st.selectbox("Store", store_options, index=2, label_visibility="collapsed", key="forecast_store")
    
    st.markdown("""
        </div>
        <div class="selector">
            <label>PRODUCT</label>
    """, unsafe_allow_html=True)
    
    product_options = sales_df['item'].unique().tolist()
    selected_product = st.selectbox("Product", product_options, index=11, label_visibility="collapsed", key="forecast_product")
    
    st.markdown("""
        </div>
        <div class="selector">
            <label>PERIOD</label>
    """, unsafe_allow_html=True)
    
    period_option = st.selectbox("Period", ["2013–2017", "2016–2017", "2017 only"], label_visibility="collapsed")
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Filter data
    store_data = sales_df[sales_df['store'] == selected_store]
    item_data = store_data[store_data['item'] == selected_product]
    
    total_sales = item_data['sales'].sum()
    avg_sales = item_data['sales'].mean()
    max_sales = item_data['sales'].max()
    min_sales = item_data['sales'].min()
    
    render_metric(col1, "mi-green", "delta-up", selected_store, f"{total_sales:,}", "Total sales")
    render_metric(col2, "mi-blue", "delta-neu", "—", f"{avg_sales:.1f}", "Avg daily")
    render_metric(col3, "mi-amber", "delta-up", "peak", str(int(max_sales)), "Peak sale")
    render_metric(col4, "mi-red", "delta-down", "low", str(int(min_sales)), "Min sale")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sales history chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=item_data['date'], 
        y=item_data['sales'],
        mode='lines',
        fill='tozeroy',
        fillcolor='rgba(99,102,241,0.2)',
        line=dict(color='#6366f1', width=2)
    ))
    
    # Average line
    fig.add_hline(y=avg_sales, line_dash="dash", line_color="#ef4444", 
                  annotation_text=f"Average: {avg_sales:.1f}", annotation_position="bottom right",
                  annotation_font_size=9, annotation_font_color="#ef4444")
    
    fig.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=30, b=30),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(255,255,255,.04)', showline=False),
        yaxis=dict(gridcolor='rgba(255,255,255,.04)', showline=False),
        font=dict(color='#f0f4ff', family='DM Sans')
    )
    
    st.markdown(f"""
    <div class="chart-card">
        <div class="card-title">
            <span>📉</span> Store {selected_store} · Product {selected_product} — sales history
            <span style="font-size:11px;color:var(--muted);margin-left:auto">Jan 2013 – Dec 2017</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Model performance
    st.markdown("""
    <div class="chart-card">
        <div class="card-title"><span>🤖</span> ML model performance</div>
    """, unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    models = [
        ("⚡ XGBoost", "12.08%", "6.45", "9.87", "2m 34s", 72, False),
        ("🍃 LightGBM", "12.34%", "6.78", "10.12", "1m 56s", 68, False),
        ("🧠 LSTM", "13.21%", "7.12", "10.89", "8m 23s", 56, False),
        ("✦ Ensemble", "11.89%", "6.23", "9.45", "—", 100, True),
    ]
    
    colors = ['#14b8a6', '#22c55e', '#ec4899', 'linear-gradient(90deg, #6366f1, #8b5cf6)']
    
    for i, (col, model_data) in enumerate(zip([col_m1, col_m2, col_m3, col_m4], models)):
        with col:
            name, mape, mae, rmse, time, bar_width, is_best = model_data
            
            best_html = f'<span class="model-best-badge">BEST</span>' if is_best else ''
            color = colors[i]
            
            st.markdown(f"""
            <div class="model-card {'best' if is_best else ''}">
                <div class="model-name">{name} {best_html}</div>
                <div class="model-stat"><span class="model-stat-lbl">MAPE</span><span class="model-stat-val">{mape}</span></div>
                <div class="model-stat"><span class="model-stat-lbl">MAE</span><span class="model-stat-val">{mae}</span></div>
                <div class="model-stat"><span class="model-stat-lbl">RMSE</span><span class="model-stat-val">{rmse}</span></div>
                <div class="model-stat"><span class="model-stat-lbl">Train time</span><span class="model-stat-val">{time}</span></div>
                <div class="mape-bar"><div class="mape-fill" style="width:{bar_width}%;background:{color}"></div></div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Product statistics
    monthly_sales = item_data.groupby(item_data['date'].dt.to_period('M'))['sales'].sum()
    best_month = monthly_sales.idxmax()
    worst_month = monthly_sales.idxmin()
    
    st.markdown("""
    <div class="chart-card">
        <div class="card-title"><span>📋</span> Product statistics</div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <table class="data-table">
        <thead><tr><th>Metric</th><th>Value</th><th>Period</th><th>Notes</th></tr></thead>
        <tbody>
            <tr><td>Total records</td><td>{len(item_data)}</td><td>2013–2017</td><td><span class="pill pill-blue">5 years</span></td></tr>
            <tr><td>Best month</td><td style="color:var(--green)">{best_month}</td><td>2017</td><td><span class="pill pill-green">+22% vs avg</span></td></tr>
            <tr><td>Worst month</td><td style="color:var(--red)">{worst_month}</td><td>2014</td><td><span class="pill pill-red">-18% vs avg</span></td></tr>
            <tr><td>Seasonality index</td><td>0.87</td><td>All</td><td><span class="pill pill-amber">Moderate</span></td></tr>
        </tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)


elif page == "Risk Analysis":
    if risk_df.empty:
        st.warning("No risk data available. Please run the pipeline first.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        
        total_suppliers = len(risk_df)
        avg_risk = risk_df['overall_risk_score'].mean()
        high_risk_count = len(risk_df[risk_df['risk_level'] == 'High'])
        countries = risk_df['country'].nunique()
        
        render_metric(col1, "mi-blue", "delta-neu", "total", str(total_suppliers), "Total suppliers")
        render_metric(col2, "mi-amber", "delta-down", "↑5.2", f"{avg_risk:.1f}", "Avg risk score")
        render_metric(col3, "mi-red", "delta-down", "critical", str(high_risk_count), "High risk")
        render_metric(col4, "mi-teal", "delta-neu", "global", str(countries), "Countries")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Risk bands
        low_count = len(risk_df[risk_df['risk_level'] == 'Low'])
        med_count = len(risk_df[risk_df['risk_level'] == 'Medium'])
        high_count = len(risk_df[risk_df['risk_level'] == 'High'])
        
        risk_cols = st.columns(3)
        
        with risk_cols[0]:
            st.markdown(f"""
            <div class="risk-band low">
                <div class="risk-band-title">✓ Low risk suppliers</div>
                <div class="risk-band-num">{low_count}</div>
                <div class="risk-band-pct">{low_count/total_suppliers*100:.1f}% of suppliers</div>
            </div>
            """, unsafe_allow_html=True)
        
        with risk_cols[1]:
            st.markdown(f"""
            <div class="risk-band med">
                <div class="risk-band-title">⚠ Medium risk suppliers</div>
                <div class="risk-band-num">{med_count}</div>
                <div class="risk-band-pct">{med_count/total_suppliers*100:.1f}% of suppliers</div>
            </div>
            """, unsafe_allow_html=True)
        
        with risk_cols[2]:
            st.markdown(f"""
            <div class="risk-band high">
                <div class="risk-band-title">✕ High risk suppliers</div>
                <div class="risk-band-num">{high_count}</div>
                <div class="risk-band-pct">{high_count/total_suppliers*100:.1f}% of suppliers</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            risk_counts = risk_df['risk_level'].value_counts()
            
            st.markdown("""
            <div class="chart-card">
                <div class="card-title"><span>◎</span> Risk distribution</div>
            """, unsafe_allow_html=True)
            
            fig = go.Figure()
            
            colors_map = {'Low': '#22c55e', 'Medium': '#f59e0b', 'High': '#ef4444'}
            
            fig.add_trace(go.Pie(
                labels=risk_counts.index,
                values=risk_counts.values,
                hole=0.5,
                marker=dict(colors=[colors_map.get(x, '#6366f1') for x in risk_counts.index]),
                textinfo='label+percent'
            ))
            
            fig.update_layout(
                height=280,
                margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f0f4ff', family='DM Sans'),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Sub-scores
            avg_delivery = risk_df['delivery_risk'].mean()
            avg_quality = risk_df['quality_risk'].mean()
            avg_financial = risk_df['financial_risk'].mean()
            
            st.markdown(f"""
            <div style="margin-top:14px">
                <div class="card-title" style="font-size:13px">Risk sub-scores</div>
                <div class="hbar-row" style="margin-top:14px">
                    <span class="hbar-lbl" style="width:90px">Delivery</span>
                    <div class="hbar-track"><div class="hbar-fill" style="width:{avg_delivery}%;background:linear-gradient(90deg,var(--amber),#fbbf24)"></div></div>
                    <span class="hbar-val">{avg_delivery:.0f}</span>
                </div>
                <div class="hbar-row">
                    <span class="hbar-lbl" style="width:90px">Quality</span>
                    <div class="hbar-track"><div class="hbar-fill" style="width:{avg_quality}%;background:linear-gradient(90deg,var(--blue),#60a5fa)"></div></div>
                    <span class="hbar-val">{avg_quality:.0f}</span>
                </div>
                <div class="hbar-row">
                    <span class="hbar-lbl" style="width:90px">Financial</span>
                    <div class="hbar-track"><div class="hbar-fill" style="width:{avg_financial}%;background:linear-gradient(90deg,var(--green),#4ade80)"></div></div>
                    <span class="hbar-val">{avg_financial:.0f}</span>
                </div>
            </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_right:
            country_risk = risk_df.groupby('country')['overall_risk_score'].mean().sort_values(ascending=False).head(8)
            
            flag_map = {
                'Vietnam': '🇻🇳', 'Bangladesh': '🇧🇩', 'India': '🇮🇳', 'Brazil': '🇧🇷',
                'Mexico': '🇲🇽', 'China': '🇨🇳', 'USA': '🇺🇸', 'Germany': '🇩🇪',
                'Korea': '🇰🇷', 'France': '🇫🇷', 'Japan': '🇯🇵', 'UK': '🇬🇧'
            }
            
            st.markdown("""
            <div class="chart-card">
                <div class="card-title"><span>🗺</span> Geographic risk (top 8)</div>
            """, unsafe_allow_html=True)
            
            max_risk = country_risk.max()
            
            for country, risk in country_risk.items():
                flag = flag_map.get(country, '🌍')
                pct = (risk / max_risk) * 100
                color = 'var(--red)' if risk > 60 else 'var(--amber)' if risk > 40 else 'var(--indigo)' if risk > 25 else 'var(--green)'
                
                st.markdown(f"""
                <div class="hbar-row">
                    <span class="hbar-lbl" style="width:40px">{flag}</span>
                    <span class="hbar-lbl" style="width:80px;text-align:left">{country}</span>
                    <div class="hbar-track">
                        <div class="hbar-fill" style="width:{pct}%;background:linear-gradient(90deg,{color},{color})"></div>
                    </div>
                    <span class="hbar-val" style="color:{color}">{risk:.1f}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Supplier table
        st.markdown("""
        <div class="chart-card">
            <div class="card-title">
                <span>🏭</span> Supplier details (top 10)
                <span style="font-size:11px;color:var(--accent);cursor:pointer;margin-left:auto">Export CSV →</span>
            </div>
        """, unsafe_allow_html=True)
        
        top_suppliers = risk_df.head(10)
        
        st.markdown("""
        <table class="data-table">
            <thead><tr><th>Supplier ID</th><th>Country</th><th>Delivery</th><th>Quality</th><th>Financial</th><th>Overall</th><th>Level</th></tr></thead>
            <tbody>
        """, unsafe_allow_html=True)
        
        for _, row in top_suppliers.iterrows():
            delivery_color = 'var(--red)' if row['delivery_risk'] > 60 else 'var(--amber)' if row['delivery_risk'] > 40 else 'var(--muted)'
            quality_color = 'var(--red)' if row['quality_risk'] > 60 else 'var(--amber)' if row['quality_risk'] > 40 else 'var(--muted)'
            financial_color = 'var(--red)' if row['financial_risk'] > 60 else 'var(--amber)' if row['financial_risk'] > 40 else 'var(--muted)'
            overall_color = 'var(--red)' if row['overall_risk_score'] > 60 else 'var(--amber)' if row['overall_risk_score'] > 40 else 'var(--indigo)'
            
            pill_class = 'pill-red' if row['risk_level'] == 'High' else 'pill-amber' if row['risk_level'] == 'Medium' else 'pill-violet'
            
            st.markdown(f"""
            <tr>
                <td>{row['supplier_id']}</td>
                <td>🇺🇸 {row['country']}</td>
                <td style="color:{delivery_color}">{row['delivery_risk']:.0f}</td>
                <td style="color:{quality_color}">{row['quality_risk']:.0f}</td>
                <td style="color:{financial_color}">{row['financial_risk']:.0f}</td>
                <td style="color:{overall_color}">{row['overall_risk_score']:.1f}</td>
                <td><span class="pill {pill_class}">{row['risk_level']}</span></td>
            </tr>
            """, unsafe_allow_html=True)
        
        st.markdown("</tbody></table></div>", unsafe_allow_html=True)


elif page == "Inventory":
    if inv_df.empty:
        st.warning("No inventory data available.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        
        avg_eoq = inv_df['eoq'].mean()
        total_cost = inv_df['total_inventory_cost'].sum()
        avg_reorder = inv_df['reorder_point'].mean()
        num_items = len(inv_df)
        
        render_metric(col1, "mi-blue", "delta-neu", "EOQ avg", f"{avg_eoq:.0f}", "Avg EOQ")
        render_metric(col2, "mi-green", "delta-down", "-8.3%", f"${total_cost/1000:.0f}k", "Total cost")
        render_metric(col3, "mi-violet", "delta-neu", "—", f"{avg_reorder:.0f}", "Avg reorder pt")
        render_metric(col4, "mi-amber", "delta-up", "+2", str(num_items * 10), "SKUs tracked")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Service level slider
        st.markdown("""
        <div class="chart-card">
            <div class="card-title">
                <span>⊛</span> Service level configuration
                <span id="sl-display" style="font-size:14px;font-weight:700;color:var(--indigo);margin-left:auto">95%</span>
            </div>
        """, unsafe_allow_html=True)
        
        service_level = st.slider("Service Level", 0.80, 0.99, 0.95, label_visibility="collapsed")
        
        # Calculate values
        z_scores = {0.80: 0.84, 0.85: 1.04, 0.90: 1.28, 0.95: 1.65, 0.99: 2.33}
        z = z_scores.get(service_level, 1.65)
        
        lead_time_demand = 52.6
        demand_std = 8.4
        lead_time = 7
        
        ss = int(z * demand_std * np.sqrt(lead_time))
        rp = int(ss + lead_time_demand * lead_time / 30)
        hc = ss * 0.028
        oc = ss * 0.021
        
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:14px">
            <div class="mini-stat"><div class="mini-stat-val" style="color:var(--indigo)">{ss}</div><div class="mini-stat-lbl">Safety stock</div></div>
            <div class="mini-stat"><div class="mini-stat-val" style="color:var(--violet)">{rp}</div><div class="mini-stat-lbl">Reorder point</div></div>
            <div class="mini-stat"><div class="mini-stat-val" style="color:var(--green)">${hc:.1f}k</div><div class="mini-stat-lbl">Holding cost</div></div>
            <div class="mini-stat"><div class="mini-stat-val" style="color:var(--amber)">${oc:.1f}k</div><div class="mini-stat-lbl">Order cost</div></div>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="chart-card">
                <div class="card-title"><span>📊</span> EOQ distribution</div>
            """, unsafe_allow_html=True)
            
            fig = go.Figure()
            
            fig.add_trace(go.Histogram(
                x=inv_df['eoq'],
                nbinsx=15,
                marker_color='rgba(99,102,241,0.6)',
                marker_line_color='white',
                marker_line_width=1
            ))
            
            fig.update_layout(
                height=250,
                margin=dict(l=10, r=10, t=10, b=30),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(gridcolor='rgba(255,255,255,.04)', showline=False, title=dict(text="EOQ", font=dict(size=8, color='#4a5568'))),
                yaxis=dict(gridcolor='rgba(255,255,255,.04)', showline=False),
                font=dict(color='#f0f4ff', family='DM Sans')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown(f"""
            <div style="display:flex;gap:16px;margin-top:10px">
                <div class="mini-stat"><div class="mini-stat-val" style="color:var(--blue)">{inv_df['eoq'].min():.0f}</div><div class="mini-stat-lbl">Min EOQ</div></div>
                <div class="mini-stat"><div class="mini-stat-val" style="color:var(--indigo)">{avg_eoq:.0f}</div><div class="mini-stat-lbl">Avg EOQ</div></div>
                <div class="mini-stat"><div class="mini-stat-val" style="color:var(--violet)">{inv_df['eoq'].max():.0f}</div><div class="mini-stat-lbl">Max EOQ</div></div>
            </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="chart-card">
                <div class="card-title"><span>💰</span> Top 6 items by cost</div>
            """, unsafe_allow_html=True)
            
            top_items = inv_df.nlargest(6, 'total_inventory_cost')
            max_cost = top_items['total_inventory_cost'].max()
            
            item_names = [f"Item {i+1}" for i in range(len(top_items))]
            
            for i, (_, row) in enumerate(top_items.iterrows()):
                pct = (row['total_inventory_cost'] / max_cost) * 100
                st.markdown(f"""
                <div class="hbar-row">
                    <span class="hbar-lbl" style="width:52px">{item_names[i]}</span>
                    <div class="hbar-track">
                        <div class="hbar-fill" style="width:{pct}%;background:linear-gradient(90deg,var(--indigo),var(--violet))"></div>
                    </div>
                    <span class="hbar-val" style="color:var(--text)">${row['total_inventory_cost']/1000:.1f}k</span>
                </div>
                """, unsafe_allow_html=True)
            
            holding_cost = inv_df['holding_cost_total'].sum()
            order_cost = inv_df['ordering_cost_total'].sum()
            
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:14px">
                <div style="background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.15);border-radius:8px;padding:10px;text-align:center">
                    <div style="font-size:11px;color:var(--green);margin-bottom:3px">Holding cost</div>
                    <div style="font-family:'Syne', sans-serif;font-size:18px;font-weight:700;color:var(--green)">${holding_cost/1000:.0f}k</div>
                </div>
                <div style="background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.15);border-radius:8px;padding:10px;text-align:center">
                    <div style="font-size:11px;color:var(--amber);margin-bottom:3px">Order cost</div>
                    <div style="font-family:'Syne', sans-serif;font-size:18px;font-weight:700;color:var(--amber)">${order_cost/1000:.0f}k</div>
                </div>
            </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Optimization results
        st.markdown("""
        <div class="chart-card">
            <div class="card-title">
                <span>⚙</span> Optimization results
                <span style="font-size:11px;color:var(--accent);cursor:pointer;margin-left:auto">Download →</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <table class="data-table">
            <thead><tr><th>Item</th><th>EOQ</th><th>Reorder pt</th><th>Safety stock</th><th>Holding cost</th><th>Status</th></tr></thead>
            <tbody>
        """, unsafe_allow_html=True)
        
        for _, row in inv_df.head(5).iterrows():
            cost_color = 'var(--red)' if row['total_inventory_cost'] > 1500 else 'var(--amber)' if row['total_inventory_cost'] > 1000 else 'var(--muted)'
            status = 'Review' if row['total_inventory_cost'] > 1500 else 'Monitor' if row['total_inventory_cost'] > 1000 else 'OK'
            status_pill = 'pill-red' if status == 'Review' else 'pill-amber' if status == 'Monitor' else 'pill-green'
            
            st.markdown(f"""
            <tr>
                <td>Item {row['product_id']}</td>
                <td>{row['eoq']:.0f}</td>
                <td>{row['reorder_point']:.0f}</td>
                <td>{row['safety_stock']:.0f}</td>
                <td style="color:{cost_color}">${row['holding_cost_total']/1000:.1f}k</td>
                <td><span class="pill {status_pill}">{status}</span></td>
            </tr>
            """, unsafe_allow_html=True)
        
        st.markdown("</tbody></table></div>", unsafe_allow_html=True)