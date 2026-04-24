from __future__ import annotations

from sqlalchemy import text

from app.core.config import get_settings
from app.db.database import source_engine
from app.ml.preprocessing import bentuk_record_dataset


DATASET_QUERY = """
WITH invoice_paid AS (
    SELECT
        i.customer_code,
        i.invoice_no,
        i.total,
        COALESCE(i.invoice_receipt_date, i.invoice_date) AS tanggal_awal,
        CAST(COALESCE(NULLIF(REGEXP_SUBSTR(c.top, '[0-9]+'), ''), '30') AS UNSIGNED) AS top_hari,
        COALESCE(SUM(CASE WHEN ip.payment_no IS NOT NULL THEN ipi.payment_amount ELSE 0 END), 0) AS total_bayar,
        MAX(CASE WHEN ip.payment_no IS NOT NULL THEN ip.payment_date ELSE NULL END) AS pembayaran_terakhir
    FROM invoice i
    JOIN customer c ON c.customer_code = i.customer_code
    LEFT JOIN invoice_payment_item ipi
        ON ipi.invoice_no = i.invoice_no
        AND ipi.deletedAt IS NULL
        AND (ipi.status <> 'VOID' OR ipi.status IS NULL)
    LEFT JOIN invoice_payment ip
        ON ip.payment_no = ipi.payment_no
        AND ip.deletedAt IS NULL
        AND (ip.status <> 'VOID' OR ip.status IS NULL)
    WHERE i.deletedAt IS NULL
        AND i.status = 'CONFIRMED'
        AND (:customer_code IS NULL OR i.customer_code = :customer_code)
    GROUP BY
        i.customer_code,
        i.invoice_no,
        i.total,
        i.invoice_receipt_date,
        i.invoice_date,
        c.top
),
fitur AS (
    SELECT
        c.customer_code,
        c.customer_name,
        COALESCE(ct.name, '-') AS customer_type,
        CAST(COALESCE(NULLIF(REGEXP_SUBSTR(c.top, '[0-9]+'), ''), '30') AS UNSIGNED) AS top_hari,
        SUM(CASE WHEN ip.total - ip.total_bayar > 0 THEN ip.total - ip.total_bayar ELSE 0 END) AS nominal_piutang,
        SUM(CASE WHEN ip.total - ip.total_bayar > 0 THEN 1 ELSE 0 END) AS jumlah_invoice_belum_lunas,
        MAX(CASE WHEN ip.total - ip.total_bayar > 0 THEN DATEDIFF(CURDATE(), DATE(ip.tanggal_awal)) ELSE 0 END) AS umur_piutang_hari,
        SUM(
            CASE
                WHEN ip.pembayaran_terakhir IS NOT NULL
                    AND ip.pembayaran_terakhir > DATE_ADD(ip.tanggal_awal, INTERVAL ip.top_hari DAY)
                THEN 1
                ELSE 0
            END
        ) AS frekuensi_keterlambatan,
        DATEDIFF(CURDATE(), DATE(COALESCE(c.early_period, c.createdAt))) AS umur_customer_hari
    FROM invoice_paid ip
    JOIN customer c ON c.customer_code = ip.customer_code
    LEFT JOIN customer_type ct ON ct.id = c.customer_type_id
    GROUP BY
        c.customer_code,
        c.customer_name,
        ct.name,
        c.top,
        c.early_period,
        c.createdAt
    HAVING nominal_piutang > 0
)
SELECT
    customer_code,
    customer_name,
    customer_type,
    top_hari,
    umur_piutang_hari,
    nominal_piutang,
    frekuensi_keterlambatan,
    jumlah_invoice_belum_lunas,
    umur_customer_hari
FROM fitur
ORDER BY customer_name ASC
"""


def ambil_dataset_dari_database_sumber(customer_code: str | None = None) -> list[dict]:
    settings = get_settings()
    with source_engine.connect() as conn:
        result = conn.execute(text(DATASET_QUERY), {"customer_code": customer_code})
        rows = [dict(row) for row in result.mappings().all()]

    return [
        bentuk_record_dataset(row, source_database=settings.source_database_name)
        for row in rows
    ]
