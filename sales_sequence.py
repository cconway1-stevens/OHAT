import streamlit as st
import pandas as pd

def calculate_cost(tire_cost, tax, surcharge, tire_markup, nj_tire_tax, disposal_fee, credit_card_fee):
    fees = tire_markup + nj_tire_tax + disposal_fee + surcharge
    total_with_tax = (tire_cost + fees) * (1 + tax / 100)
    total_with_credit_card_fee = total_with_tax * (1 + credit_card_fee / 100)
    return round(total_with_credit_card_fee, 2)

def generate_sales_sequence(start_price, end_price, interval, tax, surcharge, tire_markup, nj_tire_tax, disposal_fee, credit_card_fee):
    if (end_price - start_price) % interval != 0:
        st.error("The interval must evenly divide the range between the start and end prices.")
        return None
    
    prices = list(range(start_price, end_price + 1, interval))
    data = []
    
    for price in prices:
        fees = tire_markup + nj_tire_tax + disposal_fee + surcharge
        w_tax = calculate_cost(price, tax, surcharge, tire_markup, nj_tire_tax, disposal_fee, credit_card_fee)
        total_1 = w_tax
        total_2 = w_tax * 2
        total_3 = w_tax * 3
        total_4 = w_tax * 4
        data.append([price, fees, round(w_tax - price, 2), round(w_tax, 2), round(total_4, 2), round(total_3, 2), round(total_2, 2), round(total_1, 2)])
    
    return pd.DataFrame(data, columns=["Cost", "Fees", "W/tax", "Total", "4", "3", "2", "1"])

def sales_sequence_page(start_price, end_price, interval, tax, surcharge, tire_markup, nj_tire_tax, disposal_fee, credit_card_fee):
    st.title("Sales Sequence Chart")

    df = generate_sales_sequence(start_price, end_price, interval, tax, surcharge, tire_markup, nj_tire_tax, disposal_fee, credit_card_fee)
    if df is not None:
        st.write("## Generated Sequence Table")
        st.dataframe(df, use_container_width=True)
