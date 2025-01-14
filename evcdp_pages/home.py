import streamlit as st

def render():
    # Set the title and subtitle for the Home Page
    st.title("🌟 EV Demand Forecast Hub 🌟")
    st.write("Platform for predicting electric vehicle charging demand across charging stations in Malaysia.")

    # Add an image
    st.image("EVCDPHub.jpg",  use_column_width=True)

    # Intro
    st.markdown(
        """
        ---
        ### Introduction
        <p style="font-size:16px; line-height:1.6;">
        The global shift toward electric vehicles (EVs) aims to reduce fossil fuel consumption and achieve 
        carbon neutrality. In Malaysia, government initiatives such as tax exemptions, home charging tax 
        reliefs, and plans to install 10,000 EV charging stations by 2025 have significantly boosted EV 
        adoption. This rapid growth has increased the demand for electricity and accessible charging infrastructure.
        </p>

        <p style="font-size:16px; line-height:1.6;">
        Accurate forecasting of charging demand is essential to support this transition. Several researchers have proven deep learning models, such 
        as LSTMs and GRUs, outperform traditional statistical models by effectively capture complex, non-linear relationships in the data, capture long term temporal  
        patterns in EV usage. This project leverages advanced deep learning techniques to predict next-day charging 
        demand across Malaysian regions, enabling better infrastructure planning, maintenance planning, reduced waiting times, and alignment 
        with the nation's green mobility goals.
        </p>
        

        """,
        unsafe_allow_html=True
    )


    # Objectives
    st.markdown(
        """
        ---
        ### Objectives
        -  To develop a model for predicting EV charging demand across stations in various regions
           in Malaysia using deep learning methods.
        -  To evaluate the model to ensure reliability of the model.
        -  To deploy the best performing model with an interactive web interface using Streamlit.

        """
    )

    # Add sections with a better design
    st.markdown(
        """
        ---
        ### Key Features
        - 📊 **Exploratory Data Analysis**: Gain insights into historical charging data.
        - 🧠 **Model Architecture**: Understand the models used for predictions.
        - 🎯 **Prediction Tool**: Forecast energy demand for EV charging stations.
        - 🔍 **Model Evaluation**: Review the performance of predictive models.
    

        """
    )

    # # Add sections with improved content
    # st.markdown(
    #     """
    #     ---
    #     ### Contact
    #     - Email: evcharginghub@gmail.com
    #     - Phone : 0126568788

        
    #     """
    # )

    # # Add sections with improved content
    # st.markdown(
    #     """
    #     ---
    #     ### Why Predict EV Charging Demand?
    #     Predicting the next-day charging demand for EV stations brings numerous advantages:
        
    #     - **Optimized Resource Allocation**: Ensures chargers and energy supplies are allocated efficiently.
    #     - **Energy Grid Management**: Helps electricity providers balance energy loads and avoid grid overloads.
    #     - **Dynamic Pricing Strategies**: Supports demand-based pricing to reduce congestion during peak hours.
    #     - **Data-Driven Expansion Planning**: Guides the development of new stations or upgrades in high-demand areas.
    #     - **Supports Malaysia's Green Agenda**: Aligns with the nation's goals for sustainability and EV adoption.

    #     ---
    #     ### Benefits for Malaysia
    #     By forecasting EV demand, we:
        
    #     - Enhance **user experience** with reduced waiting times and better reliability.
    #     - Support the **Low Carbon Mobility Blueprint (2021–2030)** to promote sustainable transportation.
    #     - Facilitate **cost savings** for operators and optimize the integration of renewable energy.
    #     - Ensure **preparedness for demand surges**, such as during public holidays or severe weather.

        
    #     """
    # )

    # Add a footer section
    st.markdown(
        """
        ---
        ### About This App
        <p style="font-size:16px; line-height:1.6;">
        This app is designed to empower EV station operators and energy providers with accurate demand forecasts.  
        </p>

        <p style="font-size:16px; line-height:1.6;">
        Contact:
        📭 evcharginghub@gmail.com  |  📞 0126568788
        </p>


        """,
        unsafe_allow_html=True
    )
