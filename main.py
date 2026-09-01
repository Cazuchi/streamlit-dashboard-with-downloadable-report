from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from function_table_one import create_table_one
from function_table_two import create_table_two

_current_year = datetime.today().year

YEAR_T = str(_current_year)
YEAR_T_MINUS_ONE = str(_current_year - 1)
YEAR_T_MINUS_TWO = str(_current_year - 2)

st.set_page_config(layout="wide", page_title="Meetingplace kvartalsvist overblik over overnatninger")

table_one, latest_month_string, latest_year = create_table_one(YEAR_T, YEAR_T_MINUS_ONE, YEAR_T_MINUS_TWO)
table_two = create_table_two(YEAR_T, YEAR_T_MINUS_ONE, YEAR_T_MINUS_TWO)

st.markdown("# Udviklingen i overnatninger i Region Hovedstaden (ekskl. Bornholm)")

status_total = 'vækst' if table_one['Vækst i pct.'].iloc[0] >= 0.00 else 'fald'
status_internationale = 'vækstet' if table_one['Vækst i pct.'].iloc[1] >= 0.00 else 'faldet'
status_danskere = 'vækstet' if table_one['Vækst i pct.'].iloc[2] >= 0.00 else 'faldet'
st.write(f"""
    I Jan.-{latest_month_string[:3]}. {latest_year} har regionen har haft en {status_total} i overnatninger på {table_one['Vækst i pct.'].iloc[0]:.1%}. 
    Internationale overnatninger er {status_internationale} med {table_one['Vækst i pct.'].iloc[1]:.1%}, imens at danske overnatninger er {status_danskere} med {table_one['Vækst i pct.'].iloc[2]:.1%}.
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

st.markdown("###### Figur 1:")
# 1. Dynamic colors & formatted labels (Danish decimal separator)
colors = ["#3BDA68" if val >= 0 else "#CF971E" for val in table_two['Vækst i pct.']]  # Green / Orange
text_labels = [f"{val:.1f}%".replace('.', ',') for val in table_two['Vækst i pct.']]

# 2. Create dual-axis figure
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Primary Axis: 2026 Bars
fig.add_trace(
    go.Bar(
        x=table_two.index,
        y=table_two['2026'],
        name='2026 overnatninger',
        marker_color='#0A3F19'
    ),
    secondary_y=False
)

# Secondary Axis: Growth Markers + Data Labels
fig.add_trace(
    go.Scatter(
        x=table_two.index,
        y=table_two['Vækst i pct.'],
        name='Vækst i pct.',
        mode='markers+text',
        marker=dict(color=colors, size=10),
        text=text_labels,
        textposition='top center',
        textfont=dict(color=colors, size=12, family="Arial")
    ),
    secondary_y=True
)

# 3. Adjust layout & padding for labels
fig.update_layout(
    template="plotly_white",
    margin=dict(t=30, b=40, l=40, r=40),
    legend=dict(
        orientation="h",
        xanchor="center",
        x=0.5,
        yanchor="top",
        y=-0.15  # Negative value pushes it below the x-axis
    )
)

fig.update_yaxes(title_text="2026 overnatninger", range=[0, table_two['2026'].max() * 1.20], secondary_y=False, showgrid=False)
fig.update_yaxes(title_text="Vækst i pct.", range=[table_two['Vækst i pct.'].min() * 1.40, table_two['Vækst i pct.'].max() * 1.40], secondary_y=True, showgrid=False, zeroline=False)
fig.update_xaxes(showgrid=False)

# Render in Streamlit
st.plotly_chart(fig, use_container_width=True)