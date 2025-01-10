import streamlit as st
import pandas as pd
from PIL import Image

def render():
    st.title("🔍 Model Evaluation")
    
    # Introduction section
    st.markdown("""
    In this analysis, we evaluate three different deep learning models for energy demand prediction:
    
    1. **LSTM (Long Short-Term Memory)**: A type of RNN that can learn long-term dependencies
    2. **CNN-LSTM (Convolutional Neural Network + LSTM)**: A hybrid model combining CNN's feature extraction with LSTM's sequential learning capabilities
    3. **GRU (Gated Recurrent Unit)**: A variant of RNN with a simplified gating mechanism
    
    Best performing model: **CNN-LSTM hybrid model**
    """)
    
    st.markdown("---")

    # Metrics for LSTM
    lstm_metrics = {
        "Dataset": ["Training", "Testing"],
        "MSE": [0.002138, 0.002033],
        "RMSE": [0.04624, 0.04509],
        "MAE": [0.02912, 0.02793]
    }
    
    # Metrics for CNN-LSTM
    cnn_lstm_metrics = {
        "Dataset": ["Training", "Testing"],
        "MSE": [0.0010670, 0.001140],
        "RMSE": [0.03267, 0.03377],
        "MAE": [0.02003, 0.02086]
    }
    
    # Metrics for GRU
    gru_metrics = {
        "Dataset": ["Training", "Testing"],
        "MSE": [0.002298, 0.002249],
        "RMSE": [0.04793, 0.04742],
        "MAE": [0.03102, 0.03018]
    }
    
    # Convert metrics to DataFrames
    lstm_df = pd.DataFrame(lstm_metrics)
    cnn_lstm_df = pd.DataFrame(cnn_lstm_metrics)
    gru_df = pd.DataFrame(gru_metrics)
    
    # Display tables
    st.markdown("### LSTM Model Metrics")
    st.table(lstm_df)
    
    # Add an image
    # Load images
    image1 = 'loss_graph_lstm_final.jpg'
    image2 = 'lstm_actvspred_final.jpg'
    
    # Create columns
    col1, col2 = st.columns(2)
    
    # Display images and labels
    with col1:
        st.image(image1, caption='Training and Validation Loss', use_column_width=True)
    with col2:
        st.image(image2, caption='Actual vs Predicted Energy Demand', use_column_width=True)
    
    st.markdown("---")
    
    st.markdown("### CNN-LSTM Model Metrics")
    st.table(cnn_lstm_df)
    
    # Load images
    image1 = 'cnnlstm_loss_graph_final.jpg'
    image2 = 'cnnlstm_actvspred_final.jpg'
    
    # Create columns
    col3, col4 = st.columns(2)
    
    # Display images and labels
    with col3:
        st.image(image1, caption='Training and Validation Loss', use_column_width=True)
    with col4:
        st.image(image2, caption='Actual vs Predicted Energy Demand', use_column_width=True)
    
    st.markdown("---")
    
    # Display tables
    st.markdown("### GRU Model Metrics")
    st.table(gru_df)
    
    # Add an image
    # Load images
    image31 = 'gru_loss_graph.jpg'
    image32 = 'gru_actvspred.jpg'
    
    # Create columns
    col31, col32 = st.columns(2)
    
    # Display images and labels
    with col31:
        st.image(image31, caption='Training and Validation Loss', use_column_width=True)
    with col32:
        st.image(image32, caption='Actual vs Predicted Energy Demand', use_column_width=True)
    
    st.markdown("---")
    
    # Comparison Table
    st.markdown("### Model Comparison")
    
    comparison_data = {
        "Model": ["LSTM", "CNN-LSTM", "GRU"],
        "Training MSE": [lstm_metrics["MSE"][0], cnn_lstm_metrics["MSE"][0], gru_metrics["MSE"][0]],
        "Testing MSE": [lstm_metrics["MSE"][1], cnn_lstm_metrics["MSE"][1], gru_metrics["MSE"][1]],
        "Training RMSE": [lstm_metrics["RMSE"][0], cnn_lstm_metrics["RMSE"][0], gru_metrics["RMSE"][0]],
        "Testing RMSE": [lstm_metrics["RMSE"][1], cnn_lstm_metrics["RMSE"][1], gru_metrics["RMSE"][1]],
        "Training MAE": [lstm_metrics["MAE"][0], cnn_lstm_metrics["MAE"][0], gru_metrics["MAE"][0]],
        "Testing MAE": [lstm_metrics["MAE"][1], cnn_lstm_metrics["MAE"][1], gru_metrics["MAE"][1]]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # Style the dataframe to highlight CNN-LSTM row
    def highlight_cnn_lstm(row):
        return ['background-color: #90EE90' if row['Model'] == 'CNN-LSTM' else '' for _ in row]
    
    styled_comparison = comparison_df.style.apply(highlight_cnn_lstm, axis=1)
    st.dataframe(styled_comparison)
    
    # Add conclusion about CNN-LSTM performance
    st.markdown("""
    **Key Finding**: The CNN-LSTM hybrid model (highlighted in green) demonstrates superior performance across all metrics:
    - Lowest MSE values for both training and testing
    - Lowest RMSE values for both training and testing
    - Lowest MAE values for both training and testing
    
    This indicates that the combination of CNN's feature extraction capabilities with LSTM's sequential learning provides the most accurate energy demand predictions.
    """)