import streamlit as st
import joblib

# Load model and scaler
model = joblib.load('best_model.pkl')
scaler = joblib.load('scaler.pkl')

st.title("Ride Price Prediction App 🚗💰")

# Numeric inputs
distance = st.number_input("Distance (miles)", min_value=0.0)
duration = st.number_input("Duration (minutes)", min_value=0.0)
hour = st.number_input("Hour of Day (0–23)", min_value=0, max_value=23)
day_of_week = st.number_input("Day of Week (0=Mon, 6=Sun)", min_value=0, max_value=6)
temperature = st.number_input("Temperature (°F)", min_value=-10.0)
driver_rating = st.number_input("Driver Rating (1.0–5.0)", min_value=1.0, max_value=5.0)

# Categorical inputs
weather = st.selectbox("Weather", ["Clear", "Cloudy", "Rainy", "Snowy"])
pickup_location = st.selectbox("Pickup Location", ["Downtown", "Business", "Suburban", "Residential", "Airport", "Entertainment"])
dropoff_location = st.selectbox("Dropoff Location", ["Downtown", "Business", "Suburban", "Residential", "Airport", "Entertainment"])
vehicle_type = st.selectbox("Vehicle Type", ["Standard", "Premium", "Luxury"])

# Dummy encoding logic (replace with actual encoding used during training)
def encode_inputs():
    encoded = [distance, duration, hour, day_of_week, temperature, driver_rating]
    encoded.extend([
        weather == "Clear", weather == "Cloudy", weather == "Rainy", weather == "Snowy",
        pickup_location == "Downtown", pickup_location == "Business", pickup_location == "Suburban",
        pickup_location == "Residential", pickup_location == "Airport", pickup_location == "Entertainment",
        dropoff_location == "Downtown", dropoff_location == "Business", dropoff_location == "Suburban",
        dropoff_location == "Residential", dropoff_location == "Airport", dropoff_location == "Entertainment",
        vehicle_type == "Standard", vehicle_type == "Premium", vehicle_type == "Luxury"
    ])
    return [int(val) if isinstance(val, bool) else val for val in encoded]

if st.button("Predict Price"):
    input_data = [encode_inputs()]
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)
    st.success(f"Predicted Ride Price: ${round(prediction[0], 2)}")
