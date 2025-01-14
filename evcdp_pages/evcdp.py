import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
from keras.metrics import MeanSquaredError
import tensorflow as tf
import plotly.express as px
import plotly.graph_objects as go

# Load your pre-trained LSTM model
@st.cache_resource
def load_best_model():
    # Explicitly map the 'mse' loss function
    return load_model("cnnlstm_ev_model.h5", custom_objects={"MeanSquaredError": MeanSquaredError(), "mse": mse_loss()})
    # return load_model("cnnlstm_ev_model.h5", custom_objects={"mse": MeanSquaredError()})

# Main function for the EVCDP page
def render():
    st.title("🔋 EV Charging Demand Prediction")
    
    # Upload CSV file
    uploaded_file = st.file_uploader("Upload Historical Charging Session CSV", type=["csv"])
    
    if uploaded_file is not None:
        # Load the data
        ev_session_df = pd.read_csv(uploaded_file)
        
        # Preprocess the data
        #st.write("### Data Preprocessing")
        ev_session_df['Timestamp'] = pd.to_datetime(ev_session_df['Timestamp'])
        ev_session_df = ev_session_df.sort_values(by='Timestamp')
        
        # Aggregate the data
        ev_session_df = ev_session_df.set_index('Timestamp').groupby(
            ['Station', pd.Grouper(freq='D')]
        ).agg({
            'Energy Delivered (kWh)': 'sum',
            'Duration (mins)': 'sum',
            'Latitude': 'first',
            'Longitude': 'first'
        }).reset_index()
        
        # st.write("Aggregated Data:")
        # st.dataframe(ev_session_df)
        
        # Normalize the data
        scaler = MinMaxScaler()
        ev_session_df[['Duration (mins)', 'Energy Delivered (kWh)']] = scaler.fit_transform(
            ev_session_df[['Duration (mins)', 'Energy Delivered (kWh)']]
        )
        
        # Pivot the data for time series
        temporal_data = ev_session_df.pivot(
            index='Timestamp',
            columns='Station',
            values='Energy Delivered (kWh)'
        ).fillna(0)
        
        # # Display pivoted data
        # st.write("Pivoted Time-Series Data:")
        # st.dataframe(temporal_data)
        
        # Ensure data has enough historical days
        if len(temporal_data) < 7:
            st.warning("Not enough historical data for the last 7 days.")
            return
        
        # Extract the past 7 days
        last_7_days = temporal_data.tail(7).values
        input_data = last_7_days.reshape(1, 7, last_7_days.shape[1])
        
        # Load the best model
        best_model = load_best_model()
        
        # Make predictions
        predicted_normalized = best_model.predict(input_data)[0]
        
        # Denormalize predictions
        energy_min = scaler.data_min_[1]  # 'Energy Delivered (kWh)' min
        energy_max = scaler.data_max_[1]  # 'Energy Delivered (kWh)' max
        predicted_values = predicted_normalized * (energy_max - energy_min) + energy_min
        
        # Map station names to predicted values
        station_names = temporal_data.columns
        predicted_energy = dict(zip(station_names, predicted_values))
        
        # Create prediction dataframe
        prediction_df = pd.DataFrame(list(predicted_energy.items()), 
                                   columns=["Station", "Predicted Energy (kWh)"])
        prediction_df = prediction_df.sort_values(by="Predicted Energy (kWh)", ascending=False)
        
        # Reset the index and drop it to avoid displaying the index
        prediction_df = prediction_df.reset_index(drop=True)

        # Display numerical predictions
        st.write("### Energy Predicted for Each Station on the Next Day")
        st.table(prediction_df)
        
        # Display predictions section
        st.write("### Visualization")
        
        # Create tabs for different visualizations
        tab1, tab2 = st.tabs(["Bar Chart", "Geographic Distribution"])
        
        with tab1:  
            # Horizontal Bar Chart  
            fig_bar = px.bar(prediction_df,  
                            x="Predicted Energy (kWh)",  # Switch x and y for horizontal bars
                            y="Station",  # Stations now appear on the y-axis
                            title="Predicted Energy Demand by Station",  
                            color_discrete_sequence=["#636EFA"]  # Use a single color for all bars (default Plotly blue)
                            )  

            # Update layout  
            fig_bar.update_layout(yaxis=dict(categoryorder="total ascending"),  # Sort bars by value (optional)
                                xaxis_title="Predicted Energy (kWh)",  # Add x-axis label
                                yaxis_title="Station",  # Add y-axis label
                                )  

            # Display the chart  
            st.plotly_chart(fig_bar, use_container_width=True)

        # with tab1:
        #     # Bar chart
        #     fig_bar = px.bar(prediction_df, 
        #                    x="Station", 
        #                    y="Predicted Energy (kWh)",
        #                    title="Predicted Energy Demand by Station",
        #                    color="Predicted Energy (kWh)",
        #                    color_continuous_scale="viridis")
        #     fig_bar.update_layout(xaxis_tickangle=-45)
        #     st.plotly_chart(fig_bar, use_container_width=True)
            
        # with tab2:
        #     # Pie chart
        #     fig_pie = px.pie(prediction_df, 
        #                    values="Predicted Energy (kWh)", 
        #                    names="Station",
        #                    title="Distribution of Predicted Energy Demand")
        #     st.plotly_chart(fig_pie, use_container_width=True)
            
        with tab2:
            # Geographic distribution
            # Get original lat/long data
            station_locations = ev_session_df.groupby('Station').agg({
                'Latitude': 'first',
                'Longitude': 'first'
            })
            
            # # Denormalize coordinates
            # station_locations['Latitude'] = station_locations['Latitude'] * (scaler.data_max_[3] - scaler.data_min_[3]) + scaler.data_min_[3]
            # station_locations['Longitude'] = station_locations['Longitude'] * (scaler.data_max_[2] - scaler.data_min_[2]) + scaler.data_min_[2]
            
            # Merge with predictions
            geo_data = station_locations.merge(prediction_df, left_index=True, right_on='Station')
            
            # Create map
            fig_map = px.scatter_mapbox(geo_data,
                                      lat='Latitude',
                                      lon='Longitude',
                                      size='Predicted Energy (kWh)',
                                      color='Predicted Energy (kWh)',
                                      hover_name='Station',
                                      zoom=6,
                                      title="Geographic Distribution of Predicted Demand")
            
            fig_map.update_layout(mapbox_style="carto-positron")
            st.plotly_chart(fig_map, use_container_width=True)
        
        
        # Add custom CSS to make the font size smaller for the values in the metrics
        st.markdown("""
            <style>
                .streamlit-expanderHeader {
                    font-size: 14px;
                }
                .stMetric .stMetricValue {
                    font-size: 12px !important;  /* Adjust the size as needed */
                }
            </style>
        """, unsafe_allow_html=True)

        

        # # Summary statistics
        # st.write("### Summary Statistics")
        # col1, col2, col3 = st.columns(3)
        
        # with col1:
        #     st.metric("Total Predicted Demand", 
        #              f"{prediction_df['Predicted Energy (kWh)'].sum():.2f} kWh")
        
        # with col2:
        #     st.metric("Average Station Demand", 
        #              f"{prediction_df['Predicted Energy (kWh)'].mean():.2f} kWh")
        
        # with col3:
        #     st.metric("Highest Demand Station", 
        #              f"{prediction_df.iloc[0]['Station']}\n({prediction_df.iloc[0]['Predicted Energy (kWh)']:.2f} kWh)")

