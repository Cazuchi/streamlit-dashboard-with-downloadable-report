import io
import pandas as pd
import streamlit as st
from fpdf import FPDF
from fpdf.fonts import FontFace

def create_pdf(headline, text_one, table_one, text_two, table_three, text_three, table_two_graph):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.multi_cell(0, 10, headline, new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.ln(2)

    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(
        0, 6,
        text_one
    )
    pdf.ln(2)

    table_one_data = [[""] + list(table_one.columns)]
    
    for idx, row in table_one.iterrows():
        formatted_row = [str(idx)]
        for col_name, val in row.items():
            if pd.isna(val):
                formatted_val = ""
            elif col_name in ['2025', '2026', 'Vækst i absolutte tal']:
                formatted_val = f"{val:,.0f}".replace(',', '.')
            elif col_name == 'Vækst i pct.':
                formatted_val = f"{val:.1%}".replace('.', ',')
            else:
                formatted_val = str(val)
            formatted_row.append(formatted_val)
        table_one_data.append(formatted_row)

    # 2. Define Table Styles
    # Dark green header (#0A3F19) with white bold text
    header_style = FontFace(
        color=(255, 255, 255),
        fill_color=(10, 63, 25),
        emphasis="BOLD"
    )
    
    # 3. Render Styled Table
    pdf.set_font("Helvetica", size=9)
    
    with pdf.table(
        col_widths=(25, 20, 20, 20, 20),  # Ratios: wider first column
        text_align=("LEFT", "RIGHT", "RIGHT", "RIGHT", "RIGHT"),  # Right-align numbers
        headings_style=header_style,
        line_height=7,                     # Vertical row height / padding
        padding=2,                         # Horizontal cell padding
        cell_fill_color=(245, 248, 245),   # Soft alternating row tint
        cell_fill_mode="ROWS"              # Enable zebra striping
    ) as table_one:
        for data_row in table_one_data:
            row = table_one.row()
            for datum in data_row:
                row.cell(datum)
    pdf.ln(2)

    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(
        0, 6,
        text_two
    )
    pdf.ln(2)

    table_three_data = [[""] + list(table_three.columns)]
        
    for idx, row in table_three.iterrows():
        formatted_row = [str(idx)]
        for col_name, val in row.items():
            if pd.isna(val):
                formatted_val = ""
            elif col_name in ['2025', '2026', 'Vækst i absolutte tal']:
                formatted_val = f"{val:,.0f}".replace(',', '.')
            elif col_name == 'Vækst i pct.':
                formatted_val = f"{val:.1%}".replace('.', ',')
            else:
                formatted_val = str(val)
            formatted_row.append(formatted_val)
        table_three_data.append(formatted_row)

    # 2. Define Table Styles
    # Dark green header (#0A3F19) with white bold text
    header_style = FontFace(
        color=(255, 255, 255),
        fill_color=(10, 63, 25),
        emphasis="BOLD"
    )
    
    # 3. Render Styled Table
    pdf.set_font("Helvetica", size=9)
    
    with pdf.table(
        col_widths=(25, 20, 20, 20, 20),  # Ratios: wider first column
        text_align=("LEFT", "RIGHT", "RIGHT", "RIGHT", "RIGHT"),  # Right-align numbers
        headings_style=header_style,
        line_height=7,                     # Vertical row height / padding
        padding=2,                         # Horizontal cell padding
        cell_fill_color=(245, 248, 245),   # Soft alternating row tint
        cell_fill_mode="ROWS"              # Enable zebra striping
    ) as table_three:
        for data_row in table_three_data:
            row = table_three.row()
            for datum in data_row:
                row.cell(datum)
    pdf.ln(2)

    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(
        0, 6,
        text_three
    )
    pdf.ln(2)
    
    img_bytes = table_two_graph.to_image(format="png", width=900, height=450, scale=2)
    pdf.image(io.BytesIO(img_bytes), w=180)

    return bytes(pdf.output())