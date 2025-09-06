import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("data/articles.db")
df = pd.read_sql_query("SELECT published, category FROM articles", conn)

df['published'] = pd.to_datetime(df['published'], errors='coerce', utc=True)
df = df.dropna(subset=['published'])
df['published'] = df['published'].dt.tz_localize(None)
df['week'] = df['published'].dt.to_period('W')

weekly = df.groupby(['week', 'category']).size().unstack(fill_value=0)

# Convert Period index to string for Streamlit
weekly.index = weekly.index.astype(str)

st.line_chart(weekly)
