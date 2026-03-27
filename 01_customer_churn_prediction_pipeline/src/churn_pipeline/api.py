from __future__ import annotations

import csv
from io import StringIO
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .config import load_model_config
from .inference import score_payload


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "artifacts" / "model.joblib"
CONFIG = load_model_config(PROJECT_ROOT)
UI_DIR = PROJECT_ROOT / "dashboard_ui"

AT_RISK_ROWS = [
    {
        "customer": "Sunita Reddy",
        "segment": "Enterprise",
        "risk_score": 88,
        "churn_probability": 88,
        "mrr": 4200,
        "status": "High",
    },
    {
        "customer": "James Mitchell",
        "segment": "Growth",
        "risk_score": 74,
        "churn_probability": 74,
        "mrr": 1800,
        "status": "High",
    },
    {
        "customer": "Priya Lakhani",
        "segment": "Enterprise",
        "risk_score": 71,
        "churn_probability": 71,
        "mrr": 6100,
        "status": "High",
    },
    {
        "customer": "Tom Kwan",
        "segment": "Starter",
        "risk_score": 53,
        "churn_probability": 53,
        "mrr": 320,
        "status": "Medium",
    },
    {
        "customer": "Anika Muller",
        "segment": "Growth",
        "risk_score": 41,
        "churn_probability": 41,
        "mrr": 980,
        "status": "Medium",
    },
    {
        "customer": "Ravi Nair",
        "segment": "Enterprise",
        "risk_score": 22,
        "churn_probability": 22,
        "mrr": 8400,
        "status": "Low",
    },
]


class PredictionRequest(BaseModel):
    customerID: str
    gender: str
    SeniorCitizen: float
    Partner: str
    Dependents: str
    tenure: float
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


def create_app() -> FastAPI:
    app = FastAPI(title="Customer Churn Prediction API", version="1.0.0")
    app.mount("/static", StaticFiles(directory=UI_DIR / "static"), name="static")

    @app.get("/")
    def dashboard() -> FileResponse:
        return FileResponse(UI_DIR / "index.html")

    @app.get("/health")
    def health() -> dict[str, object]:
        return {"status": "ok", "model_available": MODEL_PATH.exists()}

    @app.get("/dashboard-data")
    def dashboard_data() -> dict[str, object]:
        return {
            "kpis": {
                "churn_rate": "4.2%",
                "customers_at_risk": 312,
                "revenue_at_risk": "$94.3K",
                "retention_actions_sent": 148,
            },
            "at_risk_customers": AT_RISK_ROWS,
        }

    @app.get("/export")
    def export_dashboard_table() -> StreamingResponse:
        buffer = StringIO()
        writer = csv.DictWriter(
            buffer,
            fieldnames=["customer", "segment", "risk_score", "churn_probability", "mrr", "status"],
        )
        writer.writeheader()
        writer.writerows(AT_RISK_ROWS)
        buffer.seek(0)
        return StreamingResponse(
            iter([buffer.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=at_risk_customers.csv"},
        )

    @app.post("/predict")
    def predict(request: PredictionRequest) -> dict[str, object]:
        if not MODEL_PATH.exists():
            raise HTTPException(status_code=500, detail="Run train.py first")
        return score_payload(request.model_dump(), MODEL_PATH, CONFIG)

    return app
