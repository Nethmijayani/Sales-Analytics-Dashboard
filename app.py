import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ✅ Load data FIRST
@st.cache_data
def load_data():
    df = pd.read_csv("Sample - Superstore.csv", encoding="latin-1")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month_name()
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("🔍 Filters")

years = sorted(df["Year"].unique())
selected_year = st.sidebar.multiselect("Select Year", years, default=years)

regions = df["Region"].unique().tolist()
selected_region = st.sidebar.multiselect("Select Region", regions, default=regions)

categories = df["Category"].unique().tolist()
selected_category = st.sidebar.multiselect("Select Category", categories, default=categories)

# Apply filters
filtered_df = df[
    (df["Year"].isin(selected_year)) &
    (df["Region"].isin(selected_region)) &
    (df["Category"].isin(selected_category))
]

# KPIs
st.title("📊 Sales Analytics Dashboard")
st.markdown("---")

total_sales   = filtered_df["Sales"].sum()
total_profit  = filtered_df["Profit"].sum()
total_orders  = filtered_df["Order ID"].nunique()
profit_margin = (total_profit / total_sales) * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Sales",   f"${total_sales:,.0f}")
col2.metric("📈 Total Profit",  f"${total_profit:,.0f}")
col3.metric("🛒 Total Orders",  f"{total_orders:,}")
col4.metric("📊 Profit Margin", f"{profit_margin:.1f}%")

st.markdown("---")

# Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Sales Over Time")
    sales_over_time = filtered_df.groupby("Order Date")["Sales"].sum().reset_index()
    fig1 = px.line(sales_over_time, x="Order Date", y="Sales", title="Monthly Sales Trend")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🗂️ Sales by Category")
    sales_by_cat = filtered_df.groupby("Category")["Sales"].sum().reset_index()
    fig2 = px.pie(sales_by_cat, names="Category", values="Sales", title="Sales by Category")
    st.plotly_chart(fig2, use_container_width=True)

# Row 2
col3, col4 = st.columns(2)

with col3:
    st.subheader("🌍 Profit by Region")
    profit_by_region = filtered_df.groupby("Region")["Profit"].sum().reset_index()
    fig3 = px.bar(profit_by_region, x="Region", y="Profit", color="Profit", title="Profit by Region")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("🏆 Top 10 Sub-Categories")
    top_sub = (
        filtered_df.groupby("Sub-Category")["Sales"]
        .sum().reset_index()
        .sort_values("Sales", ascending=False)
        .head(10)
    )
    fig4 = px.bar(top_sub, x="Sales", y="Sub-Category", orientation="h", title="Top Sub-Categories")
    st.plotly_chart(fig4, use_container_width=True)

# Row 3
st.subheader("🔵 Sales vs Profit by Segment")
fig5 = px.scatter(
    filtered_df, x="Sales", y="Profit",
    color="Segment", size="Quantity",
    hover_data=["Product Name"],
    title="Sales vs Profit (bubble size = Quantity)"
)
st.plotly_chart(fig5, use_container_width=True)

# Row 4
st.subheader("📋 Raw Data")
st.dataframe(filtered_df, use_container_width=True)