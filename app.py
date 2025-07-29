import streamlit as st
import requests

st.set_page_config(page_title="Student Pass/Fail Prediction", layout="wide")

st.markdown("""
    <style>
    body {
        font-family: "Segoe UI", sans-serif;
    }
    .pass {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 15px;
        border-radius: 10px;
        font-weight: bold;
    }
    .fail {
        background-color: #ffebee;
        color: #c62828;
        padding: 15px;
        border-radius: 10px;
        font-weight: bold;
    }
    .low-score {
        border: 2px solid red;
        color: red;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Student Pass/Fail Prediction Dashboard")

with st.form("prediction_form"):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        failures = st.number_input("Failures", min_value=0)
        study_time = st.number_input("Study Time (hrs/week)", min_value=0)
        parental_support = st.selectbox("Parental Support", ["yes", "no"])
    with col2:
        core_python_total = st.number_input("Core Python Marks", min_value=0)
        advanced_java_total = st.number_input("Advanced Java Marks", min_value=0)
        internet_access = st.selectbox("Internet Access", ["yes", "no"])
    with col3:
        software_engg_total = st.number_input("Software Engineering Marks", min_value=0)
        dwdm_total = st.number_input("DWDM Marks", min_value=0)
        extra_curricular = st.selectbox("Extra-Curricular Activities", ["yes", "no"])
    with col4:
        prev_cgpa = st.number_input("Previous CGPA", min_value=0.0, format="%.2f")
        overall_total = core_python_total + advanced_java_total + software_engg_total + dwdm_total
        cgpa = round((overall_total / 400) * 10, 2)

        st.markdown("### Calculated Fields")
        if overall_total < 140:
            st.markdown(f'<div class="low-score">Overall Total: {overall_total}</div>', unsafe_allow_html=True)
        else:
            st.write(f"Overall Total: {overall_total}")

        if cgpa < 5:
            st.markdown(f'<div class="low-score">CGPA: {cgpa}</div>', unsafe_allow_html=True)
        else:
            st.write(f"CGPA: {cgpa}")

    submitted = st.form_submit_button("Predict Outcome")

if submitted:
    payload = {
        "failures": failures,
        "core_python_total": core_python_total,
        "advanced_java_total": advanced_java_total,
        "software_engg_total": software_engg_total,
        "dwdm_total": dwdm_total,
        "overall_total": overall_total,
        "cgpa": cgpa,
        "prev_cgpa": prev_cgpa,
        "study_time": study_time,
        "parental_support": parental_support,
        "internet_access": internet_access,
        "extra_curricular": extra_curricular,
    }

    try:
        res = requests.post("http://localhost:5000/predict", json=payload)
        result = res.json().get("prediction", "").upper()

        if result == "PASS":
            st.markdown(f'<div class="pass">✅ Prediction: {result}</div>', unsafe_allow_html=True)
        elif result == "FAIL":
            st.markdown(f'<div class="fail">❌ Prediction: {result}</div>', unsafe_allow_html=True)
            st.markdown("**📚 Resources to help improve:**")
            st.markdown("""
            - [Python – W3Schools](https://www.w3schools.com/python/)
            - [Java – JavaTpoint](https://www.javatpoint.com/java-tutorial)
            - [Software Engg – GFG](https://www.geeksforgeeks.org/software-engineering/)
            - [DWDM – NPTEL](https://nptel.ac.in/courses/106/106/106106089/)
            """)
        else:
            st.warning("❗ No valid prediction returned.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
