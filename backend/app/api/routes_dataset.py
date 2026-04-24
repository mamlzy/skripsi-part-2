from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.database import get_app_db
from app.services.dataset_service import generate_dataset, preview_dataset
from app.services.excel_service import export_dataset_excel, export_dataset_raw_excel


router = APIRouter()


@router.post(
    "/generate",
    summary="Generate dataset klasifikasi",
    description="Membaca data real dari database sumber lalu menyimpannya ke database lokal backend skripsi.",
)
def generate(db: Session = Depends(get_app_db)) -> dict:
    summary = generate_dataset(db)
    return {
        "message": "Dataset berhasil digenerate dan disimpan ke database backend skripsi.",
        "data": summary,
    }


@router.get(
    "/preview",
    summary="Preview dataset",
    description="Menampilkan sebagian dataset yang sudah tersimpan pada database backend skripsi.",
)
def preview(limit: int = Query(default=10, ge=1, le=100), db: Session = Depends(get_app_db)) -> dict:
    return {
        "message": "Preview dataset berhasil diambil.",
        "data": preview_dataset(db, limit=limit),
    }


@router.post(
    "/export-excel",
    summary="Export dataset ke Excel",
    description="Membuat file Excel dataset risiko piutang dari data lokal backend skripsi.",
)
def export_excel(db: Session = Depends(get_app_db)) -> dict:
    result = export_dataset_excel(db)
    return {
        "message": "Dataset berhasil diexport ke file Excel.",
        "data": result,
    }


@router.post(
    "/export-raw-excel",
    summary="Export dataset raw ke Excel",
    description="Membuat file Excel dataset raw/numerik sebelum fitur dikategorikan untuk model.",
)
def export_raw_excel(db: Session = Depends(get_app_db)) -> dict:
    result = export_dataset_raw_excel(db)
    return {
        "message": "Dataset raw berhasil diexport ke file Excel.",
        "data": result,
    }


@router.get(
    "/download-excel",
    summary="Download dataset Excel",
    description="Mengunduh file Excel dataset risiko piutang terakhir.",
)
def download_excel() -> FileResponse:
    path = get_settings().dataset_excel_path
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail="File Excel belum tersedia. Jalankan endpoint export-excel terlebih dahulu.",
        )
    return FileResponse(
        path=path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=path.name,
    )


@router.get(
    "/download-raw-excel",
    summary="Download dataset raw Excel",
    description="Mengunduh file Excel dataset raw/numerik terakhir.",
)
def download_raw_excel() -> FileResponse:
    path = get_settings().raw_dataset_excel_path
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail="File Excel raw belum tersedia. Jalankan endpoint export-raw-excel terlebih dahulu.",
        )
    return FileResponse(
        path=path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=path.name,
    )
