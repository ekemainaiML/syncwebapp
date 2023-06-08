import streamlit as st
import numpy as np
from mlem.api import import_object

# Load the model with MLEM (Iterative AI)
def load_model():
    model = import_object(path="best_gs_model_0.1.0.pkl", 
                          target="best_gs_model_0.1.0.mlem",
                            type_="pickle")
    return model

# Call method to get model
model = load_model()

# Create predict page
def show_predict_page():
    st.title("Synchronous motor excitation prediction")
    st.write("""### We need motor parameters to predict the excitation current""")
    Iy = st.number_input("Load Current Iy (A)", value=0.0, label_visibility="visible")
    PF = st.number_input("Power Factor PF", value=0.0, label_visibility="visible")
    e = st.number_input("Power Factor Error e", value=0.0, label_visibility="visible")
    dIf = st.number_input("Excitation Current Rate dIf (A/s)", value=0.0, label_visibility="visible")
    butcal = st.button("Calculate Excitation Current (A)")

    if butcal:
        X = np.array([[Iy, PF, e, dIf]])
        X = X.astype(float)
        If = model.predict(X)
        st.subheader(f"Excitation Current: {If[0][0]:.2f}A")