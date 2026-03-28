from fastapi import FastAPI
from pydantic import BaseModel

from utils import score_one, MODEL_PATH

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils import score_one, MODEL_PATH

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CustomerIn(BaseModel):
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


@app.get('/')
def home():
    return {'model_ready': MODEL_PATH.exists()}


@app.post('/predict')
def predict(body: CustomerIn):
    # will crash if model not there, run train.py first
    return score_one(body.model_dump())