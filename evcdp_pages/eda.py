import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

# Function to load data
@st.cache_data
def load_data():
    data_file = "synthetic_ev_session_varied_weekdays.csv" 
    data = pd.read_csv(data_file)
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    data['Day'] = data['Timestamp'].dt.date  # Add 'Day' column
    data['Year'] = data['Timestamp'].dt.year
    data['Month'] = data['Timestamp'].dt.month
    data['DayOfMonth'] = data['Timestamp'].dt.day
    data['Hour'] = data['Timestamp'].dt.hour
    data['Weekday'] = data['Timestamp'].dt.weekday  # 0 = Monday, 6 = Sunday
    # Map numeric weekday values to their corresponding names
    weekday_map = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    data['Weekday'] = data['Weekday'].map(weekday_map)
    return data

# Function to filter data
def filter_data(data, start_date, end_date):
    filtered_data = data.copy()
    
    # Filter by timestamp
    if start_date and end_date:
        filtered_data = filtered_data[
            (filtered_data['Timestamp'] >= pd.to_datetime(start_date)) & 
            (filtered_data['Timestamp'] <= pd.to_datetime(end_date))
        ]
    return filtered_data

# EDA Page
def render():
    st.title("Exploratory Data Analysis (EDA) for EV Charging Stations")

    # Load data
    data = load_data()

    # Filters on the main page
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date", value=data['Timestamp'].min().date())
    with col2:
        end_date = st.date_input("End Date", value=data['Timestamp'].max().date())

    # Filter data based on selected dates
    filtered_data = filter_data(data, start_date, end_date)

    # Sum of Energy Delivered by Day
    #st.subheader("Total Energy Delivered by Day")
    filtered_data['Day of Month'] = filtered_data['Timestamp'].dt.day  # Extract day of the month (1 to 31)
    daily_energy = filtered_data.groupby('Day of Month')['Energy Delivered (kWh)'].sum().reset_index()

    fig_daily_energy = px.line(
        daily_energy,
        x='Day of Month',
        y='Energy Delivered (kWh)',
        title="Energy Delivered by Day",
        labels={'Day of Month': 'Day of the Month'}
    )
    st.plotly_chart(fig_daily_energy, use_container_width=True)

    # Insight for daily energy
    st.markdown(
        "**Insight:** The energy demand exhibits a cyclic pattern where the cycle repeats every 7 days."
    )

    st.markdown("---")

    # Sum of Energy Delivered by Weekday
    #st.subheader("Total Energy Delivered by Weekday")
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    filtered_data['Weekday'] = pd.Categorical(filtered_data['Weekday'], categories=weekday_order, ordered=True)
    weekday_energy = filtered_data.groupby('Weekday')['Energy Delivered (kWh)'].sum().reset_index()

    fig_weekday_energy = px.bar(
        weekday_energy,
        x='Weekday',
        y='Energy Delivered (kWh)',
        title="Energy Delivered by Weekday",
        labels={'Energy Delivered (kWh)': 'Total Energy Delivered (kWh)', 'Weekday': 'Day of the Week'}
    )
    st.plotly_chart(fig_weekday_energy, use_container_width=True)

    # Insight for weekday energy
    st.markdown(
        "**Insight:** Weekends show lower energy demand compared to weekdays."
    )

    st.markdown("---")

    # Sum of Energy Delivered by Charging Station
    #st.subheader("Sum of Energy Delivered by Charging Station")
    station_energy = filtered_data.groupby('Station')['Energy Delivered (kWh)'].sum().reset_index()
    station_energy = station_energy.sort_values(by='Energy Delivered (kWh)', ascending=True)

    fig_station_energy = px.bar(
        station_energy,
        x='Energy Delivered (kWh)',
        y='Station',
        title="Energy Delivered by Charging Station",
        labels={'Energy Delivered (kWh)': 'Total Energy Delivered (kWh)', 'Station': 'Charging Station'},
        orientation='h'
    )
    st.plotly_chart(fig_station_energy, use_container_width=True)

    # Insight for charging station energy
    st.markdown(
        "**Insight:** The station 'Shell LDP D' Alpinia' has the highest energy demand."
    )

    st.markdown("---")

    # Monthly Charging Events Count
    #st.subheader("Monthly Charging Events Count for 2023 and 2024")
    filtered_data['Year'] = filtered_data['Timestamp'].dt.year
    filtered_data['Month'] = filtered_data['Timestamp'].dt.month_name()
    filtered_years = filtered_data[filtered_data['Year'].isin([2023, 2024])]

    monthly_event_counts = (
        filtered_years.groupby(['Year', 'Month'])
        .size()
        .reset_index(name='Count')
    )
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    monthly_event_counts['Month'] = pd.Categorical(
        monthly_event_counts['Month'], categories=month_order, ordered=True
    )
    pivot_data = monthly_event_counts.pivot(index='Month', columns='Year', values='Count').fillna(0)

    fig, ax = plt.subplots(figsize=(12, 6))
    pivot_data.plot(kind='bar', ax=ax, width=0.8, edgecolor='black')
    ax.set_title('Monthly Charging Events Count for 2023 and 2024', fontsize=14)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Number of Charging Events', fontsize=12)
    ax.set_xticklabels(
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        rotation=0,
        fontsize=10
    )
    ax.legend(title='Year', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    # Insight for monthly charging events
    st.markdown(
        "**Insight:** Higher charging counts are observed in March, May, June, and December."
    )

