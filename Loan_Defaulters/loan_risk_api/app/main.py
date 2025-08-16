from fastapi import FastAPI, HTTPException
from app.schemas import BorrowerFeatures
from app.model_utils import predict_risk_score, get_feature_importance

app = FastAPI(
    title="Loan Default Risk API",
    description="Predict loan default risk and see model insights",
    version="1.0.0"
)

@app.post("/predict")
def predict_endpoint(data: BorrowerFeatures):
    try:
        risk_score, predicted = predict_risk_score(data.dict())
        return {
            "risk_score": round(risk_score, 4),
            "predicted_default": predicted
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/model-info")
def model_info():
    try:
        feature_imp = get_feature_importance()[:10]
        return {
            "top_features": feature_imp,
            "model_type": "RandomForest"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
