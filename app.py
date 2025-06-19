from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load model and scaler
model = pickle.load(open("rf_acc_68.pkl", "rb"))
scaler = pickle.load(open("normalizer.pkl", "rb"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            features = [float(x) for x in request.form.values()]
            features = np.array([features])

            # Normalize input
            features_scaled = scaler.transform(features)

            # Predict probability
            proba = model.predict_proba(features_scaled)[0][1]

            # Print debug info to console
            print("Input:", features)
            print("Scaled Input:", features_scaled)
            print("Prediction Probability:", proba)

            # Adjust threshold
            threshold = 0.7
            prediction = 1 if proba >= threshold else 0

            # Final message
            result = f"Liver Cirrhosis Detected! (Prob: {proba:.2f})" if prediction == 1 else f"No Liver Cirrhosis Detected. (Prob: {proba:.2f})"
            return render_template('result.html', prediction=result)
        except Exception as e:
            print("❌ ERROR:", e)
            return render_template('result.html', prediction="Something went wrong. Please try again.")

if __name__ == '__main__':
    app.run(debug=True)
