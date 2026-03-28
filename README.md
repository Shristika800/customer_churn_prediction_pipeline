# churn thing

still cleaning this up.

run maybe:
```bash
python train.py
python predict.py
uvicorn app:app --reload
```

using IBM telco churn data rn.

files i actually look at most:
- train.py
- predict.py
- app.py
- utils.py

if raw file is there in data/raw it should pick it up.