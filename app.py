import streamlit as st
import pickle
import numpy as np

model = pickle.load(open("rain_model.pkl", "rb"))

st.title("🌧 Rainfall Prediction App")

temp = st.number_input("Temperature (°C)")
humidity = st.number_input("Humidity (%)")
wind = st.number_input("Wind Speed (m/s)")
cloud = st.number_input("Cloud Cover (%)")
pressure = st.number_input("Pressure (hPa)")

if st.button("Predict Rain"):
    input_data = np.array([[temp, humidity, wind, cloud, pressure]])
    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.success("🌧 Rain Expected")
    else:
        st.success("☀ No Rain Expected")
