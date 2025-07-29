import streamlit as st
import numpy as np
import pickle

# Load your model once
with open("student_performance_model.pkl", "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="Student Pass/Fail Predictor", layout="wide")

st.markdown("<h1 style='text-align: center;'>🎓 Student Pass/Fail Prediction Dashboard</h1>", unsafe_allow_html=True)

# --- Input Columns ---
col1, col2, col3, col4 = st.columns(4)

failures = col1.number_input("Failures", min_value=0, step=1)
study_time = col1.number_input("Study Time (hrs/week)", min_value=0, step=1)
parental_support = col1.selectbox("Parental Support", ["yes", "no"])
internet_access = col1.selectbox("Internet Access", ["yes", "no"])
extra_activities = col1.selectbox("Extra-Curricular Activities", ["yes", "no"])

core_python = col2.number_input("Core Python Marks", min_value=0, max_value=100, step=1)
adv_java = col2.number_input("Advanced Java Marks", min_value=0, max_value=100, step=1)
software_eng = col3.number_input("Software Engineering Marks", min_value=0, max_value=100, step=1)
dwdm = col3.number_input("DWDM Marks", min_value=0, max_value=100, step=1)
prev_cgpa = col4.number_input("Previous CGPA", min_value=0.0, max_value=10.0, step=0.1)

# --- Calculations ---
total = core_python + adv_java + software_eng + dwdm
cgpa = round(total / 40, 2)  # Example: divide by 40 to get CGPA (assuming max total 160)

# Display calculated fields
st.markdown(
    f"""
    <div style="border: 2px solid red; padding: 10px; width: 300px;">
        <h4 style="color:red;">Calculated Fields</h4>
        <p><b>Overall Total:</b> {total}</p>
        <p><b>CGPA:</b> {cgpa}</p>
    </div>
    """, unsafe_allow_html=True
)

# --- Predict Button ---
if st.button("Predict Outcome"):
    # Prepare data for model
    encoded_support = 1 if parental_support == "yes" else 0
    encoded_net = 1 if internet_access == "yes" else 0
    encoded_extra = 1 if extra_activities == "yes" else 0

    input_data = [failures, study_time, encoded_support, encoded_net, encoded_extra,
                  core_python, adv_java, software_eng, dwdm, prev_cgpa]

    result = model.predict([input_data])[0]

    st.success(f"🎯 Prediction: {'Pass' if result == 1 else 'Fail'}")
