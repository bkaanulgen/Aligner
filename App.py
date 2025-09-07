import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def hhmm_to_minutes(hhmm):
    h, m = map(int, hhmm.split(':'))
    return h * 60 + m

df_all = pd.read_csv(r"https://raw.githubusercontent.com/bkaanulgen/Aligner/refs/heads/main/csv/All.csv", sep=';')
df_sum = pd.read_csv(r"https://raw.githubusercontent.com/bkaanulgen/Aligner/refs/heads/main/csv/Sum.csv", sep=';')
df_cycle = pd.read_csv(r"https://raw.githubusercontent.com/bkaanulgen/Aligner/refs/heads/main/csv/Cycle.csv", sep=';')

df_sum['Toplam Dakika'] = df_sum['Toplam Süre'].apply(hhmm_to_minutes)
recommended_minutes = hhmm_to_minutes('02:00')


st.set_page_config(
    page_title='Filiz🌱 Plak Takibi',
    layout='wide',
    page_icon='🌱',
    initial_sidebar_state='expanded'
)

st.title('Filiz🌱 Plak Takibi')
st.subheader('Günlük Toplam Çıkarılma Süreleri')

sum_show_labels = st.radio(
    'Veri Etiketlerini Göster / Gizle:',
    ('Göster', 'Gizle')
)
sum_text_values = df_sum['Toplam Süre'] if sum_show_labels == 'Göster' else None


fig = go.Figure()

# Red dotted straight line at 02:00
fig.add_trace(go.Scatter(
    x=df_sum['Tarih'],
    y=[recommended_minutes] * len(df_sum),
    mode='lines',
    name='Tavsiye Edilen Süre',
    line=dict(color='red', dash='dot', width=1.2),
    opacity=0.8
))

fig.add_trace(go.Scatter(
    x=df_sum['Tarih'],
    y=df_sum['Toplam Dakika'],
    mode='lines',  # dotted line + dots + labels
    name='Toplam Süre',
    line=dict(color='#1c4587', dash='dot', width=1),
    opacity=0.75,
))

fig.add_trace(go.Scatter(
    x=df_sum['Tarih'],
    y=df_sum['Toplam Dakika'],
    mode='markers+text',  # dotted line + dots + labels
    showlegend=False,
    line=dict(color='#1c4587', dash='dot'),
    marker=dict(color='#1c4587', size=6),
    text=sum_text_values,  # Show HH:MM above points
    textposition='top center',
    textfont=dict(size=14, color='#363a40')
))

# Layout
fig.update_layout(
    # title='Günlük Toplam Çıkarılma Süresi',
    xaxis_title='Tarih',
    yaxis_title='Süre  ( Saat : Dakika )',
    legend_title='Veriler',
    template='simple_white',
    # height=500
    autosize=True,
)

st.plotly_chart(fig)

st.subheader('Plak Bazında Veriler')
st.dataframe(df_cycle)

st.subheader('Gün Bazında Veriler')
st.dataframe(df_sum.drop('Toplam Dakika', axis=1))

st.subheader('Tüm Veriler')
st.dataframe(df_all.fillna(''))