import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Traffic Congestion Dashboard",
    page_icon="🚦",
    layout="wide"
)

sns.set_theme(style="whitegrid")

@st.cache_data
def load_data():
    df = pd.read_csv("traffic_index.csv")
    df["Datetime"] = pd.to_datetime(df["Datetime"])
    df["Hour"] = df["Datetime"].dt.hour
    return df

df = load_data()

required_columns = [
    "City",
    "Datetime",
    "TrafficIndexLive",
    "TravelTimeLive",
    "JamsCount"
]

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"Missing required columns: {', '.join(missing_columns)}")
    st.stop()

st.sidebar.title("Traffic Dashboard")

page = st.sidebar.radio(
    "Choose Section",
    ["Overview", "Traffic Patterns", "Relationship Analysis", "Data Explorer"]
)

selected_cities = st.sidebar.multiselect(
    "Select City or Cities",
    options=sorted(df["City"].dropna().unique()),
    default=sorted(df["City"].dropna().unique())
)

filtered_df = df[df["City"].isin(selected_cities)].copy()

if filtered_df.empty:
    st.warning("No data available for the selected cities.")
    st.stop()

if page == "Traffic Patterns":
    chart_type = st.sidebar.radio(
        "Hourly Traffic Chart Type",
        ["Line Chart", "Bar Chart"]
    )
else:
    chart_type = "Line Chart"

st.title("Traffic Congestion Analysis Dashboard")
st.markdown("Explore traffic congestion patterns across selected cities using interactive visual analysis.")

avg_traffic = filtered_df["TrafficIndexLive"].mean()
avg_travel_time = filtered_df["TravelTimeLive"].mean()
total_jams = filtered_df["JamsCount"].sum()
highest_city = filtered_df.groupby("City")["TrafficIndexLive"].mean().idxmax()
highest_city_value = filtered_df.groupby("City")["TrafficIndexLive"].mean().max()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Average Traffic Index", f"{avg_traffic:.2f}")
kpi2.metric("Average Travel Time", f"{avg_travel_time:.2f}")
kpi3.metric("Total Jams Count", f"{int(total_jams):,}")
kpi4.metric("Most Congested City", highest_city)

st.markdown("---")

if page == "Overview":
    st.header("Overview")

    col1, col2 = st.columns([1.7, 1])

    with col1:
        st.subheader("Average Traffic by City")
        city_traffic = (
            filtered_df.groupby("City")["TrafficIndexLive"]
            .mean()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(
            x=city_traffic.index,
            y=city_traffic.values,
            hue=city_traffic.index,
            palette="viridis",
            legend=False,
            ax=ax
        )
        ax.set_xlabel("City")
        ax.set_ylabel("Average Traffic Index")
        ax.set_title("Average Traffic Index by City")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with col2:
        st.subheader("Key Insights")
        st.info(
            f"The highest average traffic level appears in {highest_city} "
            f"with an average traffic index of {highest_city_value:.2f}."
        )

        jams_by_city = (
            filtered_df.groupby("City")["JamsCount"]
            .sum()
            .sort_values(ascending=False)
        )

        if not jams_by_city.empty:
            st.success(
                f"The highest total jams count appears in {jams_by_city.index[0]} "
                f"with {int(jams_by_city.iloc[0]):,} jams."
            )

        st.write(f"Number of selected cities: {len(selected_cities)}")

    st.subheader("Traffic Index Distribution")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(
        filtered_df["TrafficIndexLive"],
        bins=30,
        kde=True,
        color="#4dabf7",
        ax=ax
    )
    ax.set_xlabel("Traffic Index")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution of Traffic Index")
    st.pyplot(fig)

elif page == "Traffic Patterns":
    st.header("Traffic Patterns")

    st.subheader("Traffic by Hour")
    hourly_traffic = (
        filtered_df.groupby("Hour")["TrafficIndexLive"]
        .mean()
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    if chart_type == "Line Chart":
        sns.lineplot(
            x=hourly_traffic.index,
            y=hourly_traffic.values,
            marker="o",
            linewidth=3,
            color="#ff6b6b",
            ax=ax
        )
    else:
        sns.barplot(
            x=hourly_traffic.index,
            y=hourly_traffic.values,
            hue=hourly_traffic.index,
            palette="magma",
            legend=False,
            ax=ax
        )

    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Average Traffic Index")
    ax.set_title("Traffic Pattern by Hour")
    st.pyplot(fig)

    peak_hour = hourly_traffic.idxmax()
    peak_value = hourly_traffic.max()

    st.info(
        f"Peak traffic appears around {peak_hour}:00 with an average traffic index of {peak_value:.2f}."
    )

    st.subheader("Average Travel Time by City")
    travel_by_city = (
        filtered_df.groupby("City")["TravelTimeLive"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        x=travel_by_city.index,
        y=travel_by_city.values,
        hue=travel_by_city.index,
        palette="cubehelix",
        legend=False,
        ax=ax
    )
    ax.set_xlabel("City")
    ax.set_ylabel("Average Travel Time")
    ax.set_title("Average Travel Time by City")
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif page == "Relationship Analysis":
    st.header("Relationship Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Traffic Index vs Travel Time")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(
            data=filtered_df,
            x="TrafficIndexLive",
            y="TravelTimeLive",
            color="#845ef7",
            alpha=0.7,
            ax=ax
        )
        ax.set_xlabel("Traffic Index")
        ax.set_ylabel("Travel Time")
        ax.set_title("Traffic Index vs Travel Time")
        st.pyplot(fig)

    with col2:
        st.subheader("Traffic Index vs Jams Count")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(
            data=filtered_df,
            x="JamsCount",
            y="TrafficIndexLive",
            color="#20c997",
            alpha=0.7,
            ax=ax
        )
        ax.set_xlabel("Jams Count")
        ax.set_ylabel("Traffic Index")
        ax.set_title("Traffic Index vs Jams Count")
        st.pyplot(fig)

    st.subheader("Correlation Heatmap")
    numeric_df = filtered_df.select_dtypes(include="number")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        ax=ax
    )
    ax.set_title("Correlation Between Numerical Features")
    st.pyplot(fig)

    st.caption("This section helps identify whether traffic congestion is associated with longer travel times or more traffic jams.")

elif page == "Data Explorer":
    st.header("Data Explorer")

    st.subheader("Dataset Preview")
    st.dataframe(filtered_df.head(20), use_container_width=True)

    with st.expander("Show Column Data Types"):
        info_df = pd.DataFrame({
            "Column": filtered_df.columns,
            "Data Type": filtered_df.dtypes.astype(str).values
        })
        st.dataframe(info_df, use_container_width=True)

    with st.expander("Show Summary Statistics"):
        st.dataframe(filtered_df.describe(), use_container_width=True)

    with st.expander("Show Missing Values"):
        missing_df = pd.DataFrame({
            "Column": filtered_df.columns,
            "Missing Values": filtered_df.isnull().sum().values
        })
        st.dataframe(missing_df, use_container_width=True)

st.markdown("---")
st.caption("Built with Streamlit for traffic congestion analysis.")
