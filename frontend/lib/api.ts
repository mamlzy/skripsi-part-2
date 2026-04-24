const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api"

type ApiEnvelope<T> = {
  message?: string
  data?: T
  detail?: string
}

export type RisikoLabel = "rendah" | "sedang" | "tinggi"

export type HealthResponse = {
  status: string
  message: string
  database_sumber: {
    nama: string
    status: string
    error: string | null
    mode: string
  }
  database_skripsi: {
    nama: string
    status: string
    error: string | null
    mode: string
  }
}

export type DatasetRow = {
  customer_code: string
  customer_name: string
  customer_type: string
  top_hari: number
  umur_piutang_hari: number
  nominal_piutang: number
  frekuensi_keterlambatan: number
  jumlah_invoice_belum_lunas: number
  umur_customer_hari: number
  kategori_umur_piutang: string
  kategori_nominal_piutang: string
  kategori_frekuensi_keterlambatan: string
  kategori_invoice_belum_lunas: string
  status_customer: string
  skor_risiko: number
  risiko_piutang: RisikoLabel
  source_database: string
}

export type DatasetPreview = {
  jumlah_total: number
  distribusi_label: Record<RisikoLabel, number>
  data: DatasetRow[]
}

export type DatasetActionResult = {
  jumlah_baris?: number
  jumlah_total?: number
  distribusi_label?: Record<RisikoLabel, number>
  database_sumber?: string
  database_skripsi?: string
  generated_at?: string
  file?: string
  nama_file?: string
}

export type EvaluationResponse = {
  accuracy: number
  macro_avg: {
    precision: number
    recall: number
    f1_score: number
  }
  weighted_avg: {
    precision: number
    recall: number
    f1_score: number
  }
  classification_report: Record<string, unknown>
  confusion_matrix: {
    labels: RisikoLabel[]
    matrix: number[][]
  }
  jumlah_data: number
  jumlah_data_latih: number
  jumlah_data_uji: number
}

export type ModelInfo = {
  model_tersedia: boolean
  path_model: string
  evaluasi_tersedia: boolean
  training_terakhir: string | null
  jumlah_dataset_training: number | null
  accuracy_terakhir: number | null
  database_skripsi: string
  database_sumber: string
}

export type ReferensiResponse = {
  target: string
  kelas_label: RisikoLabel[]
  fitur_model: string[]
  aturan_fitur: Array<{
    fitur: string
    kategori: string
    aturan: string
    skor: number
  }>
  aturan_label: Array<{
    risiko_piutang: RisikoLabel
    aturan: string
  }>
}

export type PredictPayload =
  | { customer_code: string }
  | {
      customer_name?: string
      customer_type?: string
      top_hari?: number
      umur_piutang_hari: number
      nominal_piutang: number
      frekuensi_keterlambatan: number
      jumlah_invoice_belum_lunas: number
      umur_customer_hari: number
    }

export type PredictResponse = {
  risiko_piutang: RisikoLabel
  probabilitas: Record<RisikoLabel, number>
  fitur: Partial<DatasetRow>
  label_aturan: RisikoLabel
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  })
  const payload = (await response.json().catch(() => ({}))) as ApiEnvelope<T>

  if (!response.ok) {
    throw new Error(payload.detail || payload.message || "Permintaan API gagal.")
  }

  return (payload.data ?? payload) as T
}

export const api = {
  baseUrl: API_BASE_URL,
  downloadExcelUrl: `${API_BASE_URL}/dataset/download-excel`,
  downloadRawExcelUrl: `${API_BASE_URL}/dataset/download-raw-excel`,
  health: () => request<HealthResponse>("/health"),
  referensi: () => request<ReferensiResponse>("/referensi/fitur"),
  previewDataset: (limit = 10) =>
    request<DatasetPreview>(`/dataset/preview?limit=${limit}`),
  generateDataset: () =>
    request<DatasetActionResult>("/dataset/generate", { method: "POST" }),
  exportExcel: () =>
    request<DatasetActionResult>("/dataset/export-excel", { method: "POST" }),
  exportRawExcel: () =>
    request<DatasetActionResult>("/dataset/export-raw-excel", { method: "POST" }),
  trainModel: () =>
    request<EvaluationResponse>("/model/train", { method: "POST" }),
  evaluateModel: () => request<EvaluationResponse>("/model/evaluate"),
  modelInfo: () => request<ModelInfo>("/model/info"),
  predict: (payload: PredictPayload) =>
    request<PredictResponse>("/model/predict", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
}
