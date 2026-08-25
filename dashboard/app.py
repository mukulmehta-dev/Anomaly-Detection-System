import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:password@localhost:5432/anomalydb")

st.title("🚨 Anomaly Detection Dashboard")

df = pd.read_sql("SELECT * FROM alerts ORDER BY created_at DESC", engine)

st.metric("Total Alerts", len(df))
st.metric("High Risk", len(df[df['priority'] == 'HIGH']))

st.dataframe(df)
st.bar_chart(df['priority'].value_counts())
