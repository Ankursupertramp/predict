from flask import Flask,request, url_for, redirect, render_template
app = Flask(__name__)
import numpy as np
import joblib
import pandas as pd

model = joblib.load('model.pkl')

input_data = np.array([i1,i2,i3,v1,v2,v3z])


prediction = model.predict(input_data.reshape(1, -1))
pred = prediction.tolist()
print(pred)
if pred ==[[0, 0, 0, 0]]:
    print("No fault")
elif pred == [[1, 0, 0, 1]]:
    print( "LG Fault (Between Phase A and Gnd)")
elif pred == [[0, 0, 1, 1]]:
    print("LL Fault (Between Phase A and Phase B)")
elif pred == [[1, 0, 1, 1]]:
    print("LLG Fault (Between Phases A, B, and ground)")
elif pred == [[0, 1, 1, 1]]:
    print("LLL Fault (Between all three phases)")
elif pred == [[1, 1, 1, 1]]:
    print("LLLG Fault (Three-phase symmetrical fault)")
