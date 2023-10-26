import numpy as np
from flask import Flask, request, render_template
import pickle

# Create Flask app
app=Flask(__name__,template_folder='templates')
model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def Home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    # Get the input values for current and voltage
    current1 = float(request.form['current1'])
    current2 = float(request.form['current2'])
    current3 = float(request.form['current3'])
    voltage1 = float(request.form['voltage1'])
    voltage2 = float(request.form['voltage2'])
    voltage3 = float(request.form['voltage3'])

    # Prepare the input data for prediction
    input_data = np.array([[current1, current2, current3, voltage1, voltage2, voltage3]])

    # Make a prediction using your model
    prediction = model.predict(input_data)

    # Based on your criteria, determine the fault classification
    if np.array_equal(prediction, [[0, 0, 0, 0]]):
        prediction_text = "No Fault"
    elif np.array_equal(prediction, [[1, 0, 0, 1]]):
        prediction_text = "LG Fault (Between Phase A and Gnd)"
    elif np.array_equal(prediction, [[0, 0, 1, 1]]):
        prediction_text = "LL Fault (Between Phase A and Phase B)"
    elif np.array_equal(prediction, [[1, 0, 1, 1]]):
        prediction_text = "LLG Fault (Between Phase A and Phase B and ground)"
    elif np.array_equal(prediction, [[0, 1, 1, 1]]):
        prediction_text = "LLL Fault (Between Phase A and Phase B and phase C)"
    elif np.array_equal(prediction, [[0, 0, 1, 1]]):
        prediction_text = "LLLG Fault (Three Phase Symmtrical Faults)"
    else:
        prediction_text = "Unknown Fault"
    return render_template("index.html", prediction_text=prediction_text)

if __name__ == "__main__":
    app.run(debug=True)