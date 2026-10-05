"""
Bank Loan Status Prediction — Mini Project
============================================
Predicts whether a loan is ACTIVE or CLOSED using customer, account,
transaction, and loan data joined from a 4-table relational database.

Input: loan_features.csv (exported from Oracle SQL Developer using the
       join query in sql_insight_queries.sql, query #1)

Models: Logistic Regression (baseline) and Random Forest (main model)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score, roc_curve, classification_report
)

# ------------------------------------------------------------------
# 1. Load data
# ------------------------------------------------------------------
DATA_PATH = "loan_features.csv"
df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)
print("\nLoan status distribution:")
print(df["LOAN_STATUS"].value_counts())

# ------------------------------------------------------------------
# 2. Prepare target and features
# ------------------------------------------------------------------
# Target: 1 = CLOSED, 0 = ACTIVE
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

# ------------------------------------------------------------------
# 3. Train/test split
# ------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ------------------------------------------------------------------
# 4. Train models
# ------------------------------------------------------------------
log_reg = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42,stratify=y)
log_reg.fit(X_train_scaled, y_train)

rf = RandomForestClassifier(
    n_estimators=300, max_depth=6, class_weight="balanced", random_state=42
)
rf.fit(X_train, y_train)

# ------------------------------------------------------------------
# 5. Evaluate models
# ------------------------------------------------------------------
def evaluate_model(name, y_true, y_pred, y_proba):
    print(f"\n{'='*50}\n{name}\n{'='*50}")
    print("Accuracy :", round(accuracy_score(y_true, y_pred), 3))
    print("Precision:", round(precision_score(y_true, y_pred), 3))
    print("Recall   :", round(recall_score(y_true, y_pred), 3))
    print("F1 Score :", round(f1_score(y_true, y_pred), 3))
    print("ROC-AUC  :", round(roc_auc_score(y_true, y_proba), 3))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_true, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=["ACTIVE", "CLOSED"]))
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred),
        "roc_auc": roc_auc_score(y_true, y_proba),
    }

lr_pred = log_reg.predict(X_test_scaled)
lr_proba = log_reg.predict_proba(X_test_scaled)[:, 1]
lr_metrics = evaluate_model("Logistic Regression", y_test, lr_pred, lr_proba)

rf_pred = rf.predict(X_test)
rf_proba = rf.predict_proba(X_test)[:, 1]
rf_metrics = evaluate_model("Random Forest", y_test, rf_pred, rf_proba)

# ------------------------------------------------------------------
# 6. Feature importance (Random Forest)
# ------------------------------------------------------------------
importances = pd.Series(rf.feature_importances_, index=feature_cols)
importances = importances.sort_values(ascending=False)
print("\nFeature Importances (Random Forest):")
print(importances)

# ------------------------------------------------------------------
# 7. Save predictions for the test set
# ------------------------------------------------------------------
results_df = df.loc[X_test.index, ["LOAN_ID", "CUSTOMER_ID", "LOAN_STATUS"]].copy()
results_df["Predicted_Status"] = np.where(rf_pred == 1, "CLOSED", "ACTIVE")
results_df["Probability_Closed"] = rf_proba.round(3)
results_df.to_csv("loan_predictions_output.csv", index=False)
print("\nSaved predictions to loan_predictions_output.csv")

# ------------------------------------------------------------------
# 8. Visualizations
# ------------------------------------------------------------------
# Confusion Matrix
plt.figure(figsize=(6, 5))
sns.heatmap(
    confusion_matrix(y_test, rf_pred), annot=True, fmt="d", cmap="Blues",
    xticklabels=["ACTIVE", "CLOSED"], yticklabels=["ACTIVE", "CLOSED"]
)
plt.title("Confusion Matrix - Random Forest")
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=120)
plt.close()

# ROC Curve
plt.figure(figsize=(6, 5))
fpr_rf, tpr_rf, _ = roc_curve(y_test, rf_proba)
fpr_lr, tpr_lr, _ = roc_curve(y_test, lr_proba)
plt.plot(fpr_rf, tpr_rf, label=f"Random Forest (AUC={rf_metrics['roc_auc']:.2f})")
plt.plot(fpr_lr, tpr_lr, label=f"Logistic Regression (AUC={lr_metrics['roc_auc']:.2f})")
plt.plot([0, 1], [0, 1], "k--", alpha=0.4, label="Random guess")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve Comparison")
plt.legend()
plt.tight_layout()
plt.savefig("roc_curve.png", dpi=120)
plt.close()

# Feature Importance
plt.figure(figsize=(7, 5))
importances.plot(kind="barh", color="teal")
plt.gca().invert_yaxis()
plt.title("Feature Importance (Random Forest)")
plt.xlabel("Importance")
plt.tight_layout()
plt.savefig("feature_importance.png", dpi=120)
plt.close()

print("\nAll charts saved: confusion_matrix.png, roc_curve.png, feature_importance.png")
print("\nDone.")
