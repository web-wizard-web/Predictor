import streamlit as st
import numpy as np
import joblib

# Load model and utilitiesimport streamlit as st
import numpy as np
import joblib

# Load model and utilities
model = joblib.load("student_performance_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

st.set_page_config(page_title="Student Pass/Fail Prediction", layout="wide")
st.markdown("<h2 style='text-align: center;'>🎓 Student Pass/Fail Prediction Dashboard</h2>", unsafe_allow_html=True)

with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)

    # Column 1 - Numeric
    with col1:
        attendance = st.slider("Attendance (%)", min_value=0, max_value=100, value=75)
        failures = st.number_input("Past Failures", min_value=0, step=1)
        core = st.number_input("Core Python Marks", min_value=0, max_value=100, value=50)
        java = st.number_input("Advanced Java Marks", min_value=0, max_value=100, value=50)

    # Column 2 - Numeric
    with col2:
        se = st.number_input("Software Engineering Marks", min_value=0, max_value=100, value=50)
        dwdm = st.number_input("DWDM Marks", min_value=0, max_value=100, value=50)
        prev_cgpa = st.number_input("Previous CGPA", min_value=0.0, max_value=10.0, step=0.1, value=6.0)
        study_time = st.slider("Study Time (hrs/week)", min_value=1, max_value=40, value=10)

    # Column 3 - Categorical
    with col3:
        parental_support = st.selectbox("Parental Support", ["yes", "no"])
        internet_access = st.selectbox("Internet Access", ["yes", "no"])
        extra_curricular = st.selectbox("Extra Curricular Activities", ["yes", "no"])

    # Calculated Total and CGPA
    total = core + java + se + dwdm
    cgpa = round((total / 400) * 10, 2)

    col_total, col_cgpa = st.columns(2)

    with col_total:
        if total < 140:
            st.markdown(f"<div style='color: red; font-weight: bold;'>❗ Overall Total: {total}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div><strong>Overall Total:</strong> {total}</div>", unsafe_allow_html=True)

    with col_cgpa:
        if cgpa < 5:
            st.markdown(f"<div style='color: red; font-weight: bold;'>❗ CGPA: {cgpa}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div><strong>CGPA:</strong> {cgpa}</div>", unsafe_allow_html=True)

    submitted = st.form_submit_button("🔍 Predict Outcome")

if submitted:
    numeric_features = np.array([[attendance, failures, core, java, se, dwdm, total, cgpa, prev_cgpa, study_time]])
    padded_numeric = np.concatenate((numeric_features[0], [0]*8)).reshape(1, -1)
    numeric_scaled = scaler.transform(padded_numeric)

    cat_features = [
        label_encoders['Parental Support'].transform([parental_support])[0],
        label_encoders['Internet Access'].transform([internet_access])[0],
        label_encoders['Extra Curricular'].transform([extra_curricular])[0]
    ]

    final_input = np.concatenate((numeric_scaled[0], cat_features)).reshape(1, -1)

    prediction = model.predict(final_input)[0]
    result = label_encoders["Target"].inverse_transform([prediction])[0]

    # Always suggest resources for weak subjects (score < 40)
    weak_subjects = []
    resources = {
        "Core Python": ("https://www.youtube.com/playlist?list=PLfqMhTWNBTe0b2nM6JHVCnAkhQRGiZMSJ", core),
        "Advanced Java": ("https://www.geeksforgeeks.org/advanced-java/", java),
        "Software Engineering": ("https://nptel.ac.in/courses/106105087", se),
        "DWDM": ("https://www.youtube.com/watch?v=2zYDK-FEvmQ&list=PLBlnK6fEyqRhqzDDHLx_ZCk5n9rwHY4WT", dwdm)
    }
    for subject, (link, score) in resources.items():
        if score < 40:
            weak_subjects.append((subject, link, score))

    if result.lower() == "pass":
        st.success("✅ Prediction: PASS")
    else:
        st.error("❌ Prediction: FAIL")

    if weak_subjects:
        st.markdown("### 📚 Suggested Resources for Weak Subjects:")
        for subject, link, score in weak_subjects:
            st.markdown(f"- [{subject}]({link}) — Score: **{score}** ❌")

    st.markdown("---")
    st.markdown(f"**Overall Total:** {total}  |  **CGPA:** {cgpa}")

