# Customer Churn Prediction - End to End ML Pipeline

This project is for showing a proper ML pipeline and not only a notebook. I wanted one project that starts with customer churn data, trains a model, saves artifacts, and exposes a prediction API.

## what is in this project

- data loading
- preprocessing
- churn model training
- saved model artifact
- CLI prediction
- FastAPI serving
- dashboard UI

## dataset idea

The main dataset now is the IBM Telco Customer Churn dataset in `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv`.

main columns:

- `tenure`
- `MonthlyCharges`
- `TotalCharges`
- `Contract`
- `InternetService`
- `PaymentMethod`
- `TechSupport`
- `OnlineSecurity`
- `PaperlessBilling`
- `Churn`

## run

```bash
python train.py
python predict.py --input examples/sample_request.json
uvicorn app:app --reload
```

## outputs

- `artifacts/model.joblib`
- `artifacts/train_metrics.json`
- `artifacts/model_metadata.json`

This is meant to be the main classification + deployment project in the portfolio.

## structure

- `src/churn_pipeline/` core Python code for training, inference, and API routes
- `dashboard_ui/` simple dashboard page with HTML, CSS, and JavaScript
- `config/` feature config and column setup
- `data/sample/` tiny backup sample file for development
- `examples/` example request payload for `/predict`
