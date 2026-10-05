"""
Use the SAVED model to predict loan status for a NEW customer/loan.

Run save_model.py first (once) to create the .pkl files.
Then edit the `new_loan` dictionary below with real values and run this file.
"""

import pandas as pd
import joblib

# ------------------------------------------------------------------
# 1. Load the saved model, scaler, and encoder
# ------------------------------------------------------------------
model = joblib.load("loan_model.pkl")
scaler = joblib.load("scaler.pkl")
gender_encoder = joblib.load("gender_encoder.pkl")
feature_cols = joblib.load("feature_cols.pkl")

# ------------------------------------------------------------------
# 2. Enter details for a NEW loan/customer here
#    (replace these example values with a real customer's data)
# ------------------------------------------------------------------
new_loan = {
    "PRINCIPAL": 100000,
    "INTEREST_RATE": 8.6,
    "TERM_MONTHS": 24,
    "EMI_AMOUNT": 6000,
    "GENDER": "Male",          # "Male" or "Female"
    "AGE": 30,
    "TENURE_MONTHS": 100,       # how long they've been a customer
    "BALANCE": 20000,
    "TXN_COUNT": 12,
    "AVG_TXN_AMOUNT": 1000,
}

# ------------------------------------------------------------------
# 3. Derive the same engineered features used in training
# ------------------------------------------------------------------
new_loan["EMI_TO_PRINCIPAL_RATIO"] = new_loan["EMI_AMOUNT"] / new_loan["PRINCIPAL"]
new_loan["EMI_TO_BALANCE_RATIO"] = new_loan["EMI_AMOUNT"] / new_loan["BALANCE"]
new_loan["GENDER_ENC"] = gender_encoder.transform([new_loan["GENDER"]])[0]

# ------------------------------------------------------------------
# 4. Build a single-row dataframe in the EXACT column order used in training
# ------------------------------------------------------------------
input_df = pd.DataFrame([{col: new_loan[col] for col in feature_cols}])

# ------------------------------------------------------------------
# 5. Scale and predict
# ------------------------------------------------------------------
input_scaled = scaler.transform(input_df)

prediction = model.predict(input_scaled)[0]
probability = model.predict_proba(input_scaled)[0][1]  # probability of CLOSED

status = "CLOSED" if prediction == 1 else "ACTIVE"

print("=" * 50)
print("NEW LOAN PREDICTION")
print("=" * 50)
print(f"Predicted Status     : {status}")
print(f"Probability of CLOSED: {probability:.1%}")
print(f"Probability of ACTIVE: {1 - probability:.1%}")
print("=" * 50)

if probability > 0.7:
    print("-> High likelihood of closing soon. Consider proactive follow-up / new offer.")
elif probability < 0.3:
    print("-> Likely to remain active long-term. Low near-term closure risk.")
else:
    print("-> Uncertain / borderline case. Monitor over time.")
