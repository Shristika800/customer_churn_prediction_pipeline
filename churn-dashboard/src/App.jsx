import { useState } from 'react'
import './App.css'

const API = 'http://127.0.0.1:8000'

const DEFAULTS = {
  customerID: '9999-DEMOX',
  gender: 'Female',
  SeniorCitizen: 0,
  Partner: 'Yes',
  Dependents: 'No',
  tenure: 12,
  PhoneService: 'Yes',
  MultipleLines: 'No',
  InternetService: 'Fiber optic',
  OnlineSecurity: 'No',
  OnlineBackup: 'Yes',
  DeviceProtection: 'No',
  TechSupport: 'No',
  StreamingTV: 'Yes',
  StreamingMovies: 'Yes',
  Contract: 'Month-to-month',
  PaperlessBilling: 'Yes',
  PaymentMethod: 'Electronic check',
  MonthlyCharges: 85.5,
  TotalCharges: 1026.0,
}

const Select = ({ label, name, options, value, onChange }) => (
  <div className="field">
    <label>{label}</label>
    <select name={name} value={value} onChange={onChange}>
      {options.map(o => <option key={o}>{o}</option>)}
    </select>
  </div>
)

const NumberInput = ({ label, name, value, onChange, min, max, step }) => (
  <div className="field">
    <label>{label}</label>
    <input
      type="number"
      name={name}
      value={value}
      onChange={onChange}
      min={min}
      max={max}
      step={step || 1}
    />
  </div>
)

const TextInput = ({ label, name, value, onChange }) => (
  <div className="field">
    <label>{label}</label>
    <input type="text" name={name} value={value} onChange={onChange} />
  </div>
)

export default function App() {
  const [form, setForm] = useState(DEFAULTS)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handle = e => {
    const { name, value } = e.target
    const numFields = ['SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges']
    setForm(f => ({ ...f, [name]: numFields.includes(name) ? Number(value) : value }))
  }

  const predict = async () => {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await fetch(`${API}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      if (!res.ok) throw new Error(`api returned ${res.status}`)
      setResult(await res.json())
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const pct = result ? Math.round(result.churn_probability * 100) : 0
  const willChurn = result?.predicted_label === 1

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-tag">ML</span>
          <div>
            <div className="brand-title">churn predictor</div>
            <div className="brand-sub">telco · random forest</div>
          </div>
        </div>

        <nav className="nav">
          <div className="nav-item active">predict</div>
          <div className="nav-item muted">history</div>
          <div className="nav-item muted">model info</div>
        </nav>

        <div className="sidebar-footer">
          <div className="status-dot" />
          <span>api connected</span>
        </div>
      </aside>

      <main className="main">
        <div className="page-header">
          <h1>customer prediction</h1>
          <p>fill in customer details and run the model</p>
        </div>

        <div className="grid">
          <section className="card">
            <div className="card-title">account</div>
            <TextInput label="customer id" name="customerID" value={form.customerID} onChange={handle} />
            <Select label="contract" name="Contract" value={form.Contract} onChange={handle}
              options={['Month-to-month', 'One year', 'Two year']} />
            <Select label="payment method" name="PaymentMethod" value={form.PaymentMethod} onChange={handle}
              options={['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)']} />
            <Select label="paperless billing" name="PaperlessBilling" value={form.PaperlessBilling} onChange={handle}
              options={['Yes', 'No']} />
            <NumberInput label="tenure (months)" name="tenure" value={form.tenure} onChange={handle} min={0} max={72} />
            <NumberInput label="monthly charges" name="MonthlyCharges" value={form.MonthlyCharges} onChange={handle} min={0} max={200} step={0.1} />
            <NumberInput label="total charges" name="TotalCharges" value={form.TotalCharges} onChange={handle} min={0} max={10000} step={0.1} />
          </section>

          <section className="card">
            <div className="card-title">demographics</div>
            <Select label="gender" name="gender" value={form.gender} onChange={handle} options={['Male', 'Female']} />
            <Select label="senior citizen" name="SeniorCitizen" value={form.SeniorCitizen} onChange={handle} options={[0, 1]} />
            <Select label="partner" name="Partner" value={form.Partner} onChange={handle} options={['Yes', 'No']} />
            <Select label="dependents" name="Dependents" value={form.Dependents} onChange={handle} options={['Yes', 'No']} />

            <div className="card-title" style={{ marginTop: '1.5rem' }}>services</div>
            <Select label="phone service" name="PhoneService" value={form.PhoneService} onChange={handle} options={['Yes', 'No']} />
            <Select label="multiple lines" name="MultipleLines" value={form.MultipleLines} onChange={handle}
              options={['Yes', 'No', 'No phone service']} />
            <Select label="internet service" name="InternetService" value={form.InternetService} onChange={handle}
              options={['Fiber optic', 'DSL', 'No']} />
          </section>

          <section className="card">
            <div className="card-title">add-ons</div>
            <Select label="online security" name="OnlineSecurity" value={form.OnlineSecurity} onChange={handle}
              options={['Yes', 'No', 'No internet service']} />
            <Select label="online backup" name="OnlineBackup" value={form.OnlineBackup} onChange={handle}
              options={['Yes', 'No', 'No internet service']} />
            <Select label="device protection" name="DeviceProtection" value={form.DeviceProtection} onChange={handle}
              options={['Yes', 'No', 'No internet service']} />
            <Select label="tech support" name="TechSupport" value={form.TechSupport} onChange={handle}
              options={['Yes', 'No', 'No internet service']} />
            <Select label="streaming tv" name="StreamingTV" value={form.StreamingTV} onChange={handle}
              options={['Yes', 'No', 'No internet service']} />
            <Select label="streaming movies" name="StreamingMovies" value={form.StreamingMovies} onChange={handle}
              options={['Yes', 'No', 'No internet service']} />
          </section>
        </div>

        <div className="actions">
          <button className="btn-predict" onClick={predict} disabled={loading}>
            {loading ? 'running model...' : 'run prediction'}
          </button>
        </div>

        {error && (
          <div className="result-card error">
            <div className="result-label">error</div>
            <div className="result-msg">{error} — is uvicorn running?</div>
          </div>
        )}

        {result && (
          <div className={`result-card ${willChurn ? 'churn' : 'stay'}`}>
            <div className="result-top">
              <div>
                <div className="result-label">prediction</div>
                <div className="result-verdict">{willChurn ? 'likely to churn' : 'likely to stay'}</div>
              </div>
              <div className="result-pct">{pct}%</div>
            </div>

            <div className="prob-bar-bg">
              <div
                className="prob-bar-fill"
                style={{ width: `${pct}%`, background: willChurn ? '#ef4444' : '#22c55e' }}
              />
            </div>
            <div className="prob-label">churn probability</div>
          </div>
        )}
      </main>
    </div>
  )
}
