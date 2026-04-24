# Frontend Skripsi Risiko Piutang

Frontend ini adalah dashboard untuk sistem klasifikasi risiko piutang pelanggan menggunakan Naive Bayes. Aplikasi membaca API dari backend FastAPI di `skripsi/backend`.

## Requirement

- Node.js
- pnpm
- Backend FastAPI berjalan di `http://127.0.0.1:8000`

## Konfigurasi

File `.env.local`:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api
```

## Menjalankan Backend

```bash
cd ../backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Menjalankan Frontend

```bash
cd skripsi/frontend
pnpm install
pnpm dev --hostname 127.0.0.1 --port 3000
```

Buka:

```text
http://127.0.0.1:3000
```

## Fitur Dashboard

- Cek status backend dan database.
- Preview dataset risiko piutang.
- Generate dataset.
- Export dan download dataset Excel.
- Training model Naive Bayes.
- Melihat evaluasi model.
- Prediksi risiko berdasarkan kode pelanggan.
- Simulasi prediksi manual.
