import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go

def hhmm_to_minutes(hhmm):
    h, m = map(int, hhmm.split(':'))
    return h * 60 + m


df_all = pd.read_csv(r"https://raw.githubusercontent.com/bkaanulgen/Aligner/refs/heads/main/csv/All.csv", sep=';')
df_sum = pd.read_csv(r"https://raw.githubusercontent.com/bkaanulgen/Aligner/refs/heads/main/csv/Sum.csv", sep=';')
df_cycle = pd.read_csv(r"https://raw.githubusercontent.com/bkaanulgen/Aligner/refs/heads/main/csv/Cycle.csv", sep=';')

df_sum['Toplam Dakika'] = df_sum['Toplam Süre'].apply(hhmm_to_minutes)
df_cycle['Çıkarılan Dakika'] = df_cycle['Çıkarılan Süre'].apply(hhmm_to_minutes)
recommended_minutes = hhmm_to_minutes('02:00')


st.set_page_config(
    page_title='Filiz🌱 Plak Takibi',
    layout='wide',
    page_icon='🌱',
    initial_sidebar_state='expanded'
)

st.title('Filiz🌱 Plak Takibi')
st.subheader('Günlük Toplam Çıkarılma Süreleri')


xaxis = alt.Axis(format='%b %Y', tickCount=df_sum['Tarih'].apply(lambda x: x[5:7]).nunique())
points = alt.Chart(df_sum).mark_point(filled=True, color='#003366', size=40).encode(
    x=alt.X('Tarih:T', title='Tarih'),
    y=alt.Y('Toplam Dakika:Q', title='Toplam Dakika'),
    tooltip=['Tarih', 'Toplam Dakika']
)

# Text labels
labels = points.mark_text(
    align='center',
    baseline='bottom',
    dy=-5,  # shift text slightly above points
    fontSize=12,
    color='black'
).encode(
    text=alt.Text('Toplam Süre:O')  # format to HH:MM
)

line = alt.Chart(df_sum).mark_line(
    color='#003366',      # Same deep blue
    strokeDash=[2, 4],    # Dotted line pattern: [dash_length, gap_length]
    strokeWidth=2,
    opacity=0.5          # <-- Transparency for points (0.0 to 1.0)
).encode(
    x=alt.X('Tarih:T', axis=xaxis, title='Tarih'),
    y=alt.Y('Toplam Dakika:Q', title='Toplam Dakika'),
)

# **Horizontal reference line at y = 120**
ref_line = alt.Chart(pd.DataFrame({'Tarih': df_sum['Tarih'], 'Toplam Dakika': [120] * len(df_sum)})).mark_line(
    color='red',
    strokeDash=[2, 4],   # Dotted red line
    strokeWidth=2,
    opacity=0.3         # <-- Transparency for points (0.0 to 1.0)
).encode(
    x=alt.X('Tarih:T', axis=xaxis, title='Tarih'),
    y=alt.Y('Toplam Dakika:Q', title='Toplam Dakika'),
)

# Combine
chart = (ref_line + line + points + labels).properties(
    title="Günlük Toplam Çıkarılma Süresi",
    width=len(df_sum)*25,
    height=500
)

# Put chart in a horizontally scrollable container
st.markdown(
    """
    <div style="overflow-x: auto; white-space: nowrap;">
    """,
    unsafe_allow_html=True
)

st.altair_chart(chart, use_container_width=False)

st.markdown("</div>", unsafe_allow_html=True)



# Create bar chart
bars = alt.Chart(df_cycle).mark_bar(color = "#0c3552").encode(
    x=alt.X('Tarih:N', title='Tarih'),
    y=alt.Y('Çıkarılan Dakika:Q', title='Çıkarılan Süre')
    ).properties(
    title='Plak Süre',
    height=600
)

bar_labels = bars.mark_text(
    align='center',
    baseline='bottom',
    dy=-5,  # shift text slightly above points
    fontSize=12,
    color="#0c3552",
    fontWeight='bold'
).encode(
    text=alt.Text('Çıkarılan Süre:O')  # format to HH:MM
)

bar_chart = (bars + bar_labels).properties(
    title="Günlük Toplam Çıkarılma Süresi",
    width=len(df_sum)*25,
    height=500
)

st.altair_chart(bar_chart)


st.subheader('Plak Bazında Veriler')
st.dataframe(df_cycle.iloc[::-1].reset_index(drop=True))

st.subheader('Gün Bazında Veriler')
st.dataframe(df_sum.drop('Toplam Dakika', axis=1).iloc[::-1].reset_index(drop=True))

st.subheader('Tüm Veriler')
st.dataframe(df_all.fillna('').iloc[::-1].reset_index(drop=True))
