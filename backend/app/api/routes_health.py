from fastapi import APIRouter

from app.core.config import get_settings
from app.db.database import check_app_database, check_source_database


router = APIRouter()


@router.get(
    "/health",
    summary="Cek kesehatan backend",
    description="Memeriksa status aplikasi, database sumber, dan database backend skripsi.",
)
def health_check() -> dict:
    settings = get_settings()
    source_ok = False
    app_ok = False
    source_error = None
    app_error = None

    try:
        source_ok = check_source_database()
    except Exception as exc:
        source_error = str(exc)

    try:
        app_ok = check_app_database()
    except Exception as exc:
        app_error = str(exc)

    return {
        "status": "sehat" if source_ok and app_ok else "perlu_diperiksa",
        "message": "Backend skripsi siap digunakan." if source_ok and app_ok else "Ada koneksi database yang perlu diperiksa.",
        "database_sumber": {
            "nama": settings.source_database_name,
            "status": "terhubung" if source_ok else "gagal",
            "error": source_error,
            "mode": "hanya_baca",
        },
        "database_skripsi": {
            "nama": settings.app_database_name,
            "status": "terhubung" if app_ok else "gagal",
            "error": app_error,
            "mode": "baca_tulis_lokal",
        },
    }
