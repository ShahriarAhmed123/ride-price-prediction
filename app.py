import streamlit as st


import streamlit as st
import pandas as pd
import numpy as np

# Page title
st.title("RideEase Price Predictor")
st.write("Predict ride prices using Machine Learning")

# Sidebar inputs
st.sidebar.header("Enter Ride Details")

distance = st.sidebar.slider("Distance (miles)", 0.5, 20.0, 5.0)
duration = st.sidebar.slider("Duration (minutes)", 5, 120, 20)
hour = st.sidebar.slider("Hour of Day", 0, 23, 12)
day_of_week = st.sidebar.selectbox("Day of Week",
    options=[0, 1, 2, 3, 4, 5, 6],
    format_func=lambda x: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][x])

weather = st.sidebar.selectbox("Weather", ['Clear', 'Cloudy', 'Light Rain', 'Heavy Rain', 'Snow'])
temperature = st.sidebar.slider("Temperature (F)", 20, 100, 70)

pickup_location = st.sidebar.selectbox("Pickup Location",
    ['Airport', 'Business', 'Downtown', 'Entertainment', 'Residential', 'Suburban'])
dropoff_location = st.sidebar.selectbox("Dropoff Location",
    ['Airport', 'Business', 'Downtown', 'Entertainment', 'Residential', 'Suburban'])

vehicle_type = st.sidebar.selectbox("Vehicle Type", ['Standard', 'Premium', 'Luxury'])
driver_rating = st.sidebar.slider("Driver Rating", 1.0, 5.0, 4.5)

# Simple price prediction function
def predict_price(distance, duration, hour, day_of_week, weather, temperature,
                  pickup_location, dropoff_location, vehicle_type, driver_rating):

    # Base price calculation
    base_fare = 3.50
    per_mile = 2.50
    per_minute = 0.35

    price = base_fare + (distance * per_mile) + (duration * per_minute)

    # Vehicle type multiplier
    if vehicle_type == 'Luxury':
        price *= 1.8
    elif vehicle_type == 'Premium':
        price *= 1.4

    # Weather adjustment
    if weather == 'Heavy Rain':
        price *= 1.25
    elif weather == 'Snow':
        price *= 1.3
    elif weather == 'Light Rain':
        price *= 1.1

    # Rush hour (7-9 AM, 5-7 PM)
    if (7 <= hour <= 9) or (17 <= hour <= 19):
        price *= 1.15

    # Late night (10 PM - 4 AM)
    if hour >= 22 or hour <= 4:
        price *= 1.2

    # Airport surcharge
    if pickup_location == 'Airport' or dropoff_location == 'Airport':
        price += 5.0

    return max(price, 5.0)

# Calculate price
predicted_price = predict_price(distance, duration, hour, day_of_week, weather,
                                 temperature, pickup_location, dropoff_location,
                                 vehicle_type, driver_rating)

# Display results
st.header("Ride Summary")

col1, col2 = st.columns(2)

with col1:
    st.write("**Distance:**", distance, "miles")
    st.write("**Duration:**", duration, "minutes")
    st.write("**Time:**", f"{hour}:00")
    st.write("**Weather:**", weather)
    st.write("**Vehicle:**", vehicle_type)

with col2:
    st.write("**From:**", pickup_location)
    st.write("**To:**", dropoff_location)
    st.write("**Temperature:**", temperature, "F")
    st.write("**Driver Rating:**", driver_rating)

st.header("Predicted Price")
st.success(f"${predicted_price:.2f}")

# Price breakdown
st.subheader("Price Breakdown")
st.write("Base Fare: $3.50")
st.write(f"Distance Cost: ${distance * 2.50:.2f}")
st.write(f"Time Cost: ${duration * 0.35:.2f}")
st.write(f"Adjustments: ${predicted_price - 3.50 - distance*2.50 - duration*0.35:.2f}")
