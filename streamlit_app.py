import streamlit as st
import requests

API = 'http://127.0.0.1:8000'

st.title('churn predictor')
st.caption('telco customer churn — rf model')

st.subheader('customer info')

col1, col2 = st.columns(2)

with col1:
    customerID = st.text_input('customerID', value='9999-DEMOX')
    gender = st.selectbox('gender', ['Male', 'Female'])
    senior = st.selectbox('senior citizen', [0, 1])
    partner = st.selectbox('partner', ['Yes', 'No'])
    dependents = st.selectbox('dependents', ['Yes', 'No'])
    tenure = st.number_input('tenure (months)', min_value=0, max_value=72, value=12)
    monthly = st.number_input('monthly charges', min_value=0.0, max_value=200.0, value=85.5)
    total = st.number_input('total charges', min_value=0.0, max_value=10000.0, value=1026.0)
    contract = st.selectbox('contract', ['Month-to-month', 'One year', 'Two year'])

with col2:
    phone = st.selectbox('phone service', ['Yes', 'No'])
    multiline = st.selectbox('multiple lines', ['Yes', 'No', 'No phone service'])
    internet = st.selectbox('internet service', ['Fiber optic', 'DSL', 'No'])
    security = st.selectbox('online security', ['Yes', 'No', 'No internet service'])
    backup = st.selectbox('online backup', ['Yes', 'No', 'No internet service'])
    device = st.selectbox('device protection', ['Yes', 'No', 'No internet service'])
    tech = st.selectbox('tech support', ['Yes', 'No', 'No internet service'])
    tv = st.selectbox('streaming tv', ['Yes', 'No', 'No internet service'])
    movies = st.selectbox('streaming movies', ['Yes', 'No', 'No internet service'])
    paperless = st.selectbox('paperless billing', ['Yes', 'No'])
    payment = st.selectbox('payment method', [
        'Electronic check', 'Mailed check',
        'Bank transfer (automatic)', 'Credit card (automatic)'
    ])

st.divider()

if st.button('predict'):
    payload = {
        'customerID': customerID,
        'gender': gender,
        'SeniorCitizen': senior,
        'Partner': partner,
        'Dependents': dependents,
        'tenure': tenure,
        'PhoneService': phone,
        'MultipleLines': multiline,
        'InternetService': internet,
        'OnlineSecurity': security,
        'OnlineBackup': backup,
        'DeviceProtection': device,
        'TechSupport': tech,
        'StreamingTV': tv,
        'StreamingMovies': movies,
        'Contract': contract,
        'PaperlessBilling': paperless,
        'PaymentMethod': payment,
        'MonthlyCharges': monthly,
        'TotalCharges': total,
    }

    try:
        res = requests.post(f'{API}/predict', json=payload)
        result = res.json()

        prob = result['churn_probability']
        label = result['predicted_label']

        st.subheader('result')
        st.progress(prob, text=f'churn probability: {round(prob * 100, 1)}%')

        if label == 1:
            st.error('likely to churn')
        else:
            st.success('likely to stay')

    except Exception as e:
        st.error(f'api error — is uvicorn running? ({e})')