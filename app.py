import streamlit as st
import joblib
import pandas as pd

model = joblib.load("house_price_model.pkl")

USD_TO_NGN = 1500

st.title("House Price Prediction")

st.write("Enter the details of the house to predict its price.")

st.subheader("Property Details")
st.subheader("Garage Details")
st.subheader("Basement & Floor Details")
st.subheader("Location Details")

overall_qual = st.number_input(
    "Overall Quality",
    min_value=1,
    max_value=10,
    value=9
)

gr_liv_area = st.number_input(
    "Living Area (sq ft)",
    min_value=0,
    value=1500
)

year_built = st.number_input(
    "Year Built",
    min_value=1800,
    max_value=2026,
    value=2000
)

lot_area = st.number_input(
    "Lot Area (sq ft)",
    min_value=0,
    value=8000
)

overall_cond = st.number_input(
    "Overall Condition",
    min_value=1,
    max_value=10,
    value=5
)

bedrooms = st.number_input(
    "Number of Bedrooms",
    min_value=0,
    max_value=20,
    value=3
)

full_bath = st.number_input(
    "Full Bathrooms",
    min_value=0,
    max_value=10,
    value=2
)

garage_cars = st.number_input(
    "Garage Capacity",
    min_value=0,
    max_value=5,
    value=2
)

garage_area = st.number_input(
    "Garage Area (sq ft)",
    min_value=0,
    value=500
)

year_remod_add = st.number_input(
    "Year Remodeled",
    min_value=1800,
    max_value=2026,
    value=2000
)

yr_sold = st.number_input(
    "Year Sold",
    min_value=2006,
    max_value=2026,
    value=2010
)

house_age = yr_sold - year_built

years_since_remodel = yr_sold - year_remod_add

has_garage = 1 if garage_area > 0 else 0

total_bsmt_sf = st.number_input(
    "Basement Area (sq ft)",
    min_value=0,
    value=1000
)

first_flr_sf = st.number_input(
    "1st Floor Area (sq ft)",
    min_value=0,
    value=1000
)

second_flr_sf = st.number_input(
    "2nd Floor Area (sq ft)",
    min_value=0,
    value=500
)

wood_deck_sf = st.number_input(
    "Wood Deck Area (sq ft)",
    min_value=0,
    value=0
)

open_porch_sf = st.number_input(
    "Open Porch Area (sq ft)",
    min_value=0,
    value=50
)

total_sf = total_bsmt_sf + first_flr_sf + second_flr_sf

total_porch_sf = wood_deck_sf + open_porch_sf

half_bath = st.number_input(
    "Half Bathrooms",
    min_value=0,
    max_value=10,
    value=0
)

bsmt_full_bath = st.number_input(
    "Basement Full Bathrooms",
    min_value=0,
    max_value=10,
    value=0
)

bsmt_half_bath = st.number_input(
    "Basement Half Bathrooms",
    min_value=0,
    max_value=10,
    value=0
)

total_bathrooms = (
    full_bath
    + 0.5 * half_bath
    + bsmt_full_bath
    + 0.5 * bsmt_half_bath
)

neighborhood = st.selectbox(
    "Neighborhood",
    [
        "NAmes",
        "CollgCr",
        "OldTown",
        "Edwards",
        "Somerst",
        "Gilbert",
        "NridgHt",
        "Sawyer",
        "NWAmes",
        "Other"
    ]
)

ms_zoning = st.selectbox(
    "Zoning",
    [
        "RL",
        "RM",
        "FV",
        "RH"
    ]
)

input_data = {column: 0 for column in model.feature_names_in_}

input_data["OverallQual"] = overall_qual
input_data["OverallCond"] = overall_cond
input_data["GrLivArea"] = gr_liv_area
input_data["YearBuilt"] = year_built
input_data["YearRemodAdd"] = year_remod_add
input_data["LotArea"] = lot_area
input_data["BedroomAbvGr"] = bedrooms
input_data["FullBath"] = full_bath
input_data["HalfBath"] = half_bath
input_data["BsmtFullBath"] = bsmt_full_bath
input_data["BsmtHalfBath"] = bsmt_half_bath
input_data["GarageCars"] = garage_cars
input_data["GarageArea"] = garage_area
input_data["TotalBsmtSF"] = total_bsmt_sf
input_data["1stFlrSF"] = first_flr_sf
input_data["2ndFlrSF"] = second_flr_sf
input_data["WoodDeckSF"] = wood_deck_sf
input_data["OpenPorchSF"] = open_porch_sf

input_data["TotalSF"] = total_sf
input_data["TotalBathrooms"] = total_bathrooms
input_data["TotalPorchSF"] = total_porch_sf
input_data["HouseAge"] = house_age
input_data["YearsSinceRemodel"] = years_since_remodel
input_data["HasGarage"] = has_garage


if ms_zoning != "RL":
    input_data[f"MSZoning_{ms_zoning}"] = 1

if neighborhood != "Other":
    input_data[f"Neighborhood_{neighborhood}"] = 1

input_df = pd.DataFrame([input_data])

if st.button("Predict House Price"):
    prediction = model.predict(input_df)
    predicted_price = prediction[0]

    naira_price = predicted_price * USD_TO_NGN

    st.success(f"Predicted House Price: ${predicted_price:,.2f}")
    st.info(f"Approximate Value in Naira: ₦{naira_price:,.0f}")