import streamlit as st
import pickle
import json
import numpy as np

# Load the model
with open("bangalore_home_prices_model.pickle", "rb") as f:
    model = pickle.load(f)

# Load the columns
with open("columns.json", "r") as f:
    data_columns = json.load(f)["data_columns"]

def predict_price(location, sqft, bath, bhk):
    try:
        loc_index = data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return model.predict([x])[0]

def main():
    st.title("Bangalore House Price Prediction")

    sqft = st.number_input("Total Square Feet Area", min_value=300, max_value=10000, value=1000)
    bath = st.number_input("Number of Bathrooms", min_value=1, max_value=10, value=2)
    bhk = st.number_input("Number of BHK", min_value=1, max_value=10, value=2)
    location = st.selectbox("Location", sorted([col for col in data_columns[3:]]))

    if st.button("Predict Price"):
        price = predict_price(location, sqft, bath, bhk)
        st.success(f"Estimated Price: ₹ {price*100000:.2f}")

if __name__ == "__main__":
    main()
