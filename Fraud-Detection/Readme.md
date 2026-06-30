# 💳 Credit Card Fraud Detection System

A Machine Learning-powered REST API that detects fraudulent credit card 
transactions in real-time, achieving **85% Recall** and **0.9811 ROC-AUC Score**.

🌐 **Live Demo:** https://fraud-detection-vztr.onrender.com/app

---

## ✨ Features

- ✅ Two prediction endpoints — Simple & Technical
- ✅ Real-time fraud detection
- ✅ Risk level classification (Low / Medium / High)
- ✅ Input validation with proper error messages
- ✅ Interactive API documentation (Swagger UI)
- ✅ Deployed and publicly accessible

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3 | Programming Language |
| FastAPI | API Framework |
| Scikit-learn | ML Model (Random Forest) |
| Joblib | Model serialization |
| Pandas & NumPy | Data processing |
| Uvicorn | ASGI Server |
| Render | Cloud Deployment |
| GitHub | Version Control |

---

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| ROC-AUC | 0.9811 |
| Recall (Fraud) | 85% |
| Precision (Fraud) | 65% |
| Best Model | Random Forest (Tuned) |

---

## 💰 Business Impact

- ✅ **83 out of 98** fraud transactions correctly identified
- 💰 **€10,143** in fraudulent transactions prevented
- ❌ Only **€1,833** in fraud missed (15 transactions)
- 📈 **83.7% effectiveness** on test data

---

## 📁 Project Structure
```
fraud-detection/
├── Fraud_Detection_API/
│   ├── main.py
│   ├── Schemas.py
│   ├── requirements.txt
│   ├── render.yaml
│   ├── fraud_model.pkl
│   ├── fraud_model_tuned.pkl
│   ├── amount_scaler.pkl
│   ├── time_scaler.pkl
│   └── feature_names.pkl
│
└── Fraud-Detection/
    ├── models/
    ├── Fraud_Detection.ipynb
    └── README.md
```

## 🚀 API Endpoints

### 1️⃣ `/predict/simple` — For Normal Users

Send basic transaction details and get fraud prediction.

**Request:**
```json
{
  "amount": 45000,
  "transaction_hour": 3,
  "merchant_category": "atm",
  "transaction_type": "withdrawal",
  "location_match": false,
  "is_foreign_transaction": true,
  "previous_fraud_count": 2
}
```

**Response:**
```json
{
  "result": {
    "fraud_detected": true,
    "message": "⚠️ FRAUD Detected!",
    "risk_level": "🔴 High Risk",
    "risk_score": "95/100",
    "advice": "Contact your bank immediately and block your card!"
  },
  "transaction_summary": {
    "amount": "₹45000.0",
    "time": "3:00",
    "merchant": "atm",
    "type": "withdrawal",
    "foreign_transaction": "Yes ⚠️",
    "location_safe": "No ⚠️",
    "fraud_history": "Fraud occurred 2 time(s) before"
  }
}
```

---

### 2️⃣ `/predict/technical` — For ML/Technical Users

Send raw PCA features (V1-V28) for accurate ML model prediction.

**Request:**
```json
{
  "Time": 406,
  "V1": -2.31, "V2": 1.95, "V3": -1.60,
  "V4": 3.99, "V5": -0.52, "V6": -1.42,
  "V7": -2.53, "V8": 1.39, "V9": -2.77,
  "V10": -2.77, "V11": 3.20, "V12": -2.90,
  "V13": -0.59, "V14": -4.28, "V15": 0.39,
  "V16": -1.14, "V17": -2.83, "V18": -0.01,
  "V19": 0.41, "V20": 0.24, "V21": 0.52,
  "V22": 0.24, "V23": 0.08, "V24": 0.08,
  "V25": -0.41, "V26": -0.01, "V27": 0.04,
  "V28": 0.02, "Amount": 1.00
}
```

**Response:**
```json
{
  "result": {
    "fraud_detected": true,
    "message": "⚠️ FRAUD Detected!",
    "risk_level": "🔴 High Risk",
    "fraud_probability": "94.5%",
    "advice": "Contact your bank immediately and block your card!"
  },
  "note": "✅ This is an accurate result from the ML model."
}
```

---

## 📊 Input Parameters Guide — `/predict/simple`

| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
| `amount` | float | 1 - 50,000 | Transaction amount in rupees |
| `transaction_hour` | int | 0 - 23 | Hour of transaction (0=midnight, 12=noon) |
| `merchant_category` | string | grocery, restaurant, online, atm, travel, other | Where transaction happened |
| `transaction_type` | string | purchase, withdrawal, transfer | Type of transaction |
| `location_match` | bool | true / false | Did transaction happen at registered location? |
| `is_foreign_transaction` | bool | true / false | Was it from a foreign country? |
| `previous_fraud_count` | int | 0, 1, 2... | How many times fraud occurred before |

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.8+
- Git

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/jatin-saxena22/fraud-detection.git
cd fraud-detection/Fraud_Detection_API
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the API**
```bash
uvicorn main:app --reload
```

**5. Open in browser**

---

## 🚀 Future Improvements

This project has strong potential for further enhancement. Below are 
planned improvements to make the system more robust and production-ready:

### Model Enhancements
- **Advanced Algorithms**: Explore LightGBM and CatBoost for faster 
  training and improved handling of categorical features
- **Anomaly Detection**: Integrate Isolation Forest as a complementary 
  unsupervised approach to catch novel fraud patterns
- **Deep Learning**: Experiment with Autoencoder-based anomaly detection 
  for identifying complex, non-linear fraud patterns
- **Ensemble Stacking**: Combine Random Forest and XGBoost predictions 
  using a meta-learner for improved accuracy

### Production Readiness
- **Real-time Streaming**: Integrate Apache Kafka for live transaction 
  stream processing instead of batch predictions
- **Model Monitoring**: Implement drift detection to track model 
  performance degradation over time
- **A/B Testing**: Set up systematic threshold optimization through 
  controlled experiments in production

### Scaling
- **Full-scale Tuning**: Run exhaustive hyperparameter optimization on 
  the complete dataset using cloud computing resources (AWS/GCP)
- **CI/CD Pipeline**: Automate testing and deployment using 
  GitHub Actions

---

## 👤 Author

**Jatin Saxena**  
[GitHub](https://github.com/jatin-saxena22) · 
[LinkedIn](https://linkedin.com/in/jatinsaxena262) · 
[Email](mailto:jatinsaxena262@gmail.com)