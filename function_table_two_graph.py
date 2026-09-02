import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st

@st.cache_data(ttl=3600)
def create_table_two_graph(table_two):
    colors = ["#3BDA68" if val >= 0 else "#CF971E" for val in table_two['Vækst i pct.']]
    text_labels = [f"{val:.1f}%".replace('.', ',') for val in table_two['Vækst i pct.']]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=table_two.index,
            y=table_two['2026'],
            name='2026 overnatninger',
            marker_color='#0A3F19'
        ),
        secondary_y=False
    )

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

    fig.update_layout(
        template="plotly_white",
        margin=dict(t=30, b=40, l=40, r=40),
        legend=dict(
            orientation="h",
            xanchor="center",
            x=0.5,
            yanchor="top",
            y=-0.15
        )
    )

    fig.update_yaxes(title_text="2026 overnatninger", range=[0, table_two['2026'].max() * 1.20], secondary_y=False, showgrid=False)
    fig.update_yaxes(title_text="Vækst i pct.", range=[table_two['Vækst i pct.'].min() * 1.40, table_two['Vækst i pct.'].max() * 1.40], secondary_y=True, showgrid=False, zeroline=False)
    fig.update_xaxes(showgrid=False)
    return fig