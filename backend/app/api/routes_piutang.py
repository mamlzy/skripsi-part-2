from fastapi import APIRouter, HTTPException, Query

from app.services.source_data_service import ambil_dataset_dari_database_sumber


router = APIRouter()


@router.get(
    "/pelanggan",
    summary="Ambil data piutang pelanggan dari database sumber",
    description="Mengambil data piutang pelanggan yang dihitung dari invoice dan pembayaran mysml-backend.",
)
def list_piutang_pelanggan(limit: int = Query(default=20, ge=1, le=500)) -> dict:
    records = ambil_dataset_dari_database_sumber()
    return {
        "message": "Data piutang pelanggan berhasil diambil dari database sumber.",
        "jumlah_total": len(records),
        "data": records[:limit],
    }


@router.get(
    "/pelanggan/{customer_code}",
    summary="Ambil piutang satu pelanggan",
    description="Mengambil fitur piutang untuk satu pelanggan berdasarkan customer_code.",
)
def detail_piutang_pelanggan(customer_code: str) -> dict:
    records = ambil_dataset_dari_database_sumber(customer_code=customer_code)
    if not records:
        raise HTTPException(
            status_code=404,
            detail="Data piutang outstanding untuk pelanggan tersebut tidak ditemukan.",
        )
    return {
        "message": "Data piutang pelanggan berhasil diambil.",
        "data": records[0],
    }
