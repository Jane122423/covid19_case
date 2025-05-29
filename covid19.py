import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ Must be the first Streamlit command
st.set_page_config(page_title="COVID-19 Case (PH)", layout="wide")

# ✅ Load the data
df = pd.read_csv("covid19_case.csv")
df["date_announced"] = pd.to_datetime(df["date_announced"], errors="coerce")
df = df.dropna(subset=["region", "province", "status", "date_announced"])

# ======================
# 💡 Sidebar Filters
# ======================
st.sidebar.header("🧪 Filters")

# Status dropdown
status = st.sidebar.selectbox(
    "Select Case Status",
    sorted(df["status"].unique()),
    index=0
)

# Region dropdown
regions = ["All Regions"] + sorted(df["region"].unique())
region = st.sidebar.selectbox("Select Region", regions)

# Province dropdown based on region
if region == "All Regions":
    provinces = ["All"] + sorted(df["province"].unique())
else:
    provinces = ["All"] + sorted(df[df["region"] == region]["province"].unique())

province = st.sidebar.selectbox("Select Province", provinces)

# Date range
min_date = df["date_announced"].min().date()
max_date = df["date_announced"].max().date()
start_date, end_date = st.sidebar.date_input(
    "Select Date Range", [min_date, max_date],
    min_value=min_date, max_value=max_date
)

# ======================
# 🎯 Page Header
# ======================
st.title("🦠 COVID-19 Case Tracker")
st.markdown("#### Philippines COVID-19 Case Visualization Tool")
st.markdown("""
<div style='color:#34495e; text-align: center; font-size: 16px'>
Use the filters on the left to explore COVID-19 case counts across different regions, provinces, and time ranges.<br>
This tool helps visualize the impact based on case status (e.g., Died, Recovered).
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ======================
# 📊 Data Filtering
# ======================
mask = (
    (df["status"] == status) &
    (df["date_announced"].dt.date >= start_date) &
    (df["date_announced"].dt.date <= end_date)
)

if region != "All Regions":
    mask &= df["region"] == region

if province != "All":
    mask &= df["province"] == province

filtered_df = df[mask]

# ======================
# 📈 Chart & Summary
# ======================
if not filtered_df.empty:
    summary = filtered_df["province"].value_counts().reset_index()
    summary.columns = ["Province", "Count"]
    summary = summary.sort_values(by="Count", ascending=False)

    # Bar chart
    fig = px.bar(
        summary, x="Province", y="Count", color="Province",
        title=f"{status} Cases in {'All Regions' if region == 'All Regions' else region}",
        labels={"Count": "Number of Cases"}
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#f9f9f9"
    )

    # Display chart and summary
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"### 🧾 Total {status} Cases: **{summary['Count'].sum()}**")
else:
    st.warning("No data found for the selected filters.")