import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from datetime import datetime
from src.database import engine, SessionLocal, Alert
from src.feature_engineering import create_features
from src.statistical_methods import z_score_detection, mahalanobis_distance
from src.ml_models import isolation_forest, lof_detection
from src.time_series import arima_residuals
from src.ensemble import ensemble_score
from src.alerting import generate_alerts

st.set_page_config(
    page_title="Anomaly Detection Dashboard",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚨 Real-Time Anomaly Detection Dashboard")
st.markdown("Monitor transaction anomalies, risk tiers, statistical deviations, and live alerts.")

# Sidebar - Test Transaction Simulator
st.sidebar.header("🧪 Test Transaction Simulator")
st.sidebar.markdown("Submit a transaction to evaluate anomaly scores in real-time.")

with st.sidebar.form("simulate_tx_form"):
    test_user = st.number_input("User ID", min_value=100, max_value=999, value=101, step=1)
    test_amount = st.number_input("Transaction Amount ($)", min_value=1.0, max_value=1000000.0, value=75000.0, step=500.0)
    test_hour = st.slider("Hour of Day (0-23)", min_value=0, max_value=23, value=2)
    submitted = st.form_submit_button("⚡ Evaluate Transaction", use_container_width=True)

if submitted:
    try:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed_transactions.csv")
        df_hist = pd.read_csv(data_path)
        df_hist['timestamp'] = pd.to_datetime(df_hist['timestamp'])
        
        sim_time = datetime.now().replace(hour=test_hour, minute=0, second=0)
        tx_row = {"user_id": test_user, "amount": test_amount, "timestamp": sim_time}
        df_all = pd.concat([df_hist, pd.DataFrame([tx_row])], ignore_index=True)
        
        df_all = create_features(df_all)
        FEATURES = ['amount_log', 'hour', 'day']
        df_all['z_score'] = z_score_detection(df_all, 'amount')
        df_all['mahalanobis'] = mahalanobis_distance(df_all, FEATURES)
        df_all['iso_score'] = isolation_forest(df_all, FEATURES)
        df_all['lof_score'] = lof_detection(df_all, FEATURES)
        df_all['arima_resid'] = arima_residuals(df_all['amount'])
        df_all = ensemble_score(df_all)
        df_all = generate_alerts(df_all)
        
        latest = df_all.iloc[-1]
        score = float(latest['final_score'])
        alert_flag = bool(latest['alert'])
        priority = str(latest['priority'])
        
        if alert_flag:
            st.sidebar.error(f"⚠️ ANOMALY FLAGGED!\nScore: {score:.3f} | Priority: {priority}")
            db = SessionLocal()
            db.add(Alert(user_id=test_user, amount=test_amount, score=score, priority=priority))
            db.commit()
            db.close()
            st.sidebar.success("✅ Alert logged to database.")
        else:
            st.sidebar.success(f"✅ Normal Transaction\nScore: {score:.3f} | Priority: {priority}")
    except Exception as e:
        st.sidebar.error(f"Error evaluating transaction: {e}")

# Load Alerts from DB
try:
    df = pd.read_sql("SELECT * FROM alerts ORDER BY created_at DESC", engine)
except Exception as e:
    st.error(f"Could not connect to database: {e}")
    df = pd.DataFrame(columns=["id", "user_id", "amount", "score", "priority", "created_at"])

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Alerts", len(df))
col2.metric("High Risk Alerts", len(df[df['priority'] == 'HIGH']) if not df.empty else 0)
col3.metric("Medium Risk Alerts", len(df[df['priority'] == 'MEDIUM']) if not df.empty else 0)
avg_score = f"{df['score'].mean():.3f}" if not df.empty and 'score' in df.columns else "0.000"
col4.metric("Avg Anomaly Score", avg_score)

st.divider()

if not df.empty:
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.subheader("📊 Alerts by Priority Tier")
        priority_counts = df['priority'].value_counts()
        st.bar_chart(priority_counts)
    
    with chart_col2:
        st.subheader("💰 Transaction Amounts Flagged")
        st.line_chart(df.set_index('created_at')['amount'])

    st.subheader("📋 Recent Alert Logs")
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "amount": st.column_config.NumberColumn("Amount ($)", format="$%.2f"),
            "score": st.column_config.NumberColumn("Anomaly Score", format="%.3f"),
            "created_at": st.column_config.DatetimeColumn("Timestamp", format="YYYY-MM-DD HH:mm:ss"),
        }
    )
else:
    st.info("No alerts recorded yet. Use the sidebar simulator or call the `/detect` API endpoint to generate alerts.")

st.sidebar.divider()
st.sidebar.markdown("🔗 **FastAPI Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)")
st.sidebar.markdown("📈 **Streamlit App**: [http://localhost:8501](http://localhost:8501)")

