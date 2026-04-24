from __future__ import annotations

from app.core.constants import FEATURE_CATEGORIES, FEATURE_COLUMNS


def kategori_umur_piutang(umur_piutang_hari: int | float | None) -> str:
    nilai = int(umur_piutang_hari or 0)
    if nilai <= 30:
        return "rendah"
    if nilai <= 60:
        return "sedang"
    return "tinggi"


def kategori_nominal_piutang(nominal_piutang: int | float | None) -> str:
    nilai = float(nominal_piutang or 0)
    if nilai <= 1_000_000:
        return "kecil"
    if nilai <= 8_000_000:
        return "sedang"
    return "besar"


def kategori_frekuensi_keterlambatan(frekuensi_keterlambatan: int | float | None) -> str:
    nilai = int(frekuensi_keterlambatan or 0)
    if nilai <= 4:
        return "jarang"
    if nilai <= 27:
        return "kadang"
    return "sering"


def kategori_invoice_belum_lunas(jumlah_invoice_belum_lunas: int | float | None) -> str:
    nilai = int(jumlah_invoice_belum_lunas or 0)
    if nilai <= 1:
        return "sedikit"
    if nilai <= 4:
        return "sedang"
    return "banyak"


def status_customer(umur_customer_hari: int | float | None) -> str:
    nilai = int(umur_customer_hari or 0)
    return "baru" if nilai <= 365 else "lama"


def hitung_skor_dan_label(record: dict) -> tuple[int, str]:
    skor = 0

    skor += {"rendah": 1, "sedang": 2, "tinggi": 3}.get(
        record["kategori_umur_piutang"],
        1,
    )
    skor += {"kecil": 1, "sedang": 2, "besar": 3}.get(
        record["kategori_nominal_piutang"],
        1,
    )
    skor += {"jarang": 1, "kadang": 2, "sering": 3}.get(
        record["kategori_frekuensi_keterlambatan"],
        1,
    )
    skor += {"sedikit": 1, "sedang": 2, "banyak": 3}.get(
        record["kategori_invoice_belum_lunas"],
        1,
    )
    skor += 1 if record["status_customer"] == "baru" else 0

    if skor <= 6:
        return skor, "rendah"
    if skor <= 9:
        return skor, "sedang"
    return skor, "tinggi"


def bentuk_record_dataset(record: dict, source_database: str) -> dict:
    hasil = {
        "customer_code": str(record.get("customer_code") or ""),
        "customer_name": str(record.get("customer_name") or "-"),
        "customer_type": record.get("customer_type") or "-",
        "top_hari": int(record.get("top_hari") or 30),
        "umur_piutang_hari": int(record.get("umur_piutang_hari") or 0),
        "nominal_piutang": float(record.get("nominal_piutang") or 0),
        "frekuensi_keterlambatan": int(record.get("frekuensi_keterlambatan") or 0),
        "jumlah_invoice_belum_lunas": int(record.get("jumlah_invoice_belum_lunas") or 0),
        "umur_customer_hari": int(record.get("umur_customer_hari") or 0),
        "source_database": source_database,
    }

    hasil["kategori_umur_piutang"] = kategori_umur_piutang(hasil["umur_piutang_hari"])
    hasil["kategori_nominal_piutang"] = kategori_nominal_piutang(hasil["nominal_piutang"])
    hasil["kategori_frekuensi_keterlambatan"] = kategori_frekuensi_keterlambatan(
        hasil["frekuensi_keterlambatan"]
    )
    hasil["kategori_invoice_belum_lunas"] = kategori_invoice_belum_lunas(
        hasil["jumlah_invoice_belum_lunas"]
    )
    hasil["status_customer"] = status_customer(hasil["umur_customer_hari"])

    skor, label = hitung_skor_dan_label(hasil)
    hasil["skor_risiko"] = skor
    hasil["risiko_piutang"] = label
    return hasil


def bentuk_record_manual(record: dict) -> dict:
    return bentuk_record_dataset(
        {
            "customer_code": record.get("customer_code") or "manual",
            "customer_name": record.get("customer_name") or "Input Manual",
            "customer_type": record.get("customer_type") or "-",
            "top_hari": record.get("top_hari") or 30,
            "umur_piutang_hari": record.get("umur_piutang_hari") or 0,
            "nominal_piutang": record.get("nominal_piutang") or 0,
            "frekuensi_keterlambatan": record.get("frekuensi_keterlambatan") or 0,
            "jumlah_invoice_belum_lunas": record.get("jumlah_invoice_belum_lunas") or 0,
            "umur_customer_hari": record.get("umur_customer_hari") or 366,
        },
        source_database="input_manual",
    )


def encode_features(records: list[dict]) -> list[list[int]]:
    encoded_rows: list[list[int]] = []
    for record in records:
        row = []
        for column in FEATURE_COLUMNS:
            categories = FEATURE_CATEGORIES[column]
            value = record.get(column) or "tidak_diketahui"
            row.append(categories.index(value) if value in categories else 0)
        encoded_rows.append(row)
    return encoded_rows


def ambil_fitur_kategorikal(records: list[dict]) -> list[list[str]]:
    return [
        [
            record.get(column)
            if record.get(column) in FEATURE_CATEGORIES[column]
            else "tidak_diketahui"
            for column in FEATURE_COLUMNS
        ]
        for record in records
    ]
