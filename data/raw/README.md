# Raw Data Instructions

Place the Kaggle Home Credit files here before training the full version of the pipeline.

Required for the baseline:

- `application_train.csv`

Optional but recommended later:

- `application_test.csv`
- `bureau.csv`
- `previous_application.csv`
- `installments_payments.csv`

The training code falls back to the sample CSV in `data/sample/` if `application_train.csv` is not present.
