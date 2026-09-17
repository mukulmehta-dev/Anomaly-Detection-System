from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from functools import lru_cache
import pandas as pd

from api.schemas import Transaction, AnomalyResponse
from src.feature_engineering import create_features
from src.statistical_methods import z_score_detection, mahalanobis_distance
from src.ml_models import isolation_forest, lof_detection
from src.time_series import arima_residuals
from src.ensemble import ensemble_score
from src.alerting import generate_alerts
from src.database import SessionLocal, Alert

app = FastAPI(title="Anomaly Detection API")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc):
    return JSONResponse(status_code=429, content={"msg": "Too many requests"})

@lru_cache(maxsize=1)
def load_data():
    df = pd.read_csv("data/processed_transactions.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

@app.post("/detect", response_model=AnomalyResponse)
@limiter.limit("5/minute")
def detect(request: Request, tx: Transaction):


    df = load_data().copy()
    df = pd.concat([df, pd.DataFrame([tx.dict()])], ignore_index=True)

    df = create_features(df)
    FEATURES = ['amount_log', 'hour', 'day']

    df['z_score'] = z_score_detection(df, 'amount')
    df['mahalanobis'] = mahalanobis_distance(df, FEATURES)
    df['iso_score'] = isolation_forest(df, FEATURES)
    df['lof_score'] = lof_detection(df, FEATURES)
    df['arima_resid'] = arima_residuals(df['amount'])

    df = ensemble_score(df)
    df = generate_alerts(df)

    latest = df.iloc[-1]

    if latest['alert']:
        db = SessionLocal()
        db.add(Alert(
            user_id=tx.user_id,
            amount=tx.amount,
            score=float(latest['final_score']),
            priority=latest['priority']
        ))
        db.commit()
        db.close()

    return {
        "anomaly_score": round(latest['final_score'], 3),
        "alert": bool(latest['alert']),
        "priority": latest['priority']
    }
