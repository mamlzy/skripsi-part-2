from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "Backend Skripsi Risiko Piutang"
    app_description: str = (
        "API pendukung penelitian klasifikasi risiko piutang pelanggan "
        "menggunakan metode Naive Bayes."
    )
    app_version: str = "1.0.0"

    source_database_url: str = Field(
        ...,
        description="Koneksi database sumber mysml-backend, hanya untuk baca data.",
    )
    app_database_url: str = Field(
        default=f"sqlite:///{BASE_DIR / 'storage' / 'skripsi_backend.db'}",
        description="Koneksi database milik backend skripsi.",
    )

    app_host: str = "127.0.0.1"
    app_port: int = 8000
    app_debug: bool = True

    storage_dir: Path = BASE_DIR / "storage"
    dataset_dir: Path = BASE_DIR / "storage" / "dataset"
    model_dir: Path = BASE_DIR / "storage" / "model"

    dataset_excel_name: str = "dataset_risiko_piutang.xlsx"
    raw_dataset_excel_name: str = "dataset_risiko_piutang_raw.xlsx"
    model_file_name: str = "model_naive_bayes_piutang.joblib"
    evaluation_file_name: str = "evaluasi_model.json"

    test_size: float = 0.2
    random_state: int = 42

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def dataset_excel_path(self) -> Path:
        return self.dataset_dir / self.dataset_excel_name

    @property
    def raw_dataset_excel_path(self) -> Path:
        return self.dataset_dir / self.raw_dataset_excel_name

    @property
    def model_path(self) -> Path:
        return self.model_dir / self.model_file_name

    @property
    def evaluation_path(self) -> Path:
        return self.model_dir / self.evaluation_file_name

    @property
    def source_database_name(self) -> str:
        return make_url(self.source_database_url).database or "tidak_diketahui"

    @property
    def app_database_name(self) -> str:
        url = make_url(self.app_database_url)
        return url.database or str(url)

    def ensure_storage_dirs(self) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.dataset_dir.mkdir(parents=True, exist_ok=True)
        self.model_dir.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_storage_dirs()
    return settings
