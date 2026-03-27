const exportButton = document.getElementById("exportButton");
const runPredictionButton = document.getElementById("runPredictionButton");
const predictionModal = document.getElementById("predictionModal");
const closeModalButton = document.getElementById("closeModalButton");
const cancelModalButton = document.getElementById("cancelModalButton");
const predictionForm = document.getElementById("predictionForm");
const predictionResult = document.getElementById("predictionResult");
const atRiskTableBody = document.getElementById("atRiskTableBody");

function openModal() {
  predictionModal.classList.remove("hidden");
}

function closeModal() {
  predictionModal.classList.add("hidden");
}

function toPayload(formData) {
  return {
    customerID: formData.get("customerID"),
    gender: formData.get("gender"),
    SeniorCitizen: Number(formData.get("SeniorCitizen")),
    Partner: formData.get("Partner"),
    Dependents: formData.get("Dependents"),
    tenure: Number(formData.get("tenure")),
    PhoneService: formData.get("PhoneService"),
    MultipleLines: formData.get("MultipleLines"),
    InternetService: formData.get("InternetService"),
    OnlineSecurity: formData.get("OnlineSecurity"),
    OnlineBackup: formData.get("OnlineBackup"),
    DeviceProtection: formData.get("DeviceProtection"),
    TechSupport: formData.get("TechSupport"),
    StreamingTV: formData.get("StreamingTV"),
    StreamingMovies: formData.get("StreamingMovies"),
    Contract: formData.get("Contract"),
    PaperlessBilling: formData.get("PaperlessBilling"),
    PaymentMethod: formData.get("PaymentMethod"),
    MonthlyCharges: Number(formData.get("MonthlyCharges")),
    TotalCharges: Number(formData.get("TotalCharges")),
  };
}

async function loadDashboardData() {
  const response = await fetch("/dashboard-data");
  if (!response.ok) return;
  const payload = await response.json();
  if (!payload.at_risk_customers) return;

  atRiskTableBody.innerHTML = payload.at_risk_customers
    .map(
      (row, index) => `
        <tr>
          <td><span class="avatar ${["rose", "blue", "lavender", "green", "amber", "sky"][index % 6]}">${row.customer
            .split(" ")
            .map((part) => part[0])
            .join("")
            .slice(0, 2)}</span> ${row.customer}</td>
          <td>${row.segment}</td>
          <td><span class="meter"><span style="width: ${row.risk_score}%"></span></span></td>
          <td>${row.churn_probability}%</td>
          <td>$${row.mrr.toLocaleString()}</td>
          <td><span class="status ${row.status.toLowerCase()}">${row.status}</span></td>
        </tr>
      `
    )
    .join("");
}

exportButton.addEventListener("click", () => {
  window.location.href = "/export";
});

runPredictionButton.addEventListener("click", openModal);
closeModalButton.addEventListener("click", closeModal);
cancelModalButton.addEventListener("click", closeModal);

predictionForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  predictionResult.classList.remove("hidden");
  predictionResult.textContent = "Running prediction...";

  const payload = toPayload(new FormData(predictionForm));
  const response = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorText = await response.text();
    predictionResult.innerHTML = `<strong>Prediction failed.</strong><pre>${errorText}</pre>`;
    return;
  }

  const result = await response.json();
  predictionResult.innerHTML = `
    <strong>Prediction result</strong>
    <div class="result-grid">
      <div><span>customerID</span><strong>${result.customerID}</strong></div>
      <div><span>Churn probability</span><strong>${(result.churn_probability * 100).toFixed(2)}%</strong></div>
      <div><span>Predicted label</span><strong>${result.predicted_label}</strong></div>
    </div>
  `;
});

predictionModal.addEventListener("click", (event) => {
  if (event.target === predictionModal) {
    closeModal();
  }
});

loadDashboardData();
