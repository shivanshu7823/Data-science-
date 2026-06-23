import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import io

# ==========================================
# 1. PAGE INITIALIZATION & CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Sales Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CUSTOM CSS STYLING (Slate Dark Theme)
# ==========================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Set Outfit as main font and clean up margins */
    .main .block-container {
        font-family: 'Outfit', sans-serif;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    
    /* Header Container styling */
    .dashboard-header {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
        padding: 24px 32px;
        border-radius: 16px;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    .dashboard-header h1 {
        margin: 0 !important;
        color: #FFFFFF !important;
        font-size: 2.25rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
    }
    .dashboard-header p {
        margin: 8px 0 0 0 !important;
        color: #C7D2FE !important;
        font-size: 1.05rem !important;
    }
    
    /* KPI Grid layout */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }
    @media (max-width: 1200px) {
        .kpi-container {
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }
    }
    @media (max-width: 768px) {
        .kpi-container {
            grid-template-columns: repeat(1, minmax(0, 1fr));
        }
    }
    
    /* KPI Card styling with hover translation */
    .kpi-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        display: flex;
        align-items: center;
        gap: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px -3px rgba(99, 102, 241, 0.15);
        border-color: #6366F1;
    }
    
    .kpi-icon-wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 52px;
        height: 52px;
        border-radius: 10px;
        font-size: 1.6rem;
    }
    
    /* Unique colors for KPI Icons */
    .kpi-sales .kpi-icon-wrapper { background-color: rgba(99, 102, 241, 0.15); color: #818CF8; }
    .kpi-orders .kpi-icon-wrapper { background-color: rgba(16, 185, 129, 0.15); color: #34D399; }
    .kpi-customers .kpi-icon-wrapper { background-color: rgba(245, 158, 11, 0.15); color: #FBBF24; }
    .kpi-aov .kpi-icon-wrapper { background-color: rgba(139, 92, 246, 0.15); color: #A78BFA; }
    .kpi-qty .kpi-icon-wrapper { background-color: rgba(239, 68, 68, 0.15); color: #F87171; }
    
    .kpi-info {
        display: flex;
        flex-direction: column;
    }
    .kpi-label {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        color: #F8FAFC;
        font-size: 1.65rem;
        font-weight: 700;
        margin-top: 4px;
        line-height: 1;
    }
    
    /* Advanced Analytics Section */
    .insight-container {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 16px;
        margin-bottom: 28px;
    }
    @media (max-width: 1024px) {
        .insight-container {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }
    @media (max-width: 576px) {
        .insight-container {
            grid-template-columns: repeat(1, minmax(0, 1fr));
        }
    }
    
    .insight-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: border-color 0.25s ease;
    }
    .insight-card:hover {
        border-color: #4B5563;
    }
    .insight-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background-color: #6366F1;
    }
    .insight-card.accent-emerald::before { background-color: #10B981; }
    .insight-card.accent-amber::before { background-color: #F59E0B; }
    .insight-card.accent-rose::before { background-color: #EF4444; }
    
    .insight-title {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .insight-val {
        color: #F8FAFC;
        font-size: 1.25rem;
        font-weight: 700;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .insight-subtext {
        color: #64748B;
        font-size: 0.8rem;
        margin-top: 6px;
    }
    
    /* Styled visual wrappers */
    .chart-wrapper {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .chart-title {
        color: #F8FAFC;
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Tab modifications */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #0F172A;
        padding: 4px;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 10px 20px;
        color: #94A3B8;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Custom spacing */
    .stSelectbox, .stMultiSelect {
        margin-bottom: 12px;
    }
    
    /* Footer styled tag */
    .footer-credits {
        text-align: center;
        color: #475569;
        font-size: 0.85rem;
        margin-top: 40px;
        border-top: 1px solid #1E293B;
        padding-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# 3. CACHED DATA LOADING PIPELINE
# ==========================================
@st.cache_data
def get_sales_data(file_path):
    try:
        # Load excel file
        df = pd.read_excel(file_path)
        # Parse Order_Date column to Datetime
        df['Order_Date'] = pd.to_datetime(df['Order_Date'])
        # Force correct types
        df['Order_ID'] = df['Order_ID'].astype(str)
        df['Customer'] = df['Customer'].astype(str)
        df['City'] = df['City'].astype(str)
        df['Product'] = df['Product'].astype(str)
        df['Category'] = df['Category'].astype(str)
        df['Qty'] = df['Qty'].astype(int)
        df['Price'] = df['Price'].astype(float)
        df['Discount'] = df['Discount'].astype(float)
        df['Payment'] = df['Payment'].astype(str)
        df['Status'] = df['Status'].astype(str)
        df['Sales_Amount'] = df['Sales_Amount'].astype(float)
        
        # Sort values chronologically
        df = df.sort_values('Order_Date').reset_index(drop=True)
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return pd.DataFrame()

# Load the file
excel_file_path = "Final_Cleaned_No_Zero.xlsx"
df_raw = get_sales_data(excel_file_path)

if df_raw.empty:
    st.stop()

# Get bounds for dates
min_dataset_date = df_raw['Order_Date'].min().date()
max_dataset_date = df_raw['Order_Date'].max().date()

# ==========================================
# 4. SESSION STATE FOR FILTERS (For resets)
# ==========================================
# Extract unique values for multiselects
unique_cities = sorted(df_raw['City'].unique())
unique_categories = sorted(df_raw['Category'].unique())
unique_payments = sorted(df_raw['Payment'].unique())
unique_statuses = sorted(df_raw['Status'].unique())

if 'filter_cities' not in st.session_state:
    st.session_state.filter_cities = list(unique_cities)
if 'filter_categories' not in st.session_state:
    st.session_state.filter_categories = list(unique_categories)
if 'filter_payments' not in st.session_state:
    st.session_state.filter_payments = list(unique_payments)
if 'filter_statuses' not in st.session_state:
    st.session_state.filter_statuses = list(unique_statuses)
if 'filter_date' not in st.session_state:
    st.session_state.filter_date = (min_dataset_date, max_dataset_date)

def reset_all_filters():
    st.session_state.filter_cities = list(unique_cities)
    st.session_state.filter_categories = list(unique_categories)
    st.session_state.filter_payments = list(unique_payments)
    st.session_state.filter_statuses = list(unique_statuses)
    st.session_state.filter_date = (min_dataset_date, max_dataset_date)

# ==========================================
# 5. SIDEBAR FILTERS SECTION
# ==========================================
st.sidebar.title("📊 Control Center")
st.sidebar.markdown("Use the filters below to refine the dashboard data.")

# Reset Button
st.sidebar.button("🔄 Reset to Default", on_click=reset_all_filters, width="stretch")
st.sidebar.markdown("---")

# Date range picker filter
date_val = st.sidebar.date_input(
    "📆 Order Date Range",
    min_value=min_dataset_date,
    max_value=max_dataset_date,
    key='filter_date'
)

# Handle single date selections vs full ranges
if isinstance(date_val, tuple) and len(date_val) == 2:
    start_date, end_date = date_val
elif isinstance(date_val, tuple) and len(date_val) == 1:
    start_date = date_val[0]
    end_date = max_dataset_date
else:
    start_date, end_date = min_dataset_date, max_dataset_date

# Multiselect filters
selected_cities = st.sidebar.multiselect("🌆 Filter by City", options=unique_cities, key='filter_cities')
selected_categories = st.sidebar.multiselect("🏷️ Filter by Category", options=unique_categories, key='filter_categories')
selected_payments = st.sidebar.multiselect("💳 Filter by Payment Method", options=unique_payments, key='filter_payments')
selected_statuses = st.sidebar.multiselect("⚙️ Filter by Order Status", options=unique_statuses, key='filter_statuses')

# ==========================================
# 6. DATA FILTERING PIPELINE
# ==========================================
# Filter by dates
filtered_df = df_raw[
    (df_raw['Order_Date'].dt.date >= start_date) & 
    (df_raw['Order_Date'].dt.date <= end_date)
]

# Filter by selected list
if selected_cities:
    filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]
if selected_categories:
    filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories)]
if selected_payments:
    filtered_df = filtered_df[filtered_df['Payment'].isin(selected_payments)]
if selected_statuses:
    filtered_df = filtered_df[filtered_df['Status'].isin(selected_statuses)]

# Handle Empty Dataset Warning
if filtered_df.empty:
    st.markdown(
        """
        <div class="dashboard-header" style="background: linear-gradient(135deg, #7F1D1D 0%, #991B1B 50%, #B91C1C 100%);">
            <h1>No Data Matches Selections</h1>
            <p>Please adjust your sidebar filters to include data in the view.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()

# ==========================================
# 7. METRIC & KPI COMPUTATION
# ==========================================
total_sales = filtered_df['Sales_Amount'].sum()
total_orders = filtered_df['Order_ID'].nunique()
total_customers = filtered_df['Customer'].nunique()
avg_order_value = total_sales / total_orders if total_orders > 0 else 0
total_qty = filtered_df['Qty'].sum()

# ==========================================
# 8. ADVANCED ANALYTICS COMPUTATION
# ==========================================
# Best Selling Product
product_stats = filtered_df.groupby('Product').agg({'Qty': 'sum', 'Sales_Amount': 'sum'}).reset_index()
if not product_stats.empty:
    best_product_row = product_stats.sort_values('Qty', ascending=False).iloc[0]
    best_product = best_product_row['Product']
    best_product_qty = best_product_row['Qty']
    best_product_rev = best_product_row['Sales_Amount']
else:
    best_product, best_product_qty, best_product_rev = "N/A", 0, 0.0

# Highest Revenue City
city_stats = filtered_df.groupby('City')['Sales_Amount'].sum().reset_index()
if not city_stats.empty:
    top_city_row = city_stats.sort_values('Sales_Amount', ascending=False).iloc[0]
    top_city = top_city_row['City']
    top_city_rev = top_city_row['Sales_Amount']
else:
    top_city, top_city_rev = "N/A", 0.0

# Most Used Payment Method
payment_stats = filtered_df.groupby('Payment')['Order_ID'].count().reset_index().rename(columns={'Order_ID': 'Count'})
if not payment_stats.empty:
    top_payment_row = payment_stats.sort_values('Count', ascending=False).iloc[0]
    top_payment = top_payment_row['Payment']
    top_payment_count = top_payment_row['Count']
    top_payment_pct = (top_payment_count / len(filtered_df)) * 100
else:
    top_payment, top_payment_count, top_payment_pct = "N/A", 0, 0.0

# Highest Sales Category
category_stats = filtered_df.groupby('Category')['Sales_Amount'].sum().reset_index()
if not category_stats.empty:
    top_category_row = category_stats.sort_values('Sales_Amount', ascending=False).iloc[0]
    top_category = top_category_row['Category']
    top_category_rev = top_category_row['Sales_Amount']
else:
    top_category, top_category_rev = "N/A", 0.0

# ==========================================
# 9. PLOTLY CHART THEME AND STYLE FUNCTION
# ==========================================
# Theme definition
COLOR_SEQUENCE = ['#6366F1', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#06B6D4']
STATUS_COLORS_MAP = {
    'Delivered': '#10B981',
    'Pending': '#F59E0B',
    'Cancelled': '#EF4444',
    'Shipped': '#6366F1',
    'Returned': '#EC4899'
}

def format_plotly_fig(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Outfit, sans-serif', color='#94A3B8', size=12),
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#94A3B8', size=11)
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='#334155',
            linecolor='#1E293B',
            tickfont=dict(color='#94A3B8')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#334155',
            linecolor='#1E293B',
            tickfont=dict(color='#94A3B8')
        )
    )
    return fig

# ==========================================
# 10. APP STRUCTURE AND HEADER
# ==========================================
st.markdown(
    """
    <div class="dashboard-header">
        <h1>Sales Executive Intelligence Dashboard</h1>
        <p>Strategic sales execution review, performance trends, distribution analysis, and business unit metrics.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# 11. ROW 1: KPI CARDS ROW (HTML Grid)
# ==========================================
st.markdown(
    f"""
    <div class="kpi-container">
        <div class="kpi-card kpi-sales">
            <div class="kpi-icon-wrapper">💰</div>
            <div class="kpi-info">
                <span class="kpi-label">Total Revenue</span>
                <span class="kpi-value">${total_sales:,.2f}</span>
            </div>
        </div>
        <div class="kpi-card kpi-orders">
            <div class="kpi-icon-wrapper">📦</div>
            <div class="kpi-info">
                <span class="kpi-label">Total Orders</span>
                <span class="kpi-value">{total_orders:,}</span>
            </div>
        </div>
        <div class="kpi-card kpi-customers">
            <div class="kpi-icon-wrapper">👥</div>
            <div class="kpi-info">
                <span class="kpi-label">Total Customers</span>
                <span class="kpi-value">{total_customers:,}</span>
            </div>
        </div>
        <div class="kpi-card kpi-aov">
            <div class="kpi-icon-wrapper">📈</div>
            <div class="kpi-info">
                <span class="kpi-label">Avg Order Value</span>
                <span class="kpi-value">${avg_order_value:,.2f}</span>
            </div>
        </div>
        <div class="kpi-card kpi-qty">
            <div class="kpi-icon-wrapper">🛍️</div>
            <div class="kpi-info">
                <span class="kpi-label">Quantity Sold</span>
                <span class="kpi-value">{total_qty:,}</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# 12. ADVANCED ANALYTICS INSIGHTS ROW
# ==========================================
st.markdown(
    f"""
    <div class="insight-container">
        <div class="insight-card">
            <div class="insight-title">🏆 Best Selling Product</div>
            <div class="insight-val" title="{best_product}">{best_product}</div>
            <div class="insight-subtext">Units: <b>{best_product_qty:,}</b> | Rev: <b>${best_product_rev:,.2f}</b></div>
        </div>
        <div class="insight-card accent-emerald">
            <div class="insight-title">🌆 Top Revenue City</div>
            <div class="insight-val" title="{top_city}">{top_city}</div>
            <div class="insight-subtext">Total Sales: <b>${top_city_rev:,.2f}</b></div>
        </div>
        <div class="insight-card accent-amber">
            <div class="insight-title">💳 Preferred Payment</div>
            <div class="insight-val" title="{top_payment}">{top_payment}</div>
            <div class="insight-subtext">Orders: <b>{top_payment_count:,} ({top_payment_pct:.1f}%)</b></div>
        </div>
        <div class="insight-card accent-rose">
            <div class="insight-title">🏷️ Top Category</div>
            <div class="insight-val" title="{top_category}">{top_category}</div>
            <div class="insight-subtext">Total Sales: <b>${top_category_rev:,.2f}</b></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# 13. TABS CREATION FOR SECTIONING
# ==========================================
tab_overview, tab_products_customers, tab_data = st.tabs([
    "📈 Performance Overview", 
    "🛍️ Product & Customer Analytics", 
    "🔍 Detailed Data Viewer"
])

# ==========================================
# TAB 1: PERFORMANCE OVERVIEW
# ==========================================
with tab_overview:
    # --- ROW 2: Trend Charts ---
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown(
            """
            <div class="chart-wrapper">
                <div class="chart-title">📈 Sales Trend Over Time</div>
            """,
            unsafe_allow_html=True
        )
        
        # Granularity Radio selector inside the container
        granularity = st.radio(
            "Select Trend Interval:",
            options=["Daily", "Weekly", "Monthly"],
            horizontal=True,
            index=2, # Default to Monthly
            label_visibility="collapsed"
        )
        
        # Group according to granularity
        if granularity == "Daily":
            trend_df = filtered_df.groupby('Order_Date')['Sales_Amount'].sum().reset_index()
            x_col = 'Order_Date'
            hover_format = "<b>Date:</b> %{x|%d %b %Y}<br><b>Sales:</b> $%{y:,.2f}"
        elif granularity == "Weekly":
            # Group by weekly starting monday
            trend_df = filtered_df.groupby(pd.Grouper(key='Order_Date', freq='W-MON'))['Sales_Amount'].sum().reset_index()
            x_col = 'Order_Date'
            hover_format = "<b>Week of:</b> %{x|%d %b %Y}<br><b>Sales:</b> $%{y:,.2f}"
        else: # Monthly
            trend_df = filtered_df.copy()
            trend_df['Year_Month'] = trend_df['Order_Date'].dt.to_period('M').dt.to_timestamp()
            trend_df = trend_df.groupby('Year_Month')['Sales_Amount'].sum().reset_index()
            x_col = 'Year_Month'
            hover_format = "<b>Month:</b> %{x|%B %Y}<br><b>Sales:</b> $%{y:,.2f}"
            
        fig_trend = px.area(
            trend_df,
            x=x_col,
            y='Sales_Amount',
            color_discrete_sequence=['#6366F1']
        )
        fig_trend.update_traces(
            line=dict(width=3, shape='spline'),
            fillcolor='rgba(99, 102, 241, 0.1)',
            hovertemplate=hover_format
        )
        fig_trend = format_plotly_fig(fig_trend)
        fig_trend.update_layout(height=320)
        
        st.plotly_chart(fig_trend, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown(
            """
            <div class="chart-wrapper">
                <div class="chart-title">📅 Monthly Sales Volume</div>
            """,
            unsafe_allow_html=True
        )
        
        monthly_df = filtered_df.copy()
        # Create Month-Year column sorted chronologically
        monthly_df['Month_TS'] = monthly_df['Order_Date'].dt.to_period('M').dt.to_timestamp()
        monthly_sales = monthly_df.groupby('Month_TS')['Sales_Amount'].sum().reset_index()
        monthly_sales['Month'] = monthly_sales['Month_TS'].dt.strftime('%b %Y')
        
        fig_monthly = px.bar(
            monthly_sales,
            x='Month',
            y='Sales_Amount',
            color='Sales_Amount',
            color_continuous_scale=['#C7D2FE', '#4F46E5']
        )
        fig_monthly.update_traces(
            hovertemplate="<b>Month:</b> %{x}<br><b>Sales:</b> $%{y:,.2f}",
            marker_line_width=0
        )
        fig_monthly = format_plotly_fig(fig_monthly)
        fig_monthly.update_layout(height=320, coloraxis_showscale=False)
        
        st.plotly_chart(fig_monthly, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ROW 3: Category & City ---
    col3, col4 = st.columns([1, 1])
    
    with col3:
        st.markdown(
            """
            <div class="chart-wrapper">
                <div class="chart-title">🏷️ Category-wise Revenue</div>
            """,
            unsafe_allow_html=True
        )
        
        cat_rev = filtered_df.groupby('Category')['Sales_Amount'].sum().reset_index().sort_values('Sales_Amount', ascending=True)
        fig_cat = px.bar(
            cat_rev,
            y='Category',
            x='Sales_Amount',
            orientation='h',
            color='Sales_Amount',
            color_continuous_scale='blues'
        )
        fig_cat.update_traces(
            hovertemplate="<b>Category:</b> %{y}<br><b>Sales:</b> $%{x:,.2f}",
            marker_line_width=0
        )
        fig_cat = format_plotly_fig(fig_cat)
        fig_cat.update_layout(height=280, coloraxis_showscale=False, yaxis=dict(showgrid=False))
        
        st.plotly_chart(fig_cat, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col4:
        st.markdown(
            """
            <div class="chart-wrapper">
                <div class="chart-title">🌆 City-wise Revenue</div>
            """,
            unsafe_allow_html=True
        )
        
        city_rev = filtered_df.groupby('City')['Sales_Amount'].sum().reset_index().sort_values('Sales_Amount', ascending=False)
        fig_city = px.bar(
            city_rev,
            x='City',
            y='Sales_Amount',
            color='Sales_Amount',
            color_continuous_scale='purples'
        )
        fig_city.update_traces(
            hovertemplate="<b>City:</b> %{x}<br><b>Sales:</b> $%{y:,.2f}",
            marker_line_width=0
        )
        fig_city = format_plotly_fig(fig_city)
        fig_city.update_layout(height=280, coloraxis_showscale=False, xaxis=dict(showgrid=False))
        
        st.plotly_chart(fig_city, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ROW 4: Payment Distribution & Status Distribution ---
    col5, col6 = st.columns([1, 1])
    
    with col5:
        st.markdown(
            """
            <div class="chart-wrapper">
                <div class="chart-title">💳 Payment Method Distribution</div>
            """,
            unsafe_allow_html=True
        )
        
        pay_df = filtered_df.groupby('Payment')['Sales_Amount'].sum().reset_index()
        fig_pay = px.pie(
            pay_df,
            values='Sales_Amount',
            names='Payment',
            color_discrete_sequence=COLOR_SEQUENCE,
            hole=0.45
        )
        fig_pay.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate="<b>Payment:</b> %{label}<br><b>Sales:</b> $%{value:,.2f}<br><b>Share:</b> %{percent:.1%}"
        )
        fig_pay = format_plotly_fig(fig_pay)
        fig_pay.update_layout(height=280, margin=dict(l=20, r=20, t=10, b=10))
        
        st.plotly_chart(fig_pay, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col6:
        st.markdown(
            """
            <div class="chart-wrapper">
                <div class="chart-title">⚙️ Order Status Share</div>
            """,
            unsafe_allow_html=True
        )
        
        status_df = filtered_df.groupby('Status')['Order_ID'].count().reset_index().rename(columns={'Order_ID': 'Count'})
        
        # Build color mapping based on available status
        present_statuses = status_df['Status'].unique()
        color_map = {st: STATUS_COLORS_MAP.get(st, '#64748B') for st in present_statuses}
        
        fig_status = px.pie(
            status_df,
            values='Count',
            names='Status',
            color='Status',
            color_discrete_map=color_map,
            hole=0.55
        )
        fig_status.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate="<b>Status:</b> %{label}<br><b>Order Count:</b> %{value}<br><b>Share:</b> %{percent:.1%}"
        )
        fig_status = format_plotly_fig(fig_status)
        fig_status.update_layout(height=280, margin=dict(l=20, r=20, t=10, b=10))
        
        st.plotly_chart(fig_status, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 2: PRODUCT & CUSTOMER ANALYTICS
# ==========================================
with tab_products_customers:
    col_prod, col_cust = st.columns([1, 1])
    
    with col_prod:
        st.markdown(
            """
            <div class="chart-wrapper">
                <div class="chart-title">🛍️ Top 10 Products by Sales Volume</div>
            """,
            unsafe_allow_html=True
        )
        
        top10_prod = filtered_df.groupby('Product')['Sales_Amount'].sum().reset_index().sort_values('Sales_Amount', ascending=True).tail(10)
        fig_top_prod = px.bar(
            top10_prod,
            y='Product',
            x='Sales_Amount',
            orientation='h',
            color='Sales_Amount',
            color_continuous_scale='tealgrn'
        )
        fig_top_prod.update_traces(
            hovertemplate="<b>Product:</b> %{y}<br><b>Total Revenue:</b> $%{x:,.2f}",
            marker_line_width=0
        )
        fig_top_prod = format_plotly_fig(fig_top_prod)
        fig_top_prod.update_layout(height=450, coloraxis_showscale=False, yaxis=dict(showgrid=False))
        
        st.plotly_chart(fig_top_prod, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_cust:
        st.markdown(
            """
            <div class="chart-wrapper">
                <div class="chart-title">👤 Top 10 Customers by Revenue</div>
            """,
            unsafe_allow_html=True
        )
        
        top10_cust = filtered_df.groupby('Customer')['Sales_Amount'].sum().reset_index().sort_values('Sales_Amount', ascending=True).tail(10)
        fig_top_cust = px.bar(
            top10_cust,
            y='Customer',
            x='Sales_Amount',
            orientation='h',
            color='Sales_Amount',
            color_continuous_scale='blugrn'
        )
        fig_top_cust.update_traces(
            hovertemplate="<b>Customer:</b> %{y}<br><b>Total Revenue:</b> $%{x:,.2f}",
            marker_line_width=0
        )
        fig_top_cust = format_plotly_fig(fig_top_cust)
        fig_top_cust.update_layout(height=450, coloraxis_showscale=False, yaxis=dict(showgrid=False))
        
        st.plotly_chart(fig_top_cust, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 3: DETAILED DATA VIEWER
# ==========================================
with tab_data:
    st.markdown(
        """
        <div class="chart-wrapper">
            <div class="chart-title">🔍 Searchable Transaction Log</div>
        """,
        unsafe_allow_html=True
    )
    
    # Grid search filters
    search_col1, search_col2 = st.columns([2, 1])
    with search_col1:
        search_query = st.text_input("🔍 Search by Customer Name or Product Name:", value="", placeholder="Type to filter...")
    with search_col2:
        # Download Filtered Data Button
        csv_buffer = io.BytesIO()
        # Format dates for export
        export_df = filtered_df.copy()
        export_df['Order_Date'] = export_df['Order_Date'].dt.strftime('%Y-%m-%d')
        
        export_df.to_csv(csv_buffer, index=False, encoding='utf-8')
        
        st.download_button(
            label="📥 Download Filtered CSV",
            data=csv_buffer.getvalue(),
            file_name=f"filtered_sales_data_{datetime.date.today()}.csv",
            mime="text/csv",
            width="stretch"
        )
    
    # Process text search query if entered
    view_df = filtered_df.copy()
    if search_query:
        view_df = view_df[
            view_df['Customer'].str.contains(search_query, case=False, na=False) |
            view_df['Product'].str.contains(search_query, case=False, na=False)
        ]
        
    # Format and present DataFrame
    formatted_view_df = view_df.copy()
    formatted_view_df['Order_Date'] = formatted_view_df['Order_Date'].dt.strftime('%d %b %Y')
    
    st.dataframe(
        formatted_view_df,
        column_config={
            "Order_ID": "Order ID",
            "Order_Date": "Order Date",
            "Customer": "Customer",
            "City": "City",
            "Product": "Product",
            "Category": "Category",
            "Qty": st.column_config.NumberColumn("Qty", format="%d"),
            "Price": st.column_config.NumberColumn("Price", format="$%d"),
            "Discount": st.column_config.NumberColumn("Discount", format="%d%%"),
            "Payment": "Payment",
            "Status": "Status",
            "Sales_Amount": st.column_config.NumberColumn("Sales Amount", format="$%.2f")
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Total row counts matching filters
    st.caption(f"Showing {len(view_df)} transactions matching current filters and search query.")
    st.markdown("</div>", unsafe_allow_html=True)

# Credits and footer
st.markdown(
    """
    <div class="footer-credits">
        Sales Executive Intelligence Dashboard • Designed with Python & Streamlit • Portfolio Showcase Project
    </div>
    """,
    unsafe_allow_html=True
)!