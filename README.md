# Bank Loan Status Prediction

A machine learning project that predicts whether a bank loan is **ACTIVE** or **CLOSED** using customer, account, transaction, and loan-related information.

The project compares two classification models:

- Logistic Regression
- Random Forest Classifier

## Project Overview

Banks maintain large amounts of customer, loan, account, and transaction data. Analyzing this data can help predict the current status of a loan.

This project uses a dataset created by joining information from multiple relational database tables. The machine learning models classify each loan into one of two categories:

- `ACTIVE`
- `CLOSED`

The Random Forest model is used as the primary model, while Logistic Regression is used as a baseline model.

## Features Used

The model uses the following input features:

| Feature | Description |
|---|---|
| `PRINCIPAL` | Original loan principal amount |
| `INTEREST_RATE` | Interest rate applied to the loan |
| `TERM_MONTHS` | Loan duration in months |
| `EMI_AMOUNT` | Monthly installment amount |
| `EMI_TO_PRINCIPAL_RATIO` | Ratio of EMI amount to principal |
| `EMI_TO_BALANCE_RATIO` | Ratio of EMI amount to outstanding balance |
| `GENDER_ENC` | Encoded customer gender |
| `AGE` | Customer age |
| `TENURE_MONTHS` | Customer account tenure |
| `BALANCE` | Current account balance |
| `TXN_COUNT` | Number of transactions |
| `AVG_TXN_AMOUNT` | Average transaction amount |

## Machine Learning Workflow

The project follows these steps:

1. Load the loan dataset from a CSV file.
2. Analyze the distribution of loan statuses.
3. Convert the target variable into numerical values:
   - `CLOSED = 1`
   - `ACTIVE = 0`
4. Encode the gender column using `LabelEncoder`.
5. Select the required features.
6. Split the dataset into training and testing data.
7. Apply feature scaling for Logistic Regression.
8. Train Logistic Regression and Random Forest models.
9. Evaluate both models using classification metrics.
10. Generate Random Forest feature importance.
11. Save test-set predictions to a CSV file.
12. Generate evaluation visualizations.

## Models Used

### Logistic Regression

Logistic Regression is used as the baseline classification model. It is trained using standardized features and balanced class weights.

### Random Forest

Random Forest is the main model used in this project. It consists of multiple decision trees and is suitable for handling nonlinear relationships between loan, customer, and transaction features.

Configuration used:

```python
RandomForestClassifier(
    n_estimators=300,
    max_depth=6,
    class_weight="balanced",
    random_state=42
)
```

## Evaluation Metrics

The models are evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC score
- Confusion matrix
- Classification report

These metrics help measure the model's ability to correctly classify active and closed loans.

## Project Structure

```text
loan-status-prediction/
│
├── loan_status_prediction.py
├── loan_features.csv
├── loan_predictions_output.csv
├── confusion_matrix.png
├── roc_curve.png
├── feature_importance.png
└── README.md
```

The generated files are created after running the Python script.

## Dataset Requirements

The input file must be named:

```text
loan_features.csv
```

The CSV file should contain the following columns:

```text
LOAN_ID
CUSTOMER_ID
LOAN_STATUS
GENDER
PRINCIPAL
INTEREST_RATE
TERM_MONTHS
EMI_AMOUNT
EMI_TO_PRINCIPAL_RATIO
EMI_TO_BALANCE_RATIO
AGE
TENURE_MONTHS
BALANCE
TXN_COUNT
AVG_TXN_AMOUNT
```

The `LOAN_STATUS` column should contain loan status values such as:

```text
ACTIVE
CLOSED
```

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/loan-status-prediction.git
cd loan-status-prediction
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install the required libraries:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

## How to Run

Place `loan_features.csv` in the same directory as the Python file.

Run the project using:

```bash
python loan_status_prediction.py
```

The script will:

- Train both machine learning models.
- Display evaluation metrics in the terminal.
- Display feature importance values.
- Generate loan predictions.
- Save charts and prediction results.

## Output Files

### Loan Predictions

The file `loan_predictions_output.csv` contains:

```text
LOAN_ID
CUSTOMER_ID
LOAN_STATUS
Predicted_Status
Probability_Closed
```

Example:

```text
LOAN_ID,CUSTOMER_ID,LOAN_STATUS,Predicted_Status,Probability_Closed
1001,501,CLOSED,CLOSED,0.873
1002,502,ACTIVE,ACTIVE,0.214
```

### Confusion Matrix

The file `confusion_matrix.png` displays the number of correct and incorrect predictions made by the Random Forest model.

### ROC Curve

The file `roc_curve.png` compares the ROC performance of Logistic Regression and Random Forest.

### Feature Importance

The file `feature_importance.png` displays the features that contributed most to the Random Forest predictions.

## Database Integration

The dataset can be exported from an Oracle database using a SQL join query that combines information from multiple tables, such as:

- Customer table
- Account table
- Transaction table
- Loan table

The exported result should be saved as:

```text
loan_features.csv
```

The Python machine learning script then uses this file for training and prediction.

## Important Implementation Notes

The target variable is created using the following logic:

```python
df["target"] = (df["LOAN_STATUS"] == "CLOSED").astype(int)
```

This means:

- A closed loan is represented by `1`.
- An active loan is represented by `0`.

The dataset is split using stratification so that both training and testing datasets maintain a similar distribution of loan statuses.

```python
train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
```

## Potential Applications

This project can be extended for:

- Loan portfolio analysis.
- Customer loan-status monitoring.
- Banking risk-analysis systems.
- Loan repayment behavior analysis.
- Customer segmentation.
- Early identification of unusual loan patterns.
- Financial decision-support systems.

## Future Enhancements

Possible improvements include:

- Adding cross-validation.
- Comparing additional models such as XGBoost, SVM, and Gradient Boosting.
- Performing hyperparameter tuning.
- Handling missing values automatically.
- Applying one-hot encoding instead of label encoding for categorical data.
- Creating a web interface using Flask or Streamlit.
- Deploying the model as a REST API.
- Adding model explainability using SHAP.
- Including more financial and repayment-related features.
- Tracking model performance on new data.

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Oracle SQL
- Machine Learning
- Classification Algorithms

## Author

**Suman**

MCA Student  
Presidency College, Bengaluru, India

## License

This project is intended for academic and educational purposes. You may modify and use it for learning, experimentation, and further development.
