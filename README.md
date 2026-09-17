# Anomaly Detection System

Production-ready anomaly detection system using statistical, machine learning, and ensemble techniques.

**Author:** Mukul Mehta ([@mukulmehta-dev](https://github.com/mukulmehta-dev))

## Key Features
- **Statistical & ML Detection**: Z-Score, Mahalanobis Distance, Isolation Forest, Local Outlier Factor (LOF), and ARIMA Residuals
- **Ensemble Scoring**: Weighted ensemble ranking with normalization and dynamic thresholding
- **Real-Time FastAPI Service**: RESTful API with Pydantic validation and SlowAPI rate limiting
- **Resilient Alert Storage**: PostgreSQL support with seamless local SQLite fallback
- **Interactive Monitoring Dashboard**: Live Streamlit UI with metric KPIs, risk priority charts, alert logs, and real-time transaction simulator

## Quickstart

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run API
```bash
uvicorn api.app:app --reload
```
Interactive API docs will be available at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Run Dashboard
```bash
streamlit run dashboard/app.py
```
Live monitoring dashboard will be available at: [http://localhost:8501](http://localhost:8501)

## API Usage Example

```bash
curl -X POST http://localhost:8000/detect \
  -H "Content-Type: application/json" \
  -d '{"user_id": 105, "amount": 85000.0, "timestamp": "2026-01-11T03:30:00"}'
```

Response:
```json
{
  "anomaly_score": 0.717,
  "alert": true,
  "priority": "MEDIUM"
}
```

