import streamlit as st
import pandas as pd
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

def calculate_cost(tire_cost, tax, surcharge, tire_markup, nj_tire_tax, disposal_fee):
    fees = tire_markup + nj_tire_tax + disposal_fee + surcharge
    total_with_tax = (tire_cost + fees) * (1 + tax / 100)
    return round(total_with_tax, 2)

def generate_pdf(df, notes, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    margin = 30
    padding = 10

    # Draw bounding box
    c.rect(margin - padding, margin - padding, width - 2 * margin + 2 * padding, height - 2 * margin + 2 * padding)

    # Title and Header Information
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, height - 40, "Tire Pricing Estimate")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, height - 70, "Ocean Heights Auto and Tire")
    c.drawString(margin, height - 85, "1178 Ocean Heights Avenue, Egg Harbor Township, NJ 08234")
    c.drawString(margin, height - 100, "Phone: (609) 241-1546")

    c.line(margin, height - 110, width - margin, height - 110)  # Line separator

    # Calculate column positions and widths
    num_cols = len(df.columns)
    col_width = (width - 2 * margin) / num_cols
    x_positions = [margin + col_width * i for i in range(num_cols)]

    # Table headers
    y = height - 130
    c.setFont("Helvetica-Bold", 12)
    for i, col in enumerate(df.columns):
        c.drawString(x_positions[i], y, col)

    # Table rows
    c.setFont("Helvetica", 12)
    y = height - 150
    row_height = 20  # Adjust row height
    for _, row in df.iterrows():
        if y < margin + 60:  # Check if there's enough space for the next row and footer
            c.showPage()
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin, height - 40, "Tire Pricing Estimate (Continued)")

            # Table headers on new page
            y = height - 70
            c.setFont("Helvetica-Bold", 12)
            for i, col in enumerate(df.columns):
                c.drawString(x_positions[i], y, col)
            y -= row_height
            c.setFont("Helvetica", 12)
        
        for i, col in enumerate(df.columns):
            value = row[col]
            if isinstance(value, float):
                value = f"${value:.2f}"  # Format as currency
            c.drawString(x_positions[i], y, str(value))
        y -= row_height

    # Footer Information
    if y < margin + 80:
        c.showPage()
        y = height - 40

    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, " ")

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(1, 0, 0)  # Red color for promotion
    c.drawString(margin, y, "Promotion: Buy 4 tires and get a free alignment and tire rotation.")

    y -= 20
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0, 0, 0)  # Reset color to black
    c.drawString(margin, y, "Legal Disclaimer: This estimate is not a contract. Prices and availability are subject to change.")
    c.drawString(margin, y - 10, "Please contact us for the most up-to-date pricing and availability.")

    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Additional Notes:")
    y -= 20
    c.setFont("Helvetica", 10)
    for line in wrap(notes, width=100):
        c.drawString(margin, y, line)
        y -= 15

    c.save()

def tire_estimator_page(tax, surcharge, tire_markup, nj_tire_tax, disposal_fee):
    st.title("Tire Pricing Estimator")

    st.write("## Tire List")
    if st.session_state.tires:
        tire_df = pd.DataFrame(st.session_state.tires)

        gb = GridOptionsBuilder.from_dataframe(tire_df)
        gb.configure_pagination()
        gb.configure_default_column(editable=True)
        grid_options = gb.build()

        response = AgGrid(
            tire_df,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            editable=True,
            fit_columns_on_grid_load=True
        )

        # Update session state with the edited table
        st.session_state.tires = response['data'].to_dict('records')

    else:
        st.write("No tires added yet.")

    notes = st.text_area("Additional Notes")

    if st.button("Generate Estimates"):
        estimates = []
        for tire in st.session_state.tires:
            costs = [round(calculate_cost(tire['cost'], tax, surcharge, tire_markup, nj_tire_tax, disposal_fee) * qty, 2) for qty in range(1, 5)]
            estimates.append([tire['name'], tire['brand']] + costs)

        estimate_df = pd.DataFrame(estimates, columns=["Tire Name", "Tire Brand", "1 Tire", "2 Tires", "3 Tires", "4 Tires"])
        st.write("## Estimates")
        st.write(estimate_df)

        # Save the generated estimate DataFrame in session state
        st.session_state.estimate_df = estimate_df
        st.session_state.notes = notes

    # Combine PDF generation and download into one button
    if 'estimate_df' in st.session_state:
        # Generate filename with current date and time
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Ocean Heights Tire EST - {now}.pdf"
        generate_pdf(st.session_state.estimate_df, st.session_state.notes, filename)
        with open(filename, "rb") as pdf_file:
            PDFbyte = pdf_file.read()
        st.download_button(
            label="Download PDF",
            data=PDFbyte,
            file_name=filename,
            mime='application/octet-stream'
        )
        # Remove the PDF file after download
        os.remove(filename)
