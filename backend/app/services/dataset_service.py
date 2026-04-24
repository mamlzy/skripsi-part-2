from __future__ import annotations

from collections import Counter
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.dataset import DatasetRisikoPiutang
from app.services.source_data_service import ambil_dataset_dari_database_sumber


DATASET_COLUMNS = [
    "customer_code",
    "customer_name",
    "customer_type",
    "top_hari",
    "umur_piutang_hari",
    "nominal_piutang",
    "frekuensi_keterlambatan",
    "jumlah_invoice_belum_lunas",
    "umur_customer_hari",
    "kategori_umur_piutang",
    "kategori_nominal_piutang",
    "kategori_frekuensi_keterlambatan",
    "kategori_invoice_belum_lunas",
    "status_customer",
    "skor_risiko",
    "risiko_piutang",
    "source_database",
]


def dataset_row_to_dict(row: DatasetRisikoPiutang) -> dict:
    return {column: getattr(row, column) for column in DATASET_COLUMNS}


def simpan_dataset_ke_database_lokal(db: Session, records: list[dict]) -> dict:
    db.query(DatasetRisikoPiutang).delete()
    generated_at = datetime.utcnow()
    db.add_all(
        DatasetRisikoPiutang(**record, generated_at=generated_at)
        for record in records
    )
    db.commit()

    distribusi = Counter(record["risiko_piutang"] for record in records)
    return {
        "jumlah_baris": len(records),
        "distribusi_label": {
            "rendah": distribusi.get("rendah", 0),
            "sedang": distribusi.get("sedang", 0),
            "tinggi": distribusi.get("tinggi", 0),
        },
        "database_sumber": get_settings().source_database_name,
        "database_skripsi": get_settings().app_database_name,
        "generated_at": generated_at.isoformat(),
    }


def generate_dataset(db: Session) -> dict:
    records = ambil_dataset_dari_database_sumber()
    return simpan_dataset_ke_database_lokal(db, records)


def ambil_dataset_lokal(db: Session) -> list[dict]:
    rows = db.scalars(select(DatasetRisikoPiutang).order_by(DatasetRisikoPiutang.customer_name)).all()
    return [dataset_row_to_dict(row) for row in rows]


def preview_dataset(db: Session, limit: int = 10) -> dict:
    rows = db.scalars(
        select(DatasetRisikoPiutang)
        .order_by(DatasetRisikoPiutang.customer_name)
        .limit(limit)
    ).all()
    total = db.query(DatasetRisikoPiutang).count()
    distribusi = Counter(row.risiko_piutang for row in db.query(DatasetRisikoPiutang).all())
    return {
        "jumlah_total": total,
        "distribusi_label": {
            "rendah": distribusi.get("rendah", 0),
            "sedang": distribusi.get("sedang", 0),
            "tinggi": distribusi.get("tinggi", 0),
        },
        "data": [dataset_row_to_dict(row) for row in rows],
    }


def ambil_dataset_atau_generate(db: Session) -> list[dict]:
    records = ambil_dataset_lokal(db)
    if records:
        return records
    generate_dataset(db)
    return ambil_dataset_lokal(db)
