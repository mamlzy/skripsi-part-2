from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.constants import ATURAN_FITUR, ATURAN_LABEL
from app.services.dataset_service import ambil_dataset_atau_generate


def export_dataset_excel(db: Session) -> dict:
    settings = get_settings()
    records = ambil_dataset_atau_generate(db)
    path = settings.dataset_excel_path

    distribusi = Counter(record["risiko_piutang"] for record in records)
    df = pd.DataFrame(records)

    kolom_dataset = [
        "customer_code",
        "customer_name",
        "customer_type",
        "kategori_umur_piutang",
        "kategori_nominal_piutang",
        "kategori_frekuensi_keterlambatan",
        "kategori_invoice_belum_lunas",
        "status_customer",
        "skor_risiko",
        "risiko_piutang",
    ]
    kolom_numerik = [
        "customer_code",
        "customer_name",
        "customer_type",
        "top_hari",
        "umur_piutang_hari",
        "nominal_piutang",
        "frekuensi_keterlambatan",
        "jumlah_invoice_belum_lunas",
        "umur_customer_hari",
        "skor_risiko",
        "risiko_piutang",
    ]

    ringkasan = pd.DataFrame(
        [
            {"keterangan": "Tanggal ekspor", "nilai": datetime.now().isoformat(timespec="seconds")},
            {"keterangan": "Database sumber", "nilai": settings.source_database_name},
            {"keterangan": "Database backend skripsi", "nilai": settings.app_database_name},
            {"keterangan": "Jumlah baris dataset", "nilai": len(records)},
            {"keterangan": "Label rendah", "nilai": distribusi.get("rendah", 0)},
            {"keterangan": "Label sedang", "nilai": distribusi.get("sedang", 0)},
            {"keterangan": "Label tinggi", "nilai": distribusi.get("tinggi", 0)},
        ]
    )

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df[kolom_dataset].to_excel(writer, sheet_name="dataset", index=False)
        df[kolom_numerik].to_excel(writer, sheet_name="data_numerik", index=False)
        pd.DataFrame(ATURAN_FITUR).to_excel(writer, sheet_name="aturan_fitur", index=False)
        pd.DataFrame(ATURAN_LABEL).to_excel(writer, sheet_name="aturan_label", index=False)
        ringkasan.to_excel(writer, sheet_name="ringkasan", index=False)

        for worksheet in writer.book.worksheets:
            worksheet.freeze_panes = "A2"
            for column_cells in worksheet.columns:
                max_length = max(len(str(cell.value or "")) for cell in column_cells)
                worksheet.column_dimensions[column_cells[0].column_letter].width = min(
                    max(max_length + 2, 12),
                    48,
                )

    return {
        "file": str(path),
        "nama_file": Path(path).name,
        "jumlah_baris": len(records),
        "distribusi_label": {
            "rendah": distribusi.get("rendah", 0),
            "sedang": distribusi.get("sedang", 0),
            "tinggi": distribusi.get("tinggi", 0),
        },
    }


def export_dataset_raw_excel(db: Session) -> dict:
    settings = get_settings()
    records = ambil_dataset_atau_generate(db)
    path = settings.raw_dataset_excel_path

    distribusi = Counter(record["risiko_piutang"] for record in records)
    df = pd.DataFrame(records)

    kolom_raw = [
        "customer_code",
        "customer_name",
        "customer_type",
        "top_hari",
        "umur_piutang_hari",
        "nominal_piutang",
        "frekuensi_keterlambatan",
        "jumlah_invoice_belum_lunas",
        "umur_customer_hari",
        "skor_risiko",
        "risiko_piutang",
        "source_database",
    ]
    kolom_pembanding = [
        "customer_code",
        "customer_name",
        "umur_piutang_hari",
        "kategori_umur_piutang",
        "nominal_piutang",
        "kategori_nominal_piutang",
        "frekuensi_keterlambatan",
        "kategori_frekuensi_keterlambatan",
        "jumlah_invoice_belum_lunas",
        "kategori_invoice_belum_lunas",
        "umur_customer_hari",
        "status_customer",
        "risiko_piutang",
    ]

    ringkasan = pd.DataFrame(
        [
            {"keterangan": "Tanggal ekspor", "nilai": datetime.now().isoformat(timespec="seconds")},
            {"keterangan": "Jenis dataset", "nilai": "Raw/numerik sebelum fitur dikategorikan untuk model"},
            {"keterangan": "Database sumber", "nilai": settings.source_database_name},
            {"keterangan": "Database backend skripsi", "nilai": settings.app_database_name},
            {"keterangan": "Jumlah baris dataset", "nilai": len(records)},
            {"keterangan": "Label rendah", "nilai": distribusi.get("rendah", 0)},
            {"keterangan": "Label sedang", "nilai": distribusi.get("sedang", 0)},
            {"keterangan": "Label tinggi", "nilai": distribusi.get("tinggi", 0)},
        ]
    )
    keterangan_kolom = pd.DataFrame(
        [
            {"kolom": "umur_piutang_hari", "keterangan": "Umur invoice outstanding paling lama dalam hari."},
            {"kolom": "nominal_piutang", "keterangan": "Total sisa piutang pelanggan dalam rupiah."},
            {"kolom": "frekuensi_keterlambatan", "keterangan": "Jumlah riwayat pembayaran yang melewati jatuh tempo."},
            {"kolom": "jumlah_invoice_belum_lunas", "keterangan": "Jumlah invoice pelanggan yang masih outstanding."},
            {"kolom": "umur_customer_hari", "keterangan": "Umur pelanggan sejak early_period atau createdAt."},
            {"kolom": "skor_risiko", "keterangan": "Skor aturan bisnis untuk membentuk label risiko_piutang."},
            {"kolom": "risiko_piutang", "keterangan": "Label target akhir: rendah, sedang, atau tinggi."},
        ]
    )

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df[kolom_raw].to_excel(writer, sheet_name="dataset_raw", index=False)
        df[kolom_pembanding].to_excel(writer, sheet_name="pembanding_kategori", index=False)
        keterangan_kolom.to_excel(writer, sheet_name="keterangan_kolom", index=False)
        pd.DataFrame(ATURAN_FITUR).to_excel(writer, sheet_name="aturan_kategorisasi", index=False)
        ringkasan.to_excel(writer, sheet_name="ringkasan", index=False)

        for worksheet in writer.book.worksheets:
            worksheet.freeze_panes = "A2"
            for column_cells in worksheet.columns:
                max_length = max(len(str(cell.value or "")) for cell in column_cells)
                worksheet.column_dimensions[column_cells[0].column_letter].width = min(
                    max(max_length + 2, 12),
                    58,
                )

    return {
        "file": str(path),
        "nama_file": Path(path).name,
        "jumlah_baris": len(records),
        "distribusi_label": {
            "rendah": distribusi.get("rendah", 0),
            "sedang": distribusi.get("sedang", 0),
            "tinggi": distribusi.get("tinggi", 0),
        },
    }
