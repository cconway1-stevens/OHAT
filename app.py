# app.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap
from tire_estimator import tire_estimator_page
from sales_sequence import sales_sequence_page

# Initialize session state for tires and brands if not already present
if "tires" not in st.session_state:
    st.session_state.tires = []

if "brands" not in st.session_state:
    st.session_state.brands = ["Michelin", "Goodyear", "Bridgestone", "Pirelli", "Continental"]

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Tire Estimator", "Sales Sequence Chart"])

# Shared input parameters
with st.sidebar.expander("Tax and Fees"):
    tax = st.number_input("Tax (%)", value=6.625, key="tax")
    surcharge = st.number_input("Surcharge ($)", value=5.0, key="surcharge")
    tire_markup = st.number_input("Tire Mark Up ($)", value=67.0, key="tire_markup")
    nj_tire_tax = st.number_input("NJ Tire Tax ($)", value=1.5, key="nj_tire_tax")
    disposal_fee = st.number_input("Disposal Fee ($)", value=7.0, key="disposal_fee")

# Page-specific input parameters and content
if page == "Tire Estimator":
    with st.sidebar.expander("Tire Details"):
        tire_name = st.text_input("Tire Name", key="tire_name")
        tire_brand = st.selectbox("Tire Brand", st.session_state.brands + ["Other"], key="tire_brand")
        if tire_brand == "Other":
            tire_brand = st.text_input("Enter New Brand", key="new_tire_brand")
            if st.button("Add Brand", key="add_brand_button"):
                if tire_brand and tire_brand not in st.session_state.brands:
                    st.session_state.brands.append(tire_brand)
        else:
            st.text(f"Selected Brand: {tire_brand}")

        tire_cost = st.number_input("Tire Cost ($)", value=100.0, key="tire_cost")
        if st.button("Add Tire", key="add_tire_button"):
            st.session_state.tires.append({"name": tire_name, "brand": tire_brand, "cost": tire_cost})

    with st.sidebar.expander("Actions"):
        if st.button("Undo Last Tire", key="undo_tire_button"):
            st.session_state.tires.pop() if st.session_state.tires else None

        if st.button("Clear All Tires", key="clear_tires_button"):
            st.session_state.tires = []

    tire_estimator_page(tax, surcharge, tire_markup, nj_tire_tax, disposal_fee)
elif page == "Sales Sequence Chart":
    with st.sidebar.expander("Sales Sequence Chart"):
        start_price = st.number_input("Start Price", value=100, step=1, key="start_price")
        end_price = st.number_input("End Price", value=500, step=1, key="end_price")
        interval = st.number_input("Interval", value=10, step=1, key="interval")

    sales_sequence_page(start_price, end_price, interval, tax, surcharge, tire_markup, nj_tire_tax, disposal_fee)
