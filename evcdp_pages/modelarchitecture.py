import streamlit as st
import pandas as pd
from PIL import Image

def render():
    st.title("🧠 Model Architecture")
    
    # Set custom CSS for better spacing
    st.markdown("""
        <style>
        .stImage > img {
            max-width: 90%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    This page presents three different deep learning architectures implemented for energy demand prediction:
    1. CNN-LSTM (Hybrid Model)
    2. GRU (Gated Recurrent Unit)
    3. LSTM (Long Short-Term Memory)
                
    """)
    
    st.markdown("---")
    
    # LSTM Architecture
    st.markdown("## 1. LSTM Architecture")
    
    col5, spacer1, col6 = st.columns([4, 1, 5])
    
    with col5:
        st.image('lstm_architecture.png', caption='LSTM Architecture Diagram', use_column_width=True)
        
    with col6:
        st.markdown("""
        ### Structure
        - Input Layer → LSTM → Dropout → LSTM → Dropout → Dense
        
        ### Key Components
        - Dual LSTM layers
        - Dropout layers for regularization
        - Dense layer 
        
        ### Justification
        - Classic modern architecture for time series
        - Excellent at capturing long-term dependencies
        - Proven track record in sequence modeling
        - Advantages include:
            1. Robust handling of long sequences
            2. Effective memory management
            3. Stable training process
        """)
    
    st.markdown("---")

    # CNN-LSTM Architecture
    st.markdown("## 2. CNN-LSTM Architecture")
    
    col1, spacer2, col2 = st.columns([4, 1, 5])
    
    with col1:
        st.image('cnnlstm_architecture.png', caption='CNN-LSTM Architecture Diagram', use_column_width=True)
        
    with col2:
        st.markdown("""
        ### Structure
        - Input Layer → Conv1D → MaxPooling1D → LSTM → Dropout → LSTM → Dropout → Dense
        
        ### Key Components
        - 1D Convolution 
        - MaxPooling1D for dimensionality reduction
        - Dual LSTM layers 
        - Strategic dropout layers
        - Dense layer 
        
        ### Justification
        - CNN extracts local patterns and features
        - MaxPooling reduces computation while preserving features
        - Dual LSTM layers capture both short and long-term dependencies
        - Best performing model due to:
            1. CNN's effective feature extraction
            2. LSTM's temporal pattern learning
            3. Balanced dimensionality reduction
        """)
    
    st.markdown("---")
    
    # GRU Architecture
    st.markdown("## 3. GRU Architecture")
    
    col3, spacer3, col4 = st.columns([4, 1, 5])
    
    with col3:
        st.image('gru_architecture.png', caption='GRU Architecture Diagram', use_column_width=True)
        
    with col4:
        st.markdown("""
        ### Structure
        - Input Layer → GRU → Dropout → GRU → Dropout → Dense
        
        ### Key Components
        - Dual GRU layers 
        - Dropout layers for regularization
        - Dense layer
        
        ### Justification
        - Simpler alternative to LSTM
        - Efficient training process
        - Effective with limited data
        - Benefits include:
            1. Fewer parameters than LSTM
            2. Faster training time
            3. Good balance of performance vs complexity
        """)
    
    st.markdown("---")
    
    
    # Common Features in a container for consistent spacing
    with st.container():
        st.markdown("""
        ### Common Features Across All Architectures
        1. **Input/Output Consistency**
            - Input shape: (None, 7, 14)
            - Output shape: (None, 14)
            
        2. **Architectural Patterns**
            - Gradual dimension reduction (64 → 32 → 14)
            - Dropout layers for regularization
            - Dense layer for final prediction
            
        3. **Training Considerations**
            - All models use similar optimization strategies
            - Dropout rates carefully tuned
            - Batch size and epochs standardized
        """)
