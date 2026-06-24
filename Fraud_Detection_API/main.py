from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
import joblib
import numpy as np
import pandas as pd

app = FastAPI(
    title="💳 Fraud Detection API",
    description="""
## Two ways to test:

### 1️⃣ /predict/simple — For normal users
Just fill in basic details — amount, time, location etc.
⚠️ Note: This gives an approximate result based on rules.

### 2️⃣ /predict/technical — For accurate results
Provide V1-V28 values — 100% accurate ML model result.
""",
    version="2.0.0"
)

model = joblib.load("fraud_model_tuned.pkl")
amount_scaler = joblib.load("amount_scaler.pkl")
time_scaler = joblib.load("time_scaler.pkl")
feature_names = joblib.load("feature_names.pkl")


# ── Schema 1: Simple (normal user) ──
class SimpleTransaction(BaseModel):
    amount: float = Field(..., example=1500.00,
        description="Transaction amount in rupees")
    transaction_hour: int = Field(..., example=14,
        description="Hour of transaction (0=midnight, 6=morning, 12=noon, 18=evening, 23=night)")
    merchant_category: Literal["grocery","restaurant","online","atm","travel","other"] = Field(
        ..., example="online",
        description="Where did the transaction happen?")
    transaction_type: Literal["purchase","withdrawal","transfer"] = Field(
        ..., example="purchase",
        description="Type of transaction")
    location_match: bool = Field(..., example=True,
        description="Did the transaction happen at your registered location? (true/false)")
    is_foreign_transaction: bool = Field(..., example=False,
        description="Was this transaction from a foreign country? (true/false)")
    previous_fraud_count: int = Field(..., example=0,
        description="How many times has fraud occurred on this card before? (0 means never)")


# ── Schema 2: Technical (accurate) ──
class TechnicalTransaction(BaseModel):
    Time: float = Field(..., example=0.0)
    V1: float = Field(..., example=-1.35)
    V2: float = Field(..., example=-0.07)
    V3: float = Field(..., example=2.53)
    V4: float = Field(..., example=1.37)
    V5: float = Field(..., example=-0.33)
    V6: float = Field(..., example=0.46)
    V7: float = Field(..., example=0.23)
    V8: float = Field(..., example=0.09)
    V9: float = Field(..., example=0.36)
    V10: float = Field(..., example=0.09)
    V11: float = Field(..., example=-0.55)
    V12: float = Field(..., example=-0.61)
    V13: float = Field(..., example=-0.99)
    V14: float = Field(..., example=-0.31)
    V15: float = Field(..., example=1.46)
    V16: float = Field(..., example=-0.47)
    V17: float = Field(..., example=0.20)
    V18: float = Field(..., example=0.02)
    V19: float = Field(..., example=0.40)
    V20: float = Field(..., example=0.25)
    V21: float = Field(..., example=-0.01)
    V22: float = Field(..., example=0.27)
    V23: float = Field(..., example=-0.11)
    V24: float = Field(..., example=0.06)
    V25: float = Field(..., example=0.12)
    V26: float = Field(..., example=-0.18)
    V27: float = Field(..., example=0.13)
    V28: float = Field(..., example=-0.02)
    Amount: float = Field(..., example=149.62)


# ── Home ──
@app.get("/", tags=["Home"])
def home():
    return {
        "message": "💳 Fraud Detection API is running!",
        "endpoints": {
            "simple": "/predict/simple — For normal users",
            "technical": "/predict/technical — For accurate ML results"
        }
    }


# ── Endpoint 1: Simple ──
@app.post("/predict/simple", tags=["Normal User"])
def predict_simple(data: SimpleTransaction):

    if data.amount <= 0:
        raise HTTPException(status_code=400,
            detail="❌ Amount must be greater than 0!")
    if data.amount > 50000:
        raise HTTPException(status_code=400,
            detail="❌ Amount cannot exceed 50,000!")

    # Rule based risk score
    risk_score = 0

    if not data.location_match:
        risk_score += 35
    if data.is_foreign_transaction:
        risk_score += 25
    if data.transaction_hour >= 22 or data.transaction_hour <= 5:
        risk_score += 20
    if data.merchant_category == "atm":
        risk_score += 10
    if data.transaction_type == "withdrawal":
        risk_score += 10
    if data.previous_fraud_count >= 1:
        risk_score += data.previous_fraud_count * 15
    if data.amount > 20000:
        risk_score += 15
    if data.amount > 40000:
        risk_score += 10

    # Risk level
    if risk_score >= 60:
        risk_level = "🔴 High Risk"
        fraud_detected = True
        message = "⚠️ FRAUD Detected!"
        advice = "Contact your bank immediately and block your card!"
    elif risk_score >= 35:
        risk_level = "🟡 Medium Risk"
        fraud_detected = False
        message = "⚠️ Suspicious Transaction!"
        advice = "Be careful — if you did not make this transaction, report it to your bank."
    else:
        risk_level = "🟢 Low Risk"
        fraud_detected = False
        message = "✅ Transaction is Safe"
        advice = "This transaction looks completely safe."

    return {
        "result": {
            "fraud_detected": fraud_detected,
            "message": message,
            "risk_level": risk_level,
            "risk_score": f"{min(risk_score, 100)}/100",
            "advice": advice
        },
        "transaction_summary": {
            "amount": f"₹{data.amount}",
            "time": f"{data.transaction_hour}:00",
            "merchant": data.merchant_category,
            "type": data.transaction_type,
            "foreign_transaction": "Yes ⚠️" if data.is_foreign_transaction else "No",
            "location_safe": "Yes" if data.location_match else "No ⚠️",
            "fraud_history": f"Fraud occurred {data.previous_fraud_count} time(s) before"
        },
        "note": "⚠️ This is an approximate result. Use /predict/technical for accurate ML model results."
    }


# ── Endpoint 2: Technical (ML Model) ──
@app.post("/predict/technical", tags=["Technical User"])
def predict_technical(data: TechnicalTransaction):

    if data.Amount <= 0:
        raise HTTPException(status_code=400,
            detail="❌ Amount must be greater than 0!")
    if data.Amount > 50000:
        raise HTTPException(status_code=400,
            detail="❌ Amount cannot exceed 50,000!")

    input_dict = data.dict()

    input_dict["Amount"] = amount_scaler.transform(
        [[input_dict["Amount"]]])[0][0]
    input_dict["Time"] = time_scaler.transform(
        [[input_dict["Time"]]])[0][0]

    df = pd.DataFrame([input_dict])
    df = df[feature_names]

    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    if probability >= 0.7:
        risk_level = "🔴 High Risk"
        advice = "Contact your bank immediately and block your card!"
    elif probability >= 0.4:
        risk_level = "🟡 Medium Risk"
        advice = "Be careful — if you did not make this transaction, report it to your bank."
    else:
        risk_level = "🟢 Low Risk"
        advice = "This transaction looks completely safe."

    return {
        "result": {
            "fraud_detected": bool(prediction),
            "message": "⚠️ FRAUD Detected!" if prediction == 1 else "✅ Transaction is Safe",
            "risk_level": risk_level,
            "fraud_probability": f"{round(float(probability) * 100, 2)}%",
            "advice": advice
        },
        "note": "✅ This is an accurate result from the ML model."
    }