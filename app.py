import streamlit as st
import pickle
import numpy as np
import requests
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SkyCast AI | Premium Weather Intelligence",
    page_icon="🌈",
    layout="wide"
)

# ---------------- ADVANCED CUSTOM CSS ----------------
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        color: #f8fafc;
    }

    /* Glassmorphism Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    
    .glass-card:hover {
        border: 1px solid rgba(56, 189, 248, 0.4);
    }

    /* Hero Text */
    .hero-text {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .sub-text {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }

    /* Metric Styling */
    .metric-box {
        text-align: center;
        padding: 15px;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 15px;
    }

    /* Custom Button */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
        color: white;
        font-weight: bold;
        padding: 15px;
        border: none;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 5px 15px rgba(56, 189, 248, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
MODEL_URL = "https://raw.githubusercontent.com/sudha1608/Green-AI-project/main/rain_model.pkl"

@st.cache_resource
def load_model():
    try:
        response = requests.get(MODEL_URL)
        return pickle.loads(response.content)
    except:
        return None

model = load_model()

# ---------------- HERO SECTION ----------------
st.markdown("<div class='hero-text'>SkyCast AI</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Next-Gen Rainfall Intelligence & Green Computing 🌱</div>", unsafe_allow_html=True)

# ---------------- MAIN LAYOUT ----------------
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("### 🛠️ Atmospheric Parameters")
    
    with st.container():
        # Using a glass card for inputs
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        temp = st.select_slider("🌡️ Temperature (°C)", options=np.arange(0.0, 51.0, 1.0), value=25.0)
        humidity = st.slider("💧 Humidity Level (%)", 0, 100, 60)
        wind = st.slider("🌬️ Wind Velocity (m/s)", 0.0, 20.0, 5.0)
        cloud = st.select_slider("☁️ Cloud Density (%)", options=np.arange(0, 101, 5), value=50)
        pressure = st.number_input("📉 Surface Pressure (hPa)", 900, 1100, 1010)
        
        predict_btn = st.button("✨ ANALYZE WEATHER PATTERNS")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if predict_btn:
        with st.spinner("🤖 AI Processing atmospheric data..."):
            time.sleep(1) # Visual effect
            
            input_data = np.array([[temp, humidity, wind, cloud, pressure]])
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][1]
            confidence = max(probability, 1 - probability) * 100

            # --- RESULT DISPLAY ---
            if prediction == 1:
                st.markdown("""
                <div class="glass-card" style="border-left: 5px solid #38bdf8;">
                    <h1 style='font-size: 4rem; margin:0;'>🌧️</h1>
                    <h2 style='color: #38bdf8;'>Rainfall Likely</h2>
                    <p>Expect precipitation in your area. Grab your gear!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="glass-card" style="border-left: 5px solid #facc15;">
                    <h1 style='font-size: 4rem; margin:0;'>☀️</h1>
                    <h2 style='color: #facc15;'>Clear Skies</h2>
                    <p>No significant rainfall detected for these parameters.</p>
                </div>
                """, unsafe_allow_html=True)

            # --- CONFIDENCE METER ---
            st.write(f"**AI Confidence Level**")
            st.progress(int(confidence))
            st.caption(f"The model is {confidence:.2f}% sure of this result.")

            # --- AI LOGIC (EXPLAINABILITY) ---
            st.markdown("### 🧠 Neural Insights")
            reasons = []
            if humidity > 70: reasons.append("💧 **Humidity**: High saturation detected.")
            if cloud > 60: reasons.append("☁️ **Cloud**: High density supports formation.")
            if pressure < 1005: reasons.append("📉 **Pressure**: Low pressure trough detected.")
            if not reasons: reasons.append("✨ **Stable**: No anomalies detected.")
            
            for r in reasons:
                st.info(r)

    else:
        # Welcome placeholder
        st.markdown("""
        <div class="glass-card" style="text-align: center; height: 400px; display: flex; flex-direction: column; justify-content: center;">
            <h2 style='color: #64748b;'>Awaiting Input...</h2>
            <p>Adjust the sliders on the left and click Analyze to generate an AI forecast.</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------- FOOTER / GREEN AI ----------------
st.divider()
f_col1, f_col2 = st.columns(2)

with f_col1:
    st.markdown("""
    #### 🌱 Eco-Friendly Compute
    This prediction was generated using **Green AI** principles, utilizing a low-latency 
    Logistic Regression core to minimize carbon footprint per inference.
    """)

with f_col2:
    st.markdown("""
    #### 🛡️ Live Advisories
    - **Rain:** ☂️ Carry umbrella | 🚗 Slow speeds
    - **Clear:** 🕶️ Use UV protection | 🏃 Perfect for outdoors
    """)