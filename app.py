import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib import colors
from datetime import datetime
import os

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
        styled_df = df.style.apply(lambda x: ['background-color: #f5f5f5' if i % 2 == 0 else 'background-color: #ffffff' for i in range(len(x))], axis=0)
        st.dataframe(styled_df, use_container_width=True)

        if st.button("Generate PDF"):
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"Sales_Sequence_Chart_{now}.pdf"
            generate_pdf(df, start_price, end_price, interval, tax, surcharge, tire_markup, nj_tire_tax, disposal_fee, credit_card_fee, filename)
            with open(filename, "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            st.download_button(
                label="Download PDF",
                data=PDFbyte,
                file_name=filename,
                mime='application/octet-stream'
            )
            os.remove(filename)

def generate_pdf(df, start_price, end_price, interval, tax, surcharge, tire_markup, nj_tire_tax, disposal_fee, credit_card_fee, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    # First page with variables and equations
    elements.append(Table([
        ["Tire Sales Sequence Chart Variables and Equations"],
        ["Start Price:", f"${start_price}"],
        ["End Price:", f"${end_price}"],
        ["Interval:", f"${interval}"],
        ["Tax:", f"{tax}%"],
        ["Surcharge:", f"${surcharge}"],
        ["Tire Markup:", f"${tire_markup}"],
        ["NJ Tire Tax:", f"${nj_tire_tax}"],
        ["Disposal Fee:", f"${disposal_fee}"],
        ["Credit Card Fee:", f"{credit_card_fee}%"],
        ["Total Cost = (Tire Cost + Fees) * (1 + Tax / 100) * (1 + Credit Card Fee / 100)"]
    ], style=[
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(PageBreak())

    # Subsequent pages with tables in portrait mode
    table_data = [df.columns.values.tolist()] + df.values.tolist()
    table = Table(table_data, repeatRows=1, colWidths=[(letter[0]-60)/9.0]*9)
    alternating_colors = [('BACKGROUND', (0, i), (-1, i), colors.whitesmoke if i % 2 == 0 else colors.beige) for i in range(1, len(table_data))]
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (2, 1), (2, -1), 'Helvetica-Bold'),
        ('FONTNAME', (4, 1), (4, -1), 'Helvetica-Bold'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
    ] + alternating_colors))
    
    elements.append(table)
    
    doc.build(elements)
