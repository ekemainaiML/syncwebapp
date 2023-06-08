import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page

# Add selection menu
page = st.sidebar.selectbox("Explore or Predict", ("Explore", "Predict"))

# Run app
if page == "Explore":
    show_explore_page()
else:
    show_predict_page()