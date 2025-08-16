import pandas as pd
import joblib
from typing import Dict

CATEGORICALS = [
    'Education', 'EmploymentType', 'MaritalStatus',
    'HasMortgage', 'HasDependents', 'LoanPurpose', 'HasCoSigner'
]

# Load artifacts only ONCE at module import
model = joblib.load('app/artifacts/loan_default_model_rfs.joblib')
feature_order = joblib.load('app/artifacts/model_feature_order.pkl')
ref_row = pd.read_excel('app/artifacts/6S_AI_TASK-Loan_default_Loan_default.xlsx').iloc[0]

def preprocess_input(data: Dict) -> pd.DataFrame:
    sample_df = pd.DataFrame([data])
    full_df = pd.concat([sample_df, ref_row.to_frame().T], ignore_index=True)
    full_encoded = pd.get_dummies(full_df, columns=CATEGORICALS, drop_first=True)
    if 'LoanID' in full_encoded.columns:
        full_encoded = full_encoded.drop(columns=['LoanID'])
    full_encoded = full_encoded.reindex(columns=feature_order, fill_value=0)
    return full_encoded.iloc[[0]]

def predict_risk_score(data: Dict):
    X_sample = preprocess_input(data)
    risk_score = model.predict_proba(X_sample)[:, 1]
    predicted = int(risk_score > 0.5)
    return float(risk_score), bool(predicted)

def get_feature_importance():
    importances = model.feature_importances_
    return sorted([
        {"feature": feature, "importance": float(imp)}
        for feature, imp in zip(feature_order, importances)
    ], key=lambda x: -x["importance"])
