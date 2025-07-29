from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS

# Load model, scaler, encoders
model = joblib.load('student_performance_model.pkl')
scaler = joblib.load('scaler.pkl')
label_encoders = joblib.load('label_encoders.pkl')

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    # Extract input data
    input_numeric = np.array([[
        data['attendance'], data['failures'],
        data['core_python_total'], data['advanced_java_total'],
        data['software_engg_total'], data['dwdm_total'],
        data['overall_total'], data['cgpa'],
        data['prev_cgpa'], data['study_time']
    ]])
    input_numeric_scaled = scaler.transform(input_numeric)

    input_cat = [
        label_encoders['Parental Support'].transform([data['parental_support']])[0],
        label_encoders['Internet Access'].transform([data['internet_access']])[0],
        label_encoders['Extra Curricular'].transform([data['extra_curricular']])[0]
    ]

    # Combine all features
    final_input = np.concatenate((input_numeric_scaled[0], input_cat)).reshape(1, -1)
    prediction = model.predict(final_input)[0]
    result = label_encoders['Target'].inverse_transform([prediction])[0]

    # Suggest resources if student fails
    resources = {}
    if result.lower() == "fail":
        thresholds = {
            "Core Python": data['core_python_total'],
            "Advanced Java": data['advanced_java_total'],
            "Software Engineering": data['software_engg_total'],
            "DWDM": data['dwdm_total']
        }
        for subject, score in thresholds.items():
            if score < 40:
                resources[subject] = recommend_resource(subject)

    return jsonify({
        "prediction": result,
        "resources": resources
    })

def recommend_resource(subject):
    subject_resources = {
        "Core Python": "https://www.youtube.com/playlist?list=PLfqMhTWNBTe0b2nM6JHVCnAkhQRGiZMSJ",
        "Advanced Java": "https://www.geeksforgeeks.org/advanced-java/",
        "Software Engineering": "https://nptel.ac.in/courses/106105087",
        "DWDM": "https://www.youtube.com/watch?v=2zYDK-FEvmQ&list=PLBlnK6fEyqRhqzDDHLx_ZCk5n9rwHY4WT"
    }
    return subject_resources.get(subject, "No resource available")

if __name__ == '__main__':
    app.run(debug=True)
    