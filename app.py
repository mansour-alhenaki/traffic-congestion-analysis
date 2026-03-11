import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Traffic Congestion Dashboard", layout="wide")

df = pd.read_csv("traffic_index.csv")
df["Datetime"] = pd.to_datetime(df["Datetime"])
df["Hour"] = df["Datetime"].dt.hour

st.sidebar.title("Dashboard Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Overview", "Traffic Analysis", "Relationship Analysis", "Data Explorer"]
)

selected_cities = st.sidebar.multiselect(
    "Select city or cities",
    options=sorted(df["City"].dropna().unique()),
    default=sorted(df["City"].dropna().unique())
)

filtered_df = df[df["City"].isin(selected_cities)].copy()

if filtered_df.empty:
    st.warning("No data available for the selected cities.")
    st.stop()

st.title("Traffic Congestion Analysis Dashboard")
st.markdown("Explore traffic congestion patterns across cities using interactive sections.")

if page == "Overview":
    st.header("Overview")

    avg_traffic = filtered_df["TrafficIndexLive"].mean()
    highest_city = filtered_df.groupby("City")["TrafficIndexLive"].mean().idxmax()
    avg_travel_time = filtered_df["TravelTimeLive"].mean()
    total_jams = filtered_df["JamsCount"].sum()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Average Traffic Index", f"{avg_traffic:.2f}")
    kpi2.metric("Highest Traffic City", highest_city)
    kpi3.metric("Average Travel Time", f"{avg_travel_time:.2f}")
    kpi4.metric("Total Jams Count", f"{int(total_jams):,}")

    st.subheader("Average Traffic by City")
    city_traffic = filtered_df.groupby("City")["TrafficIndexLive"].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    city_traffic.plot(kind="bar", ax=ax)
    ax.set_xlabel("City")
    ax.set_ylabel("Average Traffic Index")
    ax.set_title("Average Traffic by City")
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif page == "Traffic Analysis":
    st.header("Traffic Analysis")

    chart_type = st.selectbox(
        "Select chart type for hourly traffic",
        ["Line Chart", "Bar Chart"]
    )

    st.subheader("Traffic by Hour")
    hourly_traffic = filtered_df.groupby("Hour")["TrafficIndexLive"].mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    if chart_type == "Line Chart":
        hourly_traffic.plot(ax=ax)
    else:
        hourly_traffic.plot(kind="bar", ax=ax)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Average Traffic Index")
    ax.set_title("Traffic Pattern by Hour")
    st.pyplot(fig)

    st.subheader("Traffic Index Distribution")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(filtered_df["TrafficIndexLive"], bins=30)
    ax.set_xlabel("Traffic Index")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution of Traffic Index")
    st.pyplot(fig)

elif page == "Relationship Analysis":
    st.header("Relationship Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Traffic Index vs Travel Time")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(filtered_df["TrafficIndexLive"], filtered_df["TravelTimeLive"])
        ax.set_xlabel("Traffic Index")
        ax.set_ylabel("Travel Time")
        ax.set_title("Traffic Index vs Travel Time")
        st.pyplot(fig)

    with col2:
        st.subheader("Traffic Index vs Jams Count")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(filtered_df["JamsCount"], filtered_df["TrafficIndexLive"])
        ax.set_xlabel("Jams Count")
        ax.set_ylabel("Traffic Index")
        ax.set_title("Traffic Index vs Jams Count")
        st.pyplot(fig)

    st.subheader("Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(filtered_df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
    ax.set_title("Correlation Between Numerical Features")
    st.pyplot(fig)

elif page == "Data Explorer":
    st.header("Data Explorer")

    st.subheader("Dataset Preview")
    st.dataframe(filtered_df.head(20), use_container_width=True)

    st.subheader("Column Data Types")
    info_df = pd.DataFrame({
        "Column": filtered_df.columns,
        "Data Type": filtered_df.dtypes.astype(str).values
    })
    st.dataframe(info_df, use_container_width=True)

    st.subheader("Summary Statistics")
    st.dataframe(filtered_df.describe(), use_container_width=True)