import streamlit as st
import json
import os
import base64
from datetime import datetime
from sales_sequence import sales_sequence_page
from tire_estimator import tire_estimator_page

def load_data():
    with open("data.json", "r") as f:
        return json.load(f)

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)

def encode_data_to_url(data):
    json_str = json.dumps(data)
    json_bytes = json_str.encode('utf-8')
    base64_bytes = base64.urlsafe_b64encode(json_bytes)
    base64_str = base64_bytes.decode('utf-8')
    return base64_str

def decode_data_from_url():
    query_params = st.experimental_get_query_params()
    if "data" in query_params:
        base64_str = query_params["data"][0]
        base64_bytes = base64.urlsafe_b64decode(base64_str.encode('utf-8'))
        json_str = base64_bytes.decode('utf-8')
        data = json.loads(json_str)
        return data
    return None

if __name__ == "__main__":
    # Load default data
    data = load_data()

    # Decode data from URL if present
    url_data = decode_data_from_url()
    if url_data:
        data = url_data

    # Initialize session state variables if not already present
    if "tires" not in st.session_state:
        st.session_state.tires = data.get("tires", [])

    if "brands" not in st.session_state:
        st.session_state.brands = data.get("brands", [])

    if "tax" not in st.session_state:
        st.session_state.tax = data.get("tax", 6.625)

    if "surcharge" not in st.session_state:
        st.session_state.surcharge = data.get("surcharge", 0.0)

    if "tire_markup" not in st.session_state:
        st.session_state.tire_markup = data.get("tire_markup", 0.0)

    if "nj_tire_tax" not in st.session_state:
        st.session_state.nj_tire_tax = data.get("nj_tire_tax", 1.5)

    if "disposal_fee" not in st.session_state:
        st.session_state.disposal_fee = data.get("disposal_fee", 1.0)

    if "start_price" not in st.session_state:
        st.session_state.start_price = data.get("start_price", 100)

    if "end_price" not in st.session_state:
        st.session_state.end_price = data.get("end_price", 500)

    if "interval" not in st.session_state:
        st.session_state.interval = data.get("interval", 10)

    if "shop_name" not in st.session_state:
        st.session_state.shop_name = data.get("shop_name", "Ocean Heights Auto and Tire")

    if "shop_address" not in st.session_state:
        st.session_state.shop_address = data.get("shop_address", "1178 Ocean Heights Avenue, Egg Harbor Township, NJ 08234")

    if "shop_phone" not in st.session_state:
        st.session_state.shop_phone = data.get("shop_phone", "Phone: (609) 241-1546")

    if "credit_card_fee" not in st.session_state:
        st.session_state.credit_card_fee = data.get("credit_card_fee", 3.0)

    def reset_url():
        st.experimental_set_query_params()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Landing Page", "Tire Estimator", "Sales Sequence Chart"])

    if st.sidebar.button("Reset URL"):
        reset_url()

    if page == "Landing Page":
        st.title("Welcome to the Tire Management App")
        st.markdown("""
            <style>
                .main {text-align: center;}
            </style>
        """, unsafe_allow_html=True)

        st.write("## Manage Your Tire Shop Data")
        st.write("Easily manage your tire shop's data, including tire details, pricing information, and shop contact information.")
        
        with st.expander("Current Data"):
            st.json(data)

        with st.expander("Edit Data"):
            tires = st.text_area("Tires (JSON format)", value=json.dumps(st.session_state.tires, indent=4))
            brands = st.text_area("Brands (JSON format)", value=json.dumps(st.session_state.brands, indent=4))
            tax = st.number_input("Tax (%)", value=st.session_state.tax, key="tax_edit")
            surcharge = st.number_input("Surcharge ($)", value=st.session_state.surcharge, key="surcharge_edit")
            tire_markup = st.number_input("Tire Mark Up ($)", value=st.session_state.tire_markup, key="tire_markup_edit")
            nj_tire_tax = st.number_input("NJ Tire Tax ($)", value=st.session_state.nj_tire_tax, key="nj_tire_tax_edit")
            disposal_fee = st.number_input("Disposal Fee ($)", value=st.session_state.disposal_fee, key="disposal_fee_edit")
            start_price = st.number_input("Start Price", value=st.session_state.start_price, step=1, key="start_price_edit")
            end_price = st.number_input("End Price", value=st.session_state.end_price, step=1, key="end_price_edit")
            interval = st.number_input("Interval", value=st.session_state.interval, step=1, key="interval_edit")
            shop_name = st.text_input("Shop Name", value=st.session_state.shop_name, key="shop_name_edit")
            shop_address = st.text_input("Shop Address", value=st.session_state.shop_address, key="shop_address_edit")
            shop_phone = st.text_input("Shop Phone", value=st.session_state.shop_phone, key="shop_phone_edit")
            credit_card_fee = st.number_input("Credit Card Fee (%)", value=st.session_state.credit_card_fee, key="credit_card_fee_edit")

            if st.button("Save Data"):
                st.session_state.tires = json.loads(tires)
                st.session_state.brands = json.loads(brands)
                st.session_state.tax = tax
                st.session_state.surcharge = surcharge
                st.session_state.tire_markup = tire_markup
                st.session_state.nj_tire_tax = nj_tire_tax
                st.session_state.disposal_fee = disposal_fee
                st.session_state.start_price = start_price
                st.session_state.end_price = end_price
                st.session_state.interval = interval
                st.session_state.shop_name = shop_name
                st.session_state.shop_address = shop_address
                st.session_state.shop_phone = shop_phone
                st.session_state.credit_card_fee = credit_card_fee

                data_to_save = {
                    "tires": st.session_state.tires,
                    "brands": st.session_state.brands,
                    "tax": st.session_state.tax,
                    "surcharge": st.session_state.surcharge,
                    "tire_markup": st.session_state.tire_markup,
                    "nj_tire_tax": st.session_state.nj_tire_tax,
                    "disposal_fee": st.session_state.disposal_fee,
                    "start_price": st.session_state.start_price,
                    "end_price": st.session_state.end_price,
                    "interval": st.session_state.interval,
                    "shop_name": st.session_state.shop_name,
                    "shop_address": st.session_state.shop_address,
                    "shop_phone": st.session_state.shop_phone,
                    "credit_card_fee": st.session_state.credit_card_fee
                }
                save_data(data_to_save)
                st.success("Data saved successfully")

        with st.expander("Saved Data"):
            if st.button("Generate Shareable URL"):
                data_to_encode = {
                    "tires": st.session_state.tires,
                    "brands": st.session_state.brands,
                    "tax": st.session_state.tax,
                    "surcharge": st.session_state.surcharge,
                    "tire_markup": st.session_state.tire_markup,
                    "nj_tire_tax": st.session_state.nj_tire_tax,
                    "disposal_fee": st.session_state.disposal_fee,
                    "start_price": st.session_state.start_price,
                    "end_price": st.session_state.end_price,
                    "interval": st.session_state.interval,
                    "shop_name": st.session_state.shop_name,
                    "shop_address": st.session_state.shop_address,
                    "shop_phone": st.session_state.shop_phone,
                    "credit_card_fee": st.session_state.credit_card_fee
                }
                base64_str = encode_data_to_url(data_to_encode)
                shareable_url = f"https://oceanheights.streamlit.app/?data={base64_str}"
                st.write("Shareable URL:")
                st.code(shareable_url)

            st.write("## Download Data")
            json_str = json.dumps(data, indent=4)
            st.download_button(label="Download JSON", data=json_str, file_name="data.json", mime="application/json")

    elif page == "Tire Estimator":
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

        tire_estimator_page(st.session_state.tax, st.session_state.surcharge, st.session_state.tire_markup, st.session_state.nj_tire_tax, st.session_state.disposal_fee, st.session_state.credit_card_fee)

    elif page == "Sales Sequence Chart":
        with st.sidebar.expander("Sales Sequence Chart"):
            start_price = st.number_input("Start Price", value=st.session_state.start_price, step=1, key="start_price")
            end_price = st.number_input("End Price", value=st.session_state.end_price, step=1, key="end_price")
            interval = st.number_input("Interval", value=st.session_state.interval, step=1, key="interval")

        sales_sequence_page(int(start_price), int(end_price), int(interval), st.session_state.tax, st.session_state.surcharge, st.session_state.tire_markup, st.session_state.nj_tire_tax, st.session_state.disposal_fee, st.session_state.credit_card_fee)
