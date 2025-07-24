import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

response = supabase.table("logs").select("*").order("timestamp", desc=True).limit(100).execute()
df = pd.DataFrame(response.data)

st.title("Productivity Dashboard")

# Show a warning if no logs are found
if df.empty:
    st.warning("No entries yet. Go to the Home page to start logging!")
    st.stop()

# Convert date for easier plotting
df['date'] = pd.to_datetime(df['date'])

# Sidebar filters
with st.sidebar:
    st.header("Filter your entries")
    productivity_filter = st.multiselect("Filter by productivity:", df['productivity'].unique(), default=list(df['productivity'].unique()))
    mood_filter = st.multiselect("Filter by mood:", df['mood'].unique(), default=list(df['mood'].unique()))

    df = df[df['productivity'].isin(productivity_filter)]
    df = df[df['mood'].isin(mood_filter)]

# Mood Distribution
st.subheader("Mood Distribution")
mood_counts = df['mood'].value_counts()
st.bar_chart(mood_counts)

# Productivity Over Time
st.subheader("Productivity Over Time")
prod_over_time = df.groupby(['date', 'productivity']).size().unstack().fillna(0)
st.line_chart(prod_over_time)

# Average Energy Over Time
st.subheader("Average Energy Level Over Time")
avg_energy = df.groupby('date')['energy'].mean()
st.line_chart(avg_energy)

# Recent Logs Table
st.subheader("Recent Entries")
st.dataframe(df.sort_values(by="timestamp", ascending=False).reset_index(drop=True))