model = joblib.load("student_performance_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

st.set_page_config(page_title="Student Pass/Fail Prediction", layout="wide")
st.markdown("<h2 style='text-align: center;'>🎓 Student Pass/Fail Prediction Dashboard</h2>", unsafe_allow_html=True)

with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)

    # Column 1 - Numeric
    with col1:
        attendance = st.slider("Attendance (%)", min_value=0, max_value=100, value=75)
        failures = st.number_input("Past Failures", min_value=0, step=1)
        core = st.number_input("Core Python Marks", min_value=0, max_value=100, value=50)
        java = st.number_input("Advanced Java Marks", min_value=0, max_value=100, value=50)

    # Column 2 - Numeric
    with col2:
        se = st.number_input("Software Engineering Marks", min_value=0, max_value=100, value=50)
        dwdm = st.number_input("DWDM Marks", min_value=0, max_value=100, value=50)
        prev_cgpa = st.number_input("Previous CGPA", min_value=0.0, max_value=10.0, step=0.1, value=6.0)
        study_time = st.slider("Study Time (hrs/week)", min_value=1, max_value=40, value=10)

    # Column 3 - Categorical
    with col3:
        parental_support = st.selectbox("Parental Support", ["yes", "no"])
        internet_access = st.selectbox("Internet Access", ["yes", "no"])
        extra_curricular = st.selectbox("Extra Curricular Activities", ["yes", "no"])

    # Calculated Total and CGPA
    total = core + java + se + dwdm
    cgpa = round((total / 400) * 10, 2)

    col_total, col_cgpa = st.columns(2)

    with col_total:
        if total < 140:
            st.markdown(f"<div style='color: red; font-weight: bold;'>❗ Overall Total: {total}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div><strong>Overall Total:</strong> {total}</div>", unsafe_allow_html=True)

    with col_cgpa:
        if cgpa < 5:
            st.markdown(f"<div style='color: red; font-weight: bold;'>❗ CGPA: {cgpa}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div><strong>CGPA:</strong> {cgpa}</div>", unsafe_allow_html=True)

    submitted = st.form_submit_button("🔍 Predict Outcome")

if submitted:
    numeric_features = np.array([[attendance, failures, core, java, se, dwdm, total, cgpa, prev_cgpa, study_time]])
    numeric_scaled = scaler.transform(numeric_features)

    cat_features = [
        label_encoders['Parental Support'].transform([parental_support])[0],
        label_encoders['Internet Access'].transform([internet_access])[0],
        label_encoders['Extra Curricular'].transform([extra_curricular])[0]
    ]

    final_input = np.concatenate((numeric_scaled[0], cat_features)).reshape(1, -1)

    prediction = model.predict(final_input)[0]
    result = label_encoders["Target"].inverse_transform([prediction])[0]

    # Always suggest resources for weak subjects (score < 40)
    weak_subjects = []
    resources = {
        "Core Python": ("https://www.youtube.com/playlist?list=PLfqMhTWNBTe0b2nM6JHVCnAkhQRGiZMSJ", core),
        "Advanced Java": ("https://www.geeksforgeeks.org/advanced-java/", java),
        "Software Engineering": ("https://nptel.ac.in/courses/106105087", se),
        "DWDM": ("https://www.youtube.com/watch?v=2zYDK-FEvmQ&list=PLBlnK6fEyqRhqzDDHLx_ZCk5n9rwHY4WT", dwdm)
    }
    for subject, (link, score) in resources.items():
        if score < 40:
            weak_subjects.append((subject, link, score))

    if result.lower() == "pass":
        st.success("✅ Prediction: PASS")
    else:
        st.error("❌ Prediction: FAIL")

    if weak_subjects:
        st.markdown("### 📚 Suggested Resources for Weak Subjects:")
        for subject, link, score in weak_subjects:
            st.markdown(f"- [{subject}]({link}) — Score: **{score}** ❌")

    st.markdown("---")
    st.markdown(f"**Overall Total:** {total}  |  **CGPA:** {cgpa}")
