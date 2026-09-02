from datetime import datetime
import streamlit as st
import pandas as pd
from function_table_one import create_table_one #type: ignore
from function_table_two import create_table_two #type: ignore
from function_table_three import create_table_three #type: ignore
from function_table_two_graph import create_table_two_graph #type: ignore

_current_year = datetime.today().year

YEAR_T = str(_current_year)
YEAR_T_MINUS_ONE = str(_current_year - 1)
YEAR_T_MINUS_TWO = str(_current_year - 2)

st.set_page_config(layout="wide", page_title="Meetingplace kvartalsvist overblik over overnatninger")

table_one, latest_month_string, latest_year = create_table_one(YEAR_T, YEAR_T_MINUS_ONE, YEAR_T_MINUS_TWO)
table_two, table_two_top_3, table_two_bottom_3 = create_table_two(YEAR_T, YEAR_T_MINUS_ONE, YEAR_T_MINUS_TWO)
table_three = create_table_three(YEAR_T, YEAR_T_MINUS_ONE, YEAR_T_MINUS_TWO)

st.markdown("# Udviklingen i overnatninger i Region Hovedstaden (ekskl. Bornholm)")

status_total = 'vækst' if table_one['Vækst i pct.'].iloc[0] >= 0.00 else 'fald'
status_internationale = 'vækstet' if table_one['Vækst i pct.'].iloc[1] >= 0.00 else 'faldet'
status_danskere = 'vækstet' if table_one['Vækst i pct.'].iloc[2] >= 0.00 else 'faldet'
st.write(f"""
    I Jan.-{latest_month_string[:3]}. {latest_year} har regionen har haft en {status_total} i overnatninger på {table_one['Vækst i pct.'].iloc[0]:.1%}. 
    Internationale overnatninger er {status_internationale} med {table_one['Vækst i pct.'].iloc[1]:.1%}, imens at danske overnatninger er {status_danskere} med {table_one['Vækst i pct.'].iloc[2]:.1%}.
    {table_two_top_3.index[0]}, {table_two_top_3.index[1]} og {table_two_top_3.index[2]} er de markedet som er vækstet mest, med vækstrater på hhv. {table_two_top_3['Vækst i pct.'].iloc[0]/100:.1%}, {table_two_top_3['Vækst i pct.'].iloc[1]/100:.1%} og {table_two_top_3['Vækst i pct.'].iloc[2]/100:.1%}.
    Derimod er {table_two_bottom_3.index[0]}, {table_two_bottom_3.index[1]} og {table_two_bottom_3.index[2]} de markeder som er vækstet mindst, med vækstrater på hhv. {table_two_bottom_3['Vækst i pct.'].iloc[0]/100:.1%}, {table_two_bottom_3['Vækst i pct.'].iloc[1]/100:.1%} og {table_two_bottom_3['Vækst i pct.'].iloc[2]/100:.1%}.
""")

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

st.markdown("###### Figur 1:")
fig = create_table_two_graph(table_two)
st.plotly_chart(fig, width='stretch')