from fastapi import APIRouter

from app.core.constants import ATURAN_FITUR, ATURAN_LABEL, FEATURE_COLUMNS, LABEL_ORDER


router = APIRouter()


@router.get(
    "/fitur",
    summary="Lihat referensi fitur dan aturan label",
    description="Mengembalikan daftar fitur, kategori, dan aturan pembentukan label risiko piutang.",
)
def referensi_fitur() -> dict:
    return {
        "message": "Referensi fitur dan aturan label berhasil diambil.",
        "target": "risiko_piutang",
        "kelas_label": LABEL_ORDER,
        "fitur_model": FEATURE_COLUMNS,
        "aturan_fitur": ATURAN_FITUR,
        "aturan_label": ATURAN_LABEL,
    }
