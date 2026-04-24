from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.db.database import SessionLocal, init_app_db  # noqa: E402
from app.services.dataset_service import generate_dataset  # noqa: E402
from app.services.excel_service import export_dataset_excel, export_dataset_raw_excel  # noqa: E402
from app.services.model_service import train_model  # noqa: E402


def main() -> None:
    init_app_db()
    with SessionLocal() as db:
        dataset_summary = generate_dataset(db)
        excel_summary = export_dataset_excel(db)
        raw_excel_summary = export_dataset_raw_excel(db)
        evaluation = train_model(db)

    print("Dataset berhasil dibuat.")
    print(f"Jumlah baris: {dataset_summary['jumlah_baris']}")
    print(f"Distribusi label: {dataset_summary['distribusi_label']}")
    print(f"File Excel: {excel_summary['file']}")
    print(f"File Excel raw: {raw_excel_summary['file']}")
    print(f"Accuracy model: {evaluation['accuracy']:.4f}")


if __name__ == "__main__":
    main()
