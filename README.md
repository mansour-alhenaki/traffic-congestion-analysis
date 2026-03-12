# Traffic Congestion Analysis Dashboard

This project analyzes traffic congestion patterns across multiple cities using traffic data.  
An interactive dashboard was built using **Streamlit** to explore traffic indicators, congestion levels, and travel time patterns.

## Live Demo
https://traffic-congestion-analysis-5hefzxlbp6mtfybjogvebr.streamlit.app/

## Dataset Source
Kaggle Dataset:  
https://www.kaggle.com/datasets/majedalhulayel/traffic-index-in-saudi-arabia-and-middle-east

## Project Objectives
- Identify cities with the highest traffic congestion
- Analyze traffic congestion by hour of the day
- Explore relationships between traffic indicators
- Measure extra travel time caused by traffic congestion

## Tools Used
- Python
- Pandas
- Matplotlib
- Seaborn
- Streamlit
- Jupyter Notebook

## Dataset Description

The dataset contains traffic indicators across multiple cities, including:

- City
- TrafficIndexLive
- TrafficIndexWeekAgo
- JamsCount
- JamsLength
- TravelTimeLive
- TravelTimeHistoric

## Analysis Performed

The analysis explores:

- Traffic congestion by city
- Traffic congestion patterns by hour
- Extra travel time caused by congestion
- Relationships between traffic indicators
- Correlation between traffic metrics

## Project Files

- `app.py` → Streamlit dashboard application  
- `traffic_congestion_analysis.ipynb` → Data analysis notebook  
- `traffic_index.csv` → Dataset used for the analysis  
- `requirements.txt` → Python dependencies

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
