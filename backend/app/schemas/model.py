from pydantic import BaseModel, Field, model_validator


class PredictRequest(BaseModel):
    customer_code: str | None = Field(
        default=None,
        description="Kode pelanggan. Jika diisi, fitur diambil dari data piutang pelanggan.",
    )
    customer_name: str | None = Field(default=None, description="Nama pelanggan untuk input manual.")
    customer_type: str | None = Field(default=None, description="Tipe pelanggan untuk input manual.")
    top_hari: int | None = Field(default=30, ge=0, description="Termin pembayaran dalam hari.")
    umur_piutang_hari: int | None = Field(default=None, ge=0, description="Umur piutang dalam hari.")
    nominal_piutang: float | None = Field(default=None, ge=0, description="Nominal piutang.")
    frekuensi_keterlambatan: int | None = Field(
        default=None,
        ge=0,
        description="Frekuensi keterlambatan pembayaran.",
    )
    jumlah_invoice_belum_lunas: int | None = Field(
        default=None,
        ge=0,
        description="Jumlah invoice yang belum lunas.",
    )
    umur_customer_hari: int | None = Field(
        default=None,
        ge=0,
        description="Umur pelanggan dalam hari.",
    )

    @model_validator(mode="after")
    def validasi_input(self) -> "PredictRequest":
        if self.customer_code:
            return self

        required = [
            self.umur_piutang_hari,
            self.nominal_piutang,
            self.frekuensi_keterlambatan,
            self.jumlah_invoice_belum_lunas,
            self.umur_customer_hari,
        ]
        if any(value is None for value in required):
            raise ValueError(
                "Isi customer_code atau lengkapi semua fitur manual untuk prediksi."
            )
        return self
