from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_app_db
from app.schemas.model import PredictRequest
from app.services.model_service import (
    get_evaluation,
    get_model_info,
    predict_customer,
    predict_manual,
    train_model,
)


router = APIRouter()


@router.post(
    "/train",
    summary="Training model Naive Bayes",
    description="Melatih model Categorical Naive Bayes menggunakan dataset lokal backend skripsi.",
)
def train(db: Session = Depends(get_app_db)) -> dict:
    try:
        evaluation = train_model(db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "message": "Model Naive Bayes berhasil dilatih.",
        "data": evaluation,
    }


@router.get(
    "/evaluate",
    summary="Lihat evaluasi model",
    description="Menampilkan hasil evaluasi model terakhir dalam format JSON.",
)
def evaluate() -> dict:
    try:
        evaluation = get_evaluation()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {
        "message": "Evaluasi model berhasil diambil.",
        "data": evaluation,
    }


@router.post(
    "/predict",
    summary="Prediksi risiko piutang",
    description="Melakukan prediksi risiko piutang berdasarkan customer_code atau input fitur manual.",
)
def predict(payload: PredictRequest, db: Session = Depends(get_app_db)) -> dict:
    try:
        if payload.customer_code:
            result = predict_customer(db, payload.customer_code)
        else:
            result = predict_manual(db, payload.model_dump())
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {
        "message": result.pop("pesan", "Prediksi risiko piutang berhasil diproses."),
        "data": result,
    }


@router.get(
    "/info",
    summary="Informasi model",
    description="Menampilkan informasi model, evaluasi, dan database yang digunakan backend skripsi.",
)
def info(db: Session = Depends(get_app_db)) -> dict:
    return {
        "message": "Informasi model berhasil diambil.",
        "data": get_model_info(db),
    }
