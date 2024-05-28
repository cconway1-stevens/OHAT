import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime

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
    c = canvas.Canvas(filename, pagesize=letter)
    
    # First page with variables and equations
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, 750, "Tire Sales Sequence Chart Variables and Equations")
    c.setFont("Helvetica", 12)
    c.drawString(30, 720, f"Start Price: ${start_price}")
    c.drawString(30, 700, f"End Price: ${end_price}")
    c.drawString(30, 680, f"Interval: ${interval}")
    c.drawString(30, 660, f"Tax: {tax}%")
    c.drawString(30, 640, f"Surcharge: ${surcharge}")
    c.drawString(30, 620, f"Tire Markup: ${tire_markup}")
    c.drawString(30, 600, f"NJ Tire Tax: ${nj_tire_tax}")
    c.drawString(30, 580, f"Disposal Fee: ${disposal_fee}")
    c.drawString(30, 560, f"Credit Card Fee: {credit_card_fee}%")
    c.drawString(30, 520, "Total Cost = (Tire Cost + Fees) * (1 + Tax / 100) * (1 + Credit Card Fee / 100)")

    c.showPage()
    
    # Subsequent pages with tables in landscape mode
    c.setPageSize(landscape(letter))
    width, height = landscape(letter)

    table_data = [df.columns.values.tolist()] + df.values.tolist()
    table = Table(table_data, colWidths=[width/8.0]*8)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    table.wrapOn(c, width, height)
    table.drawOn(c, 30, height - len(table_data) * 20)
    
    c.save()
