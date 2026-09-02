from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from function_table_one import create_table_one #type: ignore
from function_table_two import create_table_two #type: ignore
from function_table_three import create_table_three #type: ignore
from function_table_two_graph import create_table_two_graph #type: ignore
from function_create_pdf import create_pdf #type: ignore

_current_year = datetime.today().year

YEAR_T = str(_current_year)
YEAR_T_MINUS_ONE = str(_current_year - 1)
YEAR_T_MINUS_TWO = str(_current_year - 2)

st.set_page_config(layout="wide", page_title="Meetingplace kvartalsvist overblik over overnatninger")

table_one, latest_month_string, latest_year = create_table_one(YEAR_T, YEAR_T_MINUS_ONE, YEAR_T_MINUS_TWO)
table_two, table_two_top_3, table_two_bottom_3 = create_table_two(YEAR_T, YEAR_T_MINUS_ONE, YEAR_T_MINUS_TWO)
table_three = create_table_three(YEAR_T, YEAR_T_MINUS_ONE, YEAR_T_MINUS_TWO)
table_two_graph = create_table_two_graph(table_two)

headline = f"Udviklingen i overnatninger i Region Hovedstaden (ekskl. Bornholm) Jan.-{latest_month_string[:3]}. {latest_year}"
status_total = 'en vækst' if table_one['Vækst i pct.'].iloc[0] >= 0.00 else 'et fald'
status_internationale = 'vækstet' if table_one['Vækst i pct.'].iloc[1] >= 0.00 else 'faldet'
status_danskere = 'vækstet' if table_one['Vækst i pct.'].iloc[2] >= 0.00 else 'faldet'
text_one = f"""
I Jan.-{latest_month_string[:3]}. {latest_year} har regionen har haft {status_total} i overnatninger på {table_one['Vækst i pct.'].iloc[0]:.1%}. Internationale overnatninger er {status_internationale} med {table_one['Vækst i pct.'].iloc[1]:.1%}, imens at danske overnatninger er {status_danskere} med {table_one['Vækst i pct.'].iloc[2]:.1%}.

{table_two_top_3.index[0]} ({table_two_top_3['Vækst i pct.'].iloc[0]/100:.1%}), {table_two_top_3.index[1]} ({table_two_top_3['Vækst i pct.'].iloc[1]/100:.1%}) og {table_two_top_3.index[2]} ({table_two_top_3['Vækst i pct.'].iloc[2]/100:.1%}) er de markeder som er vækstet mest, imens at {table_two_bottom_3.index[0]} ({table_two_bottom_3['Vækst i pct.'].iloc[0]/100:.1%}), {table_two_bottom_3.index[1]} ({table_two_bottom_3['Vækst i pct.'].iloc[1]/100:.1%}) og {table_two_bottom_3.index[2]} ({table_two_bottom_3['Vækst i pct.'].iloc[2]/100:.1%}) de markeder som er vækstet mindst.
"""
status_total_hotel = 'en vækst' if table_three['Vækst i pct.'].iloc[0] >= 0.00 else 'et fald'
status_ferie_hotel = 'vækstet' if table_three['Vækst i pct.'].iloc[1] >= 0.00 else 'faldet'
status_forretning_hotel = 'vækstet' if table_three['Vækst i pct.'].iloc[2] >= 0.00 else 'faldet'
text_two = f"""
For hoteller specifikt, har regionen i Jan.-{latest_month_string[:3]}. {latest_year} haft {status_total_hotel} i overnatninger på {table_three['Vækst i pct.'].iloc[0]:.1%}. Ferie-relaterede overnatninger er {status_ferie_hotel} med {table_three['Vækst i pct.'].iloc[1]:.1%}, imens at forretningsovernatninger er {status_forretning_hotel} med {table_three['Vækst i pct.'].iloc[2]:.1%}.
"""
status_table_three_kina = 'vækstet' if table_two['Vækst i pct.'].loc[(table_two.index == 'Kina*')].iloc[0] >= 0 else "faldet"
status_table_three_indien = 'vækstet' if table_two['Vækst i pct.'].loc[(table_two.index == 'Indien*')].iloc[0] >= 0 else "faldet"
text_three = f"""
Ser man på de individuelle, internationale markeders vækst i Jan.-{latest_month_string[:3]}. {latest_year}, er {len(table_two.loc[(~table_two.index.isin(['Kina*', 'Indien*'])) & (table_two['Vækst i pct.'] > 0)])} af vores top 10 markeder ift. {YEAR_T_MINUS_ONE}. Samtidig er det kinesiske marked er {status_table_three_kina} med {table_two['Vækst i pct.'].loc[(table_two.index == 'Kina*')].iloc[0]/100:.1%}, imens at det indiske marked er {status_table_three_indien} med {table_two['Vækst i pct.'].loc[(table_two.index == 'Indien*')].iloc[0]/100:.1%}.
"""

pdf_bytes = create_pdf(headline, text_one, table_one, text_two, table_three, text_three, table_two_graph)

st.download_button(
    label="Download PDF rapport",
    data=pdf_bytes,
    file_name="rapport_overnatninger.pdf",
    mime="application/pdf"
)

st.markdown(f"# {headline}")

st.write(text_one)

st.markdown("###### Tabel 1:")
st.dataframe(
    table_one.style.format({
    '2025' : '{:,.0f}',
    '2026' : '{:,.0f}',
    'Vækst i absolutte tal' : '{:,.0f}',
    'Vækst i pct.' : '{:.1%}'
    },
    thousands=".",
    decimal=",",),
    width='content'
)

st.write(text_two)

st.markdown("###### Tabel 2:")
st.dataframe(
    table_three.style.format({
    '2025' : '{:,.0f}',
    '2026' : '{:,.0f}',
    'Vækst i absolutte tal' : '{:,.0f}',
    'Vækst i pct.' : '{:.1%}'
    },
    thousands=".",
    decimal=",",),
    width='content'
)

st.write(text_three)

st.markdown("###### Figur 1:")
st.plotly_chart(table_two_graph, width='stretch')