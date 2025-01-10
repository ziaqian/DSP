import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="EVCD Demand Forecast",
    page_icon="🚗",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("Navigation")
pages = {
    "Home": "evcdp_pages.home",
    "EDA": "evcdp_pages.eda",
    "Model Architecture": "evcdp_pages.modelarchitecture",
    "Prediction": "evcdp_pages.evcdp",
    "Evaluation": "evcdp_pages.evaluation"
}

# # Sidebar navigation
# st.sidebar.title("Navigation")
# pages = {
#     "🏠_Home": "evcdp_pages.home",
#     "📊_EDA": "evcdp_pages.eda",
#     "🧠_Model Architecture": "evcdp_pages.modelarchitecture",
#     "🎯_Prediction": "evcdp_pages.evcdp",
#     "🔍_Evaluation": "evcdp_pages.evaluation"
# }

selected_page = st.sidebar.radio("Go to:", list(pages.keys()))

# Dynamically load the selected page
page_module = __import__(pages[selected_page], fromlist=[""])
page_module.render()
