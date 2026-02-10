import streamlit as st
import pickle
import numpy as np
import requests

# GitHub RAW URL
MODEL_URL = "https://raw.githubusercontent.com/sudha1608/Green-AI-project/main/rain_model.pkl"

@st.cache_resource
def load_model():
    response = requests.get(MODEL_URL)
    model = pickle.loads(response.content)
    return model

model = load_model()

st.set_page_config(page_title="Rainfall Prediction", layout="centered")
st.title("🌧 Rainfall Prediction App")

# Input fields
temp = st.number_input("Temperature (°C)", value=25.0)
humidity = st.number_input("Humidity (%)", value=60.0)
wind = st.number_input("Wind Speed (m/s)", value=5.0)
cloud = st.number_input("Cloud Cover (%)", value=50.0)
pressure = st.number_input("Pressure (hPa)", value=1010.0)

if st.button("Predict Rain"):
    input_data = np.array([[temp, humidity, wind, cloud, pressure]])
    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)[0][1]

    if prediction[0] == 1:
        st.success(f"🌧 Rain Expected (Probability: {probability*100:.2f}%)")
        st.warning("Carry an umbrella ☂")
    else:
        st.success(f"☀ No Rain Expected (Probability: {(1-probability)*100:.2f}%)")
