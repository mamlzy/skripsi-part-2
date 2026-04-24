from __future__ import annotations

import json
from datetime import datetime

import joblib
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import CategoricalNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OrdinalEncoder
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.constants import FEATURE_CATEGORIES, FEATURE_COLUMNS, LABEL_ORDER
from app.ml.preprocessing import ambil_fitur_kategorikal, bentuk_record_manual
from app.models.dataset import DatasetRisikoPiutang, ModelTrainingRun, PredictionLog
from app.services.dataset_service import ambil_dataset_atau_generate, dataset_row_to_dict
from app.services.source_data_service import ambil_dataset_dari_database_sumber


def _ganti_unknown_encoder(data: np.ndarray) -> np.ndarray:
    return np.where(data < 0, 0, data).astype(int)


def _buat_pipeline_model() -> Pipeline:
    categories = [FEATURE_CATEGORIES[column] for column in FEATURE_COLUMNS]
    min_categories = [len(category) for category in categories]
    return Pipeline(
        steps=[
            (
                "ordinal_encoder",
                OrdinalEncoder(
                    categories=categories,
                    handle_unknown="use_encoded_value",
                    unknown_value=-1,
                    dtype=np.int64,
                ),
            ),
            (
                "unknown_ke_tidak_diketahui",
                FunctionTransformer(_ganti_unknown_encoder, validate=False),
            ),
            ("naive_bayes", CategoricalNB(min_categories=min_categories)),
        ]
    )


def _probabilitas(model: Pipeline, feature_values: list[list[str]]) -> dict:
    probabilities = model.predict_proba(feature_values)[0]
    return {
        str(label): float(probabilities[index])
        for index, label in enumerate(model.classes_)
    }


def train_model(db: Session) -> dict:
    settings = get_settings()
    records = ambil_dataset_atau_generate(db)
    if len(records) < 10:
        raise ValueError("Dataset minimal 10 baris untuk proses training.")

    x = ambil_fitur_kategorikal(records)
    y = [record["risiko_piutang"] for record in records]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=settings.test_size,
        random_state=settings.random_state,
        stratify=y,
    )

    model = _buat_pipeline_model()
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    macro = precision_recall_fscore_support(
        y_test,
        y_pred,
        labels=LABEL_ORDER,
        average="macro",
        zero_division=0,
    )
    weighted = precision_recall_fscore_support(
        y_test,
        y_pred,
        labels=LABEL_ORDER,
        average="weighted",
        zero_division=0,
    )
    report = classification_report(
        y_test,
        y_pred,
        labels=LABEL_ORDER,
        output_dict=True,
        zero_division=0,
    )
    matrix = confusion_matrix(y_test, y_pred, labels=LABEL_ORDER).tolist()

    artifact = {
        "model": model,
        "encoding": "OrdinalEncoder",
        "feature_columns": FEATURE_COLUMNS,
        "feature_categories": FEATURE_CATEGORIES,
        "label_order": LABEL_ORDER,
        "trained_at": datetime.utcnow().isoformat(),
        "dataset_count": len(records),
    }
    joblib.dump(artifact, settings.model_path)

    evaluation = {
        "accuracy": float(accuracy),
        "macro_avg": {
            "precision": float(macro[0]),
            "recall": float(macro[1]),
            "f1_score": float(macro[2]),
        },
        "weighted_avg": {
            "precision": float(weighted[0]),
            "recall": float(weighted[1]),
            "f1_score": float(weighted[2]),
        },
        "classification_report": report,
        "confusion_matrix": {
            "labels": LABEL_ORDER,
            "matrix": matrix,
        },
        "jumlah_data": len(records),
        "jumlah_data_latih": len(x_train),
        "jumlah_data_uji": len(x_test),
    }

    settings.evaluation_path.write_text(
        json.dumps(evaluation, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    run = ModelTrainingRun(
        model_path=str(settings.model_path),
        dataset_count=len(records),
        test_size=settings.test_size,
        accuracy=float(accuracy),
        macro_precision=float(macro[0]),
        macro_recall=float(macro[1]),
        macro_f1=float(macro[2]),
        weighted_precision=float(weighted[0]),
        weighted_recall=float(weighted[1]),
        weighted_f1=float(weighted[2]),
        report_json=json.dumps(report, ensure_ascii=False),
        confusion_matrix_json=json.dumps(matrix),
    )
    db.add(run)
    db.commit()

    return evaluation


def load_artifact() -> dict:
    settings = get_settings()
    if not settings.model_path.exists():
        raise FileNotFoundError("Model belum tersedia. Jalankan training terlebih dahulu.")
    return joblib.load(settings.model_path)


def get_evaluation() -> dict:
    settings = get_settings()
    if not settings.evaluation_path.exists():
        raise FileNotFoundError("Evaluasi belum tersedia. Jalankan training terlebih dahulu.")
    return json.loads(settings.evaluation_path.read_text(encoding="utf-8"))


def get_model_info(db: Session) -> dict:
    settings = get_settings()
    latest = db.scalars(select(ModelTrainingRun).order_by(ModelTrainingRun.trained_at.desc())).first()
    return {
        "model_tersedia": settings.model_path.exists(),
        "path_model": str(settings.model_path),
        "evaluasi_tersedia": settings.evaluation_path.exists(),
        "training_terakhir": latest.trained_at.isoformat() if latest else None,
        "jumlah_dataset_training": latest.dataset_count if latest else None,
        "accuracy_terakhir": latest.accuracy if latest else None,
        "database_skripsi": settings.app_database_name,
        "database_sumber": settings.source_database_name,
    }


def predict_record(db: Session, record: dict, customer_code: str | None = None) -> dict:
    artifact = load_artifact()
    model: Pipeline = artifact["model"]
    feature_values = ambil_fitur_kategorikal([record])
    prediction = str(model.predict(feature_values)[0])
    probabilities = _probabilitas(model, feature_values)

    log = PredictionLog(
        customer_code=customer_code,
        input_json=json.dumps(record, ensure_ascii=False),
        risiko_piutang=prediction,
        probabilitas_json=json.dumps(probabilities),
    )
    db.add(log)
    db.commit()

    return {
        "risiko_piutang": prediction,
        "probabilitas": probabilities,
        "fitur": record,
        "label_aturan": record.get("risiko_piutang"),
    }


def predict_customer(db: Session, customer_code: str) -> dict:
    row = db.scalars(
        select(DatasetRisikoPiutang).where(DatasetRisikoPiutang.customer_code == customer_code)
    ).first()

    if row:
        record = dataset_row_to_dict(row)
    else:
        records = ambil_dataset_dari_database_sumber(customer_code=customer_code)
        if not records:
            return {
                "risiko_piutang": "rendah",
                "probabilitas": {"rendah": 1.0, "sedang": 0.0, "tinggi": 0.0},
                "fitur": {"customer_code": customer_code},
                "label_aturan": "rendah",
                "pesan": "Pelanggan tidak memiliki piutang outstanding pada data sumber.",
            }
        record = records[0]

    hasil = predict_record(db, record, customer_code=customer_code)
    hasil["pesan"] = "Prediksi risiko piutang pelanggan berhasil diproses."
    return hasil


def predict_manual(db: Session, payload: dict) -> dict:
    record = bentuk_record_manual(payload)
    hasil = predict_record(db, record, customer_code=payload.get("customer_code"))
    hasil["pesan"] = "Prediksi risiko piutang dari input manual berhasil diproses."
    return hasil
