import streamlit as st
import joblib
import numpy as np

# Load the trained RandomForest model
model = joblib.load("student_performance_model.pkl")  # Make sure 'model.pkl' is in the same folder

# Main UI
st.set_page_config(page_title="Student Pass/Fail Predictor", layout="wide")

st.title("🎓 Student Performance Predictor")
st.markdown("Enter the subject scores and study time to predict if the student will pass or fail.")

# Collect user input
col1, col2 = st.columns(2)
with col1:
    sem1 = st.number_input("Semester 1 Marks", 0, 100, 60)
    sem2 = st.number_input("Semester 2 Marks", 0, 100, 60)
    study_time = st.slider("Study Time (hrs/day)", 0, 10, 2)

with col2:
    subject1 = st.number_input("Math Score", 0, 100, 70)
    subject2 = st.number_input("Science Score", 0, 100, 65)
    subject3 = st.number_input("English Score", 0, 100, 75)

# Calculate total & CGPA
total = sem1 + sem2 + subject1 + subject2 + subject3
cgpa = round(total / 50, 2)

st.markdown(f"**Total Marks:** {total}")
st.markdown(f"**Estimated CGPA:** {cgpa}")

# Predict button
if st.button("Predict Outcome"):
    input_data = np.array([[sem1, sem2, subject1, subject2, subject3, study_time]])
    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.success("✅ The student is likely to **Pass**.")
    else:
        st.error("❌ The student is likely to **Fail**.")
        st.info("📚 Recommended Resources:")
        st.markdown("- [Khan Academy](https://www.khanacademy.org/)")
        st.markdown("- [Coursera - Study Skills](https://www.coursera.org/)")
        st.markdown("- [YouTube: CrashCourse, StudyTube, etc.]")

