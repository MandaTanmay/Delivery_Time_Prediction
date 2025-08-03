import streamlit as st
import pickle
import numpy as np

# ---------------- Basic CSS Styling ----------------
st.markdown("""
<style>
    body {
        font-family: 'Segoe UI', sans-serif;
    }

    h1 {
        color: #1e3a8a;
        text-align: center;
    }

    .stButton > button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
    }

    .stButton > button:hover {
        background-color: #1d4ed8;
    }

    .stTextInput input, .stNumberInput input {
        font-size: 16px;
    }

    .stSelectbox label, .stNumberInput label {
        font-weight: bold;
    }

    .stSuccess {
        font-size: 18px;
    }

    /* Hide up/down arrows in number input (Chrome, Edge, Safari) */
    input[type=number]::-webkit-outer-spin-button,
    input[type=number]::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }

    /* Hide up/down arrows in number input (Firefox) */
    input[type=number] {
        -moz-appearance: textfield;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- Title ----------------
st.title("📦 Delivery Time Prediction")
st.markdown("### Fill in the delivery details below:")

# ---------------- Load Model ----------------
with open('best_regression_model.pkl', 'rb') as file:
    model = pickle.load(file)

# ---------------- Mapping Dicts ----------------
delivery_method_map = {"Select": -1, "Express": 0, "Overnight": 1, "Standard": 2}
traffic_map = {"Select": -1, "Low": 0, "Medium": 1, "High": 2}
weather_map = {"Select": -1, "Clear": 0, "Rainy": 1, "Snowy": 2}
priority_map = {"Select": -1, "High": 0, "Medium": 1, "Low": 2}
transport_map = {"Select": -1, "Bike": 0, "Truck": 1, "Van": 2}

# ---------------- User Inputs ----------------
distance = st.number_input("Distance (in km)", min_value=0.0, step=0.1, format="%.2f", value=None, placeholder="Enter distance")
weight = st.number_input("Package Weight (in kg)", min_value=0.0, step=0.1, format="%.2f", value=None, placeholder="Enter weight")

delivery_method = st.selectbox("Delivery Method", list(delivery_method_map.keys()))
traffic = st.selectbox("Traffic Conditions", list(traffic_map.keys()))
weather = st.selectbox("Weather Conditions", list(weather_map.keys()))
priority = st.selectbox("Delivery Priority", list(priority_map.keys()))
transport = st.selectbox("Transport Mode", list(transport_map.keys()))

# ---------------- Prediction Logic ----------------
if st.button("Predict Delivery Time"):
    if distance is None or weight is None:
        st.warning("Please enter valid numeric values for distance and weight.")
    elif -1 in [delivery_method_map[delivery_method],
                traffic_map[traffic],
                weather_map[weather],
                priority_map[priority],
                transport_map[transport]]:
        st.warning("Please make valid selections for all dropdowns.")
    else:
        try:
            input_data = np.array([[distance,
                                    weight,
                                    delivery_method_map[delivery_method],
                                    traffic_map[traffic],
                                    weather_map[weather],
                                    priority_map[priority],
                                    transport_map[transport]]])
            prediction = model.predict(input_data)[0]
            total_minutes = int(round(prediction * 60))
            hours = total_minutes // 60
            minutes = total_minutes % 60

            st.success(f"Estimated Delivery Time: **{hours} hour{'s' if hours != 1 else ''} {minutes} minute{'s' if minutes != 1 else ''}**")
        except Exception as e:
            st.error("Error: " + str(e))
