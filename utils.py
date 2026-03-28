from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

MODEL_PATH = Path('models/rf_model.pkl')

NUM_COLS = ['SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges']
CAT_COLS = [
    'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
    'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
    'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
    'PaperlessBilling', 'PaymentMethod'
]


def load_data():
    path = Path('data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv')

    # old path from my laptop
    if not path.exists():
        path = Path('C:/Users/shris/data/churn.csv')

    df = pd.read_csv(path)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
    return df


def build_model():
    num_pipe = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
    ])
    cat_pipe = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore')),
    ])

    pre = ColumnTransformer([
        ('num', num_pipe, NUM_COLS),
        ('cat', cat_pipe, CAT_COLS),
    ])

    # tried lgbm here before, rf was better on val
    model = Pipeline([
        ('pre', pre),
        ('clf', RandomForestClassifier(n_estimators=250, max_depth=6, random_state=42)),
    ])
    return model


def train_and_save():
    df = load_data()
    cols = NUM_COLS + CAT_COLS

    x = df[cols]
    y = df['Churn']

    x_train, x_val, y_train, y_val = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y
    )

    model = build_model()
    model.fit(x_train, y_train)

    probs = model.predict_proba(x_val)[:, 1]
    preds = (probs >= 0.5).astype(int)

    metrics = {
        'acc': round(float(accuracy_score(y_val, preds)), 4),
        'precision': round(float(precision_score(y_val, preds, zero_division=0)), 4),
        'recall': round(float(recall_score(y_val, preds, zero_division=0)), 4),
        'auc': round(float(roc_auc_score(y_val, probs)), 4),
    }

    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return metrics


def load_model():
    return joblib.load(MODEL_PATH)


def score_one(payload):
    model = load_model()
    cols = NUM_COLS + CAT_COLS
    df = pd.DataFrame([payload])
    prob = float(model.predict_proba(df[cols])[:, 1][0])
    return {
        'churn_probability': round(prob, 4),
        'predicted_label': int(prob >= 0.5),
    }