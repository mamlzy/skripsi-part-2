# Backend Skripsi Risiko Piutang

Backend ini dibuat untuk mendukung skripsi berjudul **Model Klasifikasi Piutang Pelanggan dengan Metode Naive Bayes pada PT Sarana Mulya Logistik**.

Sistem ini membaca data real dari database `mysml-backend`, membentuk dataset klasifikasi risiko piutang pelanggan, menyimpan dataset ke database lokal milik backend skripsi, mengekspor dataset ke Excel, melatih model Naive Bayes, dan menyediakan endpoint prediksi.

## Prinsip Database

Backend ini memakai dua database:

- `SOURCE_DATABASE_URL`: database sumber `mysml-backend`, hanya untuk membaca data real.
- `APP_DATABASE_URL`: database milik backend skripsi sendiri untuk menyimpan dataset hasil olahan, log prediksi, dan metadata training.

Database `mysml-backend` tidak ditulis atau diubah oleh backend skripsi.

## Requirement

- Python 3.11 atau lebih baru
- MySQL/MariaDB lokal yang berisi database `mysml-backend`
- Paket Python pada `requirements.txt`

## Setup Backend

```bash
cd skripsi/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Contoh konfigurasi `.env`:

```env
SOURCE_DATABASE_URL=mysql+pymysql://user:password@localhost:3306/lms_prod_sml_03_04_26
APP_DATABASE_URL=sqlite:///./storage/skripsi_backend.db
APP_HOST=127.0.0.1
APP_PORT=8000
APP_DEBUG=true
```

`APP_DATABASE_URL` adalah database backend skripsi sendiri. Default SQLite sudah cukup untuk kebutuhan skripsi. Jika ingin memakai MySQL sendiri, buat database baru lalu ubah nilainya, misalnya:

```env
APP_DATABASE_URL=mysql+pymysql://user:password@localhost:3306/skripsi_risiko_piutang
```

## Menjalankan Backend

```bash
cd skripsi/backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Dokumentasi API:

```text
http://127.0.0.1:8000/docs
```

## Generate Dataset Dan Excel

Lewat script:

```bash
cd skripsi/backend
source .venv/bin/activate
python scripts/generate_dataset_excel.py
```

Lewat API:

```bash
curl -X POST http://127.0.0.1:8000/api/dataset/generate
curl -X POST http://127.0.0.1:8000/api/dataset/export-excel
curl -X POST http://127.0.0.1:8000/api/dataset/export-raw-excel
```

Download Excel:

```text
http://127.0.0.1:8000/api/dataset/download-excel
http://127.0.0.1:8000/api/dataset/download-raw-excel
```

Lokasi file Excel:

```text
storage/dataset/dataset_risiko_piutang.xlsx
storage/dataset/dataset_risiko_piutang_raw.xlsx
```

`dataset_risiko_piutang.xlsx` berisi dataset kategorikal untuk model. `dataset_risiko_piutang_raw.xlsx` berisi fitur numerik asli agar proses sebelum dan sesudah kategorisasi bisa dibandingkan.

## Training Dan Evaluasi Model

Training:

```bash
curl -X POST http://127.0.0.1:8000/api/model/train
```

Evaluasi:

```bash
curl http://127.0.0.1:8000/api/model/evaluate
```

Metrik evaluasi yang disediakan:

- accuracy
- precision
- recall
- f1-score
- confusion matrix
- classification report per kelas

## Prediksi

Prediksi berdasarkan kode pelanggan:

```bash
curl -X POST http://127.0.0.1:8000/api/model/predict \
  -H "Content-Type: application/json" \
  -d '{"customer_code":"KODE_CUSTOMER"}'
```

Prediksi dengan input manual:

```bash
curl -X POST http://127.0.0.1:8000/api/model/predict \
  -H "Content-Type: application/json" \
  -d '{
    "umur_piutang_hari": 75,
    "nominal_piutang": 12000000,
    "frekuensi_keterlambatan": 10,
    "jumlah_invoice_belum_lunas": 5,
    "umur_customer_hari": 800
  }'
```

## Fitur Model

Dataset dibuat pada level pelanggan dengan fitur:

- `umur_piutang_hari`
- `nominal_piutang`
- `frekuensi_keterlambatan`
- `jumlah_invoice_belum_lunas`
- `status_customer`

Fitur numerik dikategorikan, lalu diencode dengan `OrdinalEncoder` di dalam pipeline model sebelum diproses oleh `CategoricalNB`.

## Aturan Label Risiko Piutang

Target klasifikasi adalah `risiko_piutang` dengan tiga kelas:

- `rendah`
- `sedang`
- `tinggi`

Aturan skor:

- Umur piutang: `0-30=rendah`, `31-60=sedang`, `>60=tinggi`.
- Nominal piutang: `<=1.000.000=kecil`, `1.000.001-8.000.000=sedang`, `>8.000.000=besar`.
- Frekuensi keterlambatan: `<=4=jarang`, `5-27=kadang`, `>27=sering`.
- Invoice belum lunas: `<=1=sedikit`, `2-4=sedang`, `>4=banyak`.
- Status customer: `baru` jika umur customer <= 365 hari, selain itu `lama`.

Label akhir:

- `rendah` jika skor <= 6
- `sedang` jika skor 7 sampai 9
- `tinggi` jika skor >= 10

## Menjalankan Frontend

```bash
cd skripsi/frontend
pnpm install
pnpm dev --hostname 127.0.0.1 --port 3000
```

Jika frontend perlu membaca backend, buat `.env.local` di `skripsi/frontend`:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api
```

Buka frontend:

```text
http://127.0.0.1:3000
```
