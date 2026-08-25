from pydantic import BaseModel
from datetime import datetime

class Transaction(BaseModel):
    user_id: int
    amount: float
    timestamp: datetime

class AnomalyResponse(BaseModel):
    anomaly_score: float
    alert: bool
    priority: str
