"""
Train and SAVE the model to disk, so it can be reused later
without retraining every time.

Run this once. It creates:
  - loan_model.pkl      (the trained Random Forest / Logistic Regression)
  - scaler.pkl           (the fitted StandardScaler)
  - gender_encoder.pkl   (the fitted LabelEncoder for GENDER)
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression

DATA_PATH = "loan_features.csv"

df = pd.read_csv(DATA_PATH)
df["target"] = (df["LOAN_STATUS"] == "CLOSED").astype(int)

le_gender = LabelEncoder()
df["GENDER_ENC"] = le_gender.fit_transform(df["GENDER"])

feature_cols = [
    "PRINCIPAL", "INTEREST_RATE", "TERM_MONTHS", "EMI_AMOUNT",
    "EMI_TO_PRINCIPAL_RATIO", "EMI_TO_BALANCE_RATIO", "GENDER_ENC",
    "AGE", "TENURE_MONTHS", "BALANCE", "TXN_COUNT", "AVG_TXN_AMOUNT"
]

X = df[feature_cols]
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Using Logistic Regression since it performed best on this dataset
model = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
model.fit(X_train_scaled, y_train)

# Save everything needed to make future predictions
joblib.dump(model, "loan_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(le_gender, "gender_encoder.pkl")
joblib.dump(feature_cols, "feature_cols.pkl")

print("Model, scaler, and encoder saved successfully.")
print("Files created: loan_model.pkl, scaler.pkl, gender_encoder.pkl, feature_cols.pkl")
