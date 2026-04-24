from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class DatasetRisikoPiutang(Base):
    __tablename__ = "dataset_risiko_piutang"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_code: Mapped[str] = mapped_column(String(255), index=True)
    customer_name: Mapped[str] = mapped_column(String(255))
    customer_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    top_hari: Mapped[int] = mapped_column(Integer, default=30)

    umur_piutang_hari: Mapped[int] = mapped_column(Integer, default=0)
    nominal_piutang: Mapped[float] = mapped_column(Float, default=0)
    frekuensi_keterlambatan: Mapped[int] = mapped_column(Integer, default=0)
    jumlah_invoice_belum_lunas: Mapped[int] = mapped_column(Integer, default=0)
    umur_customer_hari: Mapped[int] = mapped_column(Integer, default=0)

    kategori_umur_piutang: Mapped[str] = mapped_column(String(50))
    kategori_nominal_piutang: Mapped[str] = mapped_column(String(50))
    kategori_frekuensi_keterlambatan: Mapped[str] = mapped_column(String(50))
    kategori_invoice_belum_lunas: Mapped[str] = mapped_column(String(50))
    status_customer: Mapped[str] = mapped_column(String(50))

    skor_risiko: Mapped[int] = mapped_column(Integer)
    risiko_piutang: Mapped[str] = mapped_column(String(20), index=True)
    source_database: Mapped[str] = mapped_column(String(255))
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ModelTrainingRun(Base):
    __tablename__ = "model_training_run"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trained_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    model_path: Mapped[str] = mapped_column(String(500))
    dataset_count: Mapped[int] = mapped_column(Integer)
    test_size: Mapped[float] = mapped_column(Float)
    accuracy: Mapped[float] = mapped_column(Float)
    macro_precision: Mapped[float] = mapped_column(Float)
    macro_recall: Mapped[float] = mapped_column(Float)
    macro_f1: Mapped[float] = mapped_column(Float)
    weighted_precision: Mapped[float] = mapped_column(Float)
    weighted_recall: Mapped[float] = mapped_column(Float)
    weighted_f1: Mapped[float] = mapped_column(Float)
    report_json: Mapped[str] = mapped_column(Text)
    confusion_matrix_json: Mapped[str] = mapped_column(Text)


class PredictionLog(Base):
    __tablename__ = "prediction_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    predicted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    customer_code: Mapped[str | None] = mapped_column(String(255), nullable=True)
    input_json: Mapped[str] = mapped_column(Text)
    risiko_piutang: Mapped[str] = mapped_column(String(20))
    probabilitas_json: Mapped[str] = mapped_column(Text)
