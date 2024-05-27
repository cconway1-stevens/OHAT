import streamlit as st
import pandas as pd

def calculate_cost(tire_cost, tax, surcharge, tire_markup, nj_tire_tax, disposal_fee):
    fees = tire_markup + nj_tire_tax + disposal_fee + surcharge
    total_with_tax = (tire_cost + fees) * (1 + tax / 100)
    return round(total_with_tax, 2)

def generate_sales_sequence(start_price, end_price, interval, tax, surcharge, tire_markup, nj_tire_tax, disposal_fee):
    if (end_price - start_price) % interval != 0:
        st.error("The interval must evenly divide the range between the start and end prices.")
        return None
    
    prices = list(range(start_price, end_price + 1, interval))
    data = []
    
    for price in prices:
        fees = tire_markup + nj_tire_tax + disposal_fee + surcharge
        w_tax = calculate_cost(price, tax, surcharge, tire_markup, nj_tire_tax, disposal_fee)
        total_1 = w_tax
        total_2 = w_tax * 2
        total_3 = w_tax * 3
        total_4 = w_tax * 4
        data.append([price, fees, round(w_tax - price, 2), round(w_tax, 2), round(total_4, 2), round(total_3, 2), round(total_2, 2), round(total_1, 2)])
    
    return pd.DataFrame(data, columns=["Cost", "Fees", "W/tax", "Total", "4", "3", "2", "1"])

def sales_sequence_page(start_price, end_price, interval, tax, surcharge, tire_markup, nj_tire_tax, disposal_fee):
    st.title("Sales Sequence Chart")

    df = generate_sales_sequence(start_price, end_price, interval, tax, surcharge, tire_markup, nj_tire_tax, disposal_fee)
    if df is not None:
        st.write("## Generated Sequence Table")
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    st.sidebar.title("Sales Sequence Parameters")
    start_price = st.sidebar.number_input("Start Price", value=100, step=1, key="start_price")
    end_price = st.sidebar.number_input("End Price", value=500, step=1, key="end_price")
    interval = st.sidebar.number_input("Interval", value=10, step=1, key="interval")
    tax = st.sidebar.number_input("Tax (%)", value=6.625, key="tax")
    surcharge = st.sidebar.number_input("Surcharge ($)", value=5.0, key="surcharge")
    tire_markup = st.sidebar.number_input("Tire Mark Up ($)", value=67.0, key="tire_markup")
    nj_tire_tax = st.sidebar.number_input("NJ Tire Tax ($)", value=1.5, key="nj_tire_tax")
    disposal_fee = st.sidebar.number_input("Disposal Fee ($)", value=7.0, key="disposal_fee")

    sales_sequence_page(int(start_price), int(end_price), int(interval), tax, surcharge, tire_markup, nj_tire_tax, disposal_fee)
