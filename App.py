import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def hhmm_to_minutes(hhmm):
    h, m = map(int, hhmm.split(":"))
    return h * 60 + m

df_all = pd.read_csv(r"https://raw.githubusercontent.com/bkaanulgen/Aligner/refs/heads/main/csv/All.csv", sep=';')
df_sum = pd.read_csv(r"https://raw.githubusercontent.com/bkaanulgen/Aligner/refs/heads/main/csv/Sum.csv", sep=';')
df_cycle = pd.read_csv(r"https://raw.githubusercontent.com/bkaanulgen/Aligner/refs/heads/main/csv/Cycle.csv", sep=';')

df_sum['Toplam Dakika'] = df_sum['Toplam Süre'].apply(hhmm_to_minutes)
recommended_minutes = hhmm_to_minutes('02:00')


fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_sum['Tarih'],
    y=df_sum['Toplam Dakika'],
    mode='lines+markers+text',  # dotted line + dots + labels
    name='Toplam Süre',
    line=dict(color='darkblue', dash='dot'),
    marker=dict(color='darkblue', size=8),
    text=df_sum['Toplam Dakika'],  # Show HH:MM above points
    textposition='top center'
))



st.title('Filiz🌱 Plak Takibi')

with st.container():
    # st.plotly_chart(fig)
    st.dataframe(df_all.fillna(''))
    # st.dataframe(df_sum)
    # st.dataframe(df_cycle)