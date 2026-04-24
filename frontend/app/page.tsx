"use client"

import {
  Activity,
  AlertCircle,
  BarChart3,
  Brain,
  CheckCircle2,
  Database,
  Download,
  FileSpreadsheet,
  Loader2,
  Play,
  RefreshCcw,
  Search,
  Server,
  ShieldCheck,
  Sparkles,
  Table2,
} from "lucide-react"
import { FormEvent, useEffect, useMemo, useState } from "react"

import { Button } from "@/components/ui/button"
import {
  api,
  DatasetPreview,
  EvaluationResponse,
  HealthResponse,
  ModelInfo,
  PredictResponse,
  ReferensiResponse,
  RisikoLabel,
} from "@/lib/api"
import { cn } from "@/lib/utils"

type LoadingKey =
  | "initial"
  | "refresh"
  | "generate"
  | "export"
  | "train"
  | "predictCustomer"
  | "predictManual"

type ManualForm = {
  umur_piutang_hari: string
  nominal_piutang: string
  frekuensi_keterlambatan: string
  jumlah_invoice_belum_lunas: string
  umur_customer_hari: string
}

const risikoConfig: Record<
  RisikoLabel,
  { label: string; className: string; bar: string }
> = {
  rendah: {
    label: "Rendah",
    className: "border-emerald-200 bg-emerald-50 text-emerald-700",
    bar: "bg-emerald-500",
  },
  sedang: {
    label: "Sedang",
    className: "border-amber-200 bg-amber-50 text-amber-700",
    bar: "bg-amber-500",
  },
  tinggi: {
    label: "Tinggi",
    className: "border-red-200 bg-red-50 text-red-700",
    bar: "bg-red-500",
  },
}

const initialManualForm: ManualForm = {
  umur_piutang_hari: "75",
  nominal_piutang: "12000000",
  frekuensi_keterlambatan: "10",
  jumlah_invoice_belum_lunas: "5",
  umur_customer_hari: "800",
}

function formatNumber(value: number | null | undefined) {
  if (value === null || value === undefined || Number.isNaN(value)) return "-"
  return new Intl.NumberFormat("id-ID").format(value)
}

function formatCurrency(value: number | null | undefined) {
  if (value === null || value === undefined || Number.isNaN(value)) return "-"
  return new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    maximumFractionDigits: 0,
  }).format(value)
}

function formatPercent(value: number | null | undefined) {
  if (value === null || value === undefined || Number.isNaN(value)) return "-"
  return `${(value * 100).toFixed(2)}%`
}

function formatDateTime(value: string | null | undefined) {
  if (!value) return "-"
  return new Intl.DateTimeFormat("id-ID", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value))
}

function Card({
  children,
  className,
}: {
  children: React.ReactNode
  className?: string
}) {
  return (
    <section className={cn("border border-border bg-card p-5", className)}>
      {children}
    </section>
  )
}

function SectionTitle({
  icon: Icon,
  title,
  description,
}: {
  icon: React.ElementType
  title: string
  description?: string
}) {
  return (
    <div className="mb-4 flex items-start gap-3">
      <div className="flex size-9 shrink-0 items-center justify-center border border-border bg-muted">
        <Icon className="size-4" />
      </div>
      <div className="min-w-0">
        <h2 className="text-base font-semibold">{title}</h2>
        {description ? (
          <p className="mt-1 text-sm text-muted-foreground">{description}</p>
        ) : null}
      </div>
    </div>
  )
}

function RisikoBadge({ value }: { value: RisikoLabel }) {
  const config = risikoConfig[value]
  return (
    <span
      className={cn(
        "inline-flex items-center border px-2 py-1 text-xs font-semibold",
        config.className
      )}
    >
      {config.label}
    </span>
  )
}

function TextInput({
  label,
  value,
  onChange,
  placeholder,
  type = "text",
}: {
  label: string
  value: string
  onChange: (value: string) => void
  placeholder?: string
  type?: "text" | "number"
}) {
  return (
    <label className="grid gap-1.5 text-sm">
      <span className="font-medium">{label}</span>
      <input
        type={type}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        className="h-10 border border-input bg-background px-3 text-sm outline-none transition focus:border-ring focus:ring-2 focus:ring-ring/20"
      />
    </label>
  )
}

export default function Page() {
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [dataset, setDataset] = useState<DatasetPreview | null>(null)
  const [evaluation, setEvaluation] = useState<EvaluationResponse | null>(null)
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null)
  const [referensi, setReferensi] = useState<ReferensiResponse | null>(null)
  const [loading, setLoading] = useState<LoadingKey | null>("initial")
  const [notice, setNotice] = useState<string>("")
  const [error, setError] = useState<string>("")
  const [customerCode, setCustomerCode] = useState("JKTB2B0080")
  const [manualForm, setManualForm] = useState<ManualForm>(initialManualForm)
  const [prediction, setPrediction] = useState<PredictResponse | null>(null)

  const totalDistribusi = useMemo(() => {
    if (!dataset) return 0
    return (
      dataset.distribusi_label.rendah +
      dataset.distribusi_label.sedang +
      dataset.distribusi_label.tinggi
    )
  }, [dataset])

  async function loadDashboard(mode: LoadingKey = "refresh") {
    setLoading(mode)
    setError("")
    try {
      const [healthResult, datasetResult, infoResult, referensiResult] =
        await Promise.all([
          api.health(),
          api.previewDataset(10),
          api.modelInfo(),
          api.referensi(),
        ])

      setHealth(healthResult)
      setDataset(datasetResult)
      setModelInfo(infoResult)
      setReferensi(referensiResult)

      try {
        setEvaluation(await api.evaluateModel())
      } catch {
        setEvaluation(null)
      }

      if (mode !== "initial") {
        setNotice("Data dashboard berhasil diperbarui.")
      }
    } catch (caught) {
      setError(
        caught instanceof Error
          ? caught.message
          : "Gagal mengambil data dashboard."
      )
    } finally {
      setLoading(null)
    }
  }

  useEffect(() => {
    const timeout = window.setTimeout(() => {
      void loadDashboard("initial")
    }, 0)

    return () => window.clearTimeout(timeout)
  }, [])

  async function runAction<T>(
    key: LoadingKey,
    action: () => Promise<T>,
    successMessage: string,
    after?: (result: T) => void
  ) {
    setLoading(key)
    setError("")
    setNotice("")
    try {
      const result = await action()
      after?.(result)
      setNotice(successMessage)
      await loadDashboard("refresh")
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Aksi gagal diproses.")
      setLoading(null)
    }
  }

  async function handleCustomerPredict(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!customerCode.trim()) {
      setError("Kode customer wajib diisi.")
      return
    }

    setLoading("predictCustomer")
    setError("")
    setNotice("")
    try {
      const result = await api.predict({ customer_code: customerCode.trim() })
      setPrediction(result)
      setNotice("Prediksi berdasarkan kode pelanggan berhasil diproses.")
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Prediksi gagal.")
    } finally {
      setLoading(null)
    }
  }

  async function handleManualPredict(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setLoading("predictManual")
    setError("")
    setNotice("")
    try {
      const result = await api.predict({
        umur_piutang_hari: Number(manualForm.umur_piutang_hari),
        nominal_piutang: Number(manualForm.nominal_piutang),
        frekuensi_keterlambatan: Number(
          manualForm.frekuensi_keterlambatan
        ),
        jumlah_invoice_belum_lunas: Number(
          manualForm.jumlah_invoice_belum_lunas
        ),
        umur_customer_hari: Number(manualForm.umur_customer_hari),
      })
      setPrediction(result)
      setNotice("Prediksi manual berhasil diproses.")
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Prediksi gagal.")
    } finally {
      setLoading(null)
    }
  }

  return (
    <main className="min-h-svh bg-background">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-5 px-4 py-5 sm:px-6 lg:px-8">
        <header className="flex flex-col gap-4 border-b border-border pb-5 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-3xl">
            <div className="mb-3 inline-flex items-center gap-2 border border-border bg-muted px-3 py-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              <ShieldCheck className="size-3.5" />
              Sistem Pendukung Skripsi
            </div>
            <h1 className="text-2xl font-semibold tracking-normal sm:text-3xl">
              Klasifikasi Risiko Piutang Pelanggan
            </h1>
            <p className="mt-2 text-sm leading-6 text-muted-foreground">
              Dashboard untuk membentuk dataset, melatih Naive Bayes,
              mengevaluasi model, dan memprediksi risiko piutang pelanggan PT
              Sarana Mulya Logistik.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <Button
              variant="outline"
              onClick={() => void loadDashboard("refresh")}
              disabled={loading !== null}
            >
              {loading === "refresh" ? (
                <Loader2 className="animate-spin" />
              ) : (
                <RefreshCcw />
              )}
              Segarkan
            </Button>
            <Button
              onClick={() => {
                window.location.href = api.downloadExcelUrl
              }}
            >
              <Download />
              Excel
            </Button>
            <Button
              variant="outline"
              onClick={() => {
                window.location.href = api.downloadRawExcelUrl
              }}
            >
              <Download />
              Excel Raw
            </Button>
          </div>
        </header>

        {error ? (
          <div className="flex items-start gap-3 border border-red-200 bg-red-50 p-3 text-sm text-red-700">
            <AlertCircle className="mt-0.5 size-4 shrink-0" />
            <span>{error}</span>
          </div>
        ) : null}
        {notice ? (
          <div className="flex items-start gap-3 border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
            <CheckCircle2 className="mt-0.5 size-4 shrink-0" />
            <span>{notice}</span>
          </div>
        ) : null}

        <section className="grid gap-4 lg:grid-cols-4">
          <Card>
            <div className="flex items-center gap-3">
              <Server className="size-5 text-muted-foreground" />
              <div>
                <p className="text-xs font-semibold uppercase text-muted-foreground">
                  Backend
                </p>
                <p className="mt-1 text-lg font-semibold">
                  {health?.status ?? "Memuat"}
                </p>
              </div>
            </div>
          </Card>
          <Card>
            <div className="flex items-center gap-3">
              <Database className="size-5 text-muted-foreground" />
              <div>
                <p className="text-xs font-semibold uppercase text-muted-foreground">
                  Database Sumber
                </p>
                <p className="mt-1 truncate text-lg font-semibold">
                  {health?.database_sumber.nama ?? "-"}
                </p>
              </div>
            </div>
          </Card>
          <Card>
            <div className="flex items-center gap-3">
              <Table2 className="size-5 text-muted-foreground" />
              <div>
                <p className="text-xs font-semibold uppercase text-muted-foreground">
                  Dataset
                </p>
                <p className="mt-1 text-lg font-semibold">
                  {formatNumber(dataset?.jumlah_total)} baris
                </p>
              </div>
            </div>
          </Card>
          <Card>
            <div className="flex items-center gap-3">
              <Brain className="size-5 text-muted-foreground" />
              <div>
                <p className="text-xs font-semibold uppercase text-muted-foreground">
                  Accuracy
                </p>
                <p className="mt-1 text-lg font-semibold">
                  {formatPercent(evaluation?.accuracy)}
                </p>
              </div>
            </div>
          </Card>
        </section>

        <section className="grid gap-5 xl:grid-cols-[1.35fr_0.65fr]">
          <Card>
            <SectionTitle
              icon={BarChart3}
              title="Ringkasan Dataset"
              description="Distribusi label risiko dari dataset pelanggan yang tersimpan di database skripsi."
            />
            <div className="grid gap-3 sm:grid-cols-3">
              {(["rendah", "sedang", "tinggi"] as RisikoLabel[]).map(
                (label) => {
                  const value = dataset?.distribusi_label[label] ?? 0
                  const width =
                    totalDistribusi > 0 ? (value / totalDistribusi) * 100 : 0
                  return (
                    <div key={label} className="border border-border p-3">
                      <div className="flex items-center justify-between gap-2">
                        <RisikoBadge value={label} />
                        <span className="text-lg font-semibold">
                          {formatNumber(value)}
                        </span>
                      </div>
                      <div className="mt-3 h-2 bg-muted">
                        <div
                          className={cn("h-full", risikoConfig[label].bar)}
                          style={{ width: `${width}%` }}
                        />
                      </div>
                    </div>
                  )
                }
              )}
            </div>

            <div className="mt-5 overflow-x-auto border border-border">
              <table className="w-full min-w-[920px] text-left text-sm">
                <thead className="bg-muted text-xs uppercase text-muted-foreground">
                  <tr>
                    <th className="px-3 py-3">Customer</th>
                    <th className="px-3 py-3">Nominal</th>
                    <th className="px-3 py-3">Umur</th>
                    <th className="px-3 py-3">Telat</th>
                    <th className="px-3 py-3">Invoice</th>
                    <th className="px-3 py-3">Status</th>
                    <th className="px-3 py-3">Risiko</th>
                  </tr>
                </thead>
                <tbody>
                  {(dataset?.data ?? []).map((row) => (
                    <tr key={row.customer_code} className="border-t border-border">
                      <td className="px-3 py-3">
                        <div className="font-medium">{row.customer_name}</div>
                        <div className="text-xs text-muted-foreground">
                          {row.customer_code}
                        </div>
                      </td>
                      <td className="px-3 py-3">
                        {formatCurrency(row.nominal_piutang)}
                      </td>
                      <td className="px-3 py-3">
                        {formatNumber(row.umur_piutang_hari)} hari
                      </td>
                      <td className="px-3 py-3">
                        {formatNumber(row.frekuensi_keterlambatan)}
                      </td>
                      <td className="px-3 py-3">
                        {formatNumber(row.jumlah_invoice_belum_lunas)}
                      </td>
                      <td className="px-3 py-3 capitalize">
                        {row.status_customer}
                      </td>
                      <td className="px-3 py-3">
                        <RisikoBadge value={row.risiko_piutang} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>

          <Card>
            <SectionTitle
              icon={Activity}
              title="Aksi Model"
              description="Jalankan proses utama backend dari dashboard."
            />
            <div className="grid gap-2">
              <Button
                variant="outline"
                onClick={() =>
                  void runAction(
                    "generate",
                    api.generateDataset,
                    "Dataset berhasil digenerate."
                  )
                }
                disabled={loading !== null}
              >
                {loading === "generate" ? (
                  <Loader2 className="animate-spin" />
                ) : (
                  <Database />
                )}
                Generate Dataset
              </Button>
              <Button
                variant="outline"
                onClick={() =>
                  void runAction(
                    "export",
                    api.exportExcel,
                    "Dataset berhasil diexport ke Excel."
                  )
                }
                disabled={loading !== null}
              >
                {loading === "export" ? (
                  <Loader2 className="animate-spin" />
                ) : (
                <FileSpreadsheet />
                )}
                Export Excel
              </Button>
              <Button
                variant="outline"
                onClick={() =>
                  void runAction(
                    "export",
                    api.exportRawExcel,
                    "Dataset raw berhasil diexport ke Excel."
                  )
                }
                disabled={loading !== null}
              >
                {loading === "export" ? (
                  <Loader2 className="animate-spin" />
                ) : (
                  <FileSpreadsheet />
                )}
                Export Excel Raw
              </Button>
              <Button
                onClick={() =>
                  void runAction(
                    "train",
                    api.trainModel,
                    "Model Naive Bayes berhasil dilatih.",
                    setEvaluation
                  )
                }
                disabled={loading !== null}
              >
                {loading === "train" ? (
                  <Loader2 className="animate-spin" />
                ) : (
                  <Play />
                )}
                Training Model
              </Button>
            </div>
            <div className="mt-5 border border-border p-3 text-sm">
              <p className="font-semibold">Model terakhir</p>
              <dl className="mt-3 grid gap-2 text-muted-foreground">
                <div className="flex justify-between gap-3">
                  <dt>Status</dt>
                  <dd className="text-foreground">
                    {modelInfo?.model_tersedia ? "Tersedia" : "Belum ada"}
                  </dd>
                </div>
                <div className="flex justify-between gap-3">
                  <dt>Training</dt>
                  <dd className="text-right text-foreground">
                    {formatDateTime(modelInfo?.training_terakhir)}
                  </dd>
                </div>
                <div className="flex justify-between gap-3">
                  <dt>Data latih</dt>
                  <dd className="text-foreground">
                    {formatNumber(modelInfo?.jumlah_dataset_training)}
                  </dd>
                </div>
              </dl>
            </div>
          </Card>
        </section>

        <section className="grid gap-5 xl:grid-cols-2">
          <Card>
            <SectionTitle
              icon={Brain}
              title="Evaluasi Model"
              description="Metrik multiclass untuk label rendah, sedang, dan tinggi."
            />
            {evaluation ? (
              <>
                <div className="grid gap-3 sm:grid-cols-4">
                  <Metric label="Accuracy" value={formatPercent(evaluation.accuracy)} />
                  <Metric
                    label="Precision"
                    value={formatPercent(evaluation.macro_avg.precision)}
                  />
                  <Metric
                    label="Recall"
                    value={formatPercent(evaluation.macro_avg.recall)}
                  />
                  <Metric
                    label="F1-score"
                    value={formatPercent(evaluation.macro_avg.f1_score)}
                  />
                </div>
                <div className="mt-4 overflow-x-auto border border-border">
                  <table className="w-full min-w-[420px] text-center text-sm">
                    <thead className="bg-muted text-xs uppercase text-muted-foreground">
                      <tr>
                        <th className="px-3 py-3 text-left">Aktual \ Prediksi</th>
                        {evaluation.confusion_matrix.labels.map((label) => (
                          <th key={label} className="px-3 py-3 capitalize">
                            {label}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {evaluation.confusion_matrix.matrix.map((row, index) => (
                        <tr key={evaluation.confusion_matrix.labels[index]} className="border-t border-border">
                          <th className="px-3 py-3 text-left capitalize">
                            {evaluation.confusion_matrix.labels[index]}
                          </th>
                          {row.map((value, cellIndex) => (
                            <td key={`${index}-${cellIndex}`} className="px-3 py-3">
                              {formatNumber(value)}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </>
            ) : (
              <div className="border border-dashed border-border p-5 text-sm text-muted-foreground">
                Evaluasi belum tersedia. Jalankan training model terlebih dahulu.
              </div>
            )}
          </Card>

          <Card>
            <SectionTitle
              icon={Search}
              title="Prediksi Risiko"
              description="Gunakan kode pelanggan atau masukkan fitur manual untuk simulasi."
            />
            <form onSubmit={handleCustomerPredict} className="flex gap-2">
              <input
                value={customerCode}
                onChange={(event) => setCustomerCode(event.target.value)}
                className="h-10 min-w-0 flex-1 border border-input bg-background px-3 text-sm outline-none transition focus:border-ring focus:ring-2 focus:ring-ring/20"
                placeholder="Contoh: JKTB2B0080"
              />
              <Button disabled={loading !== null} type="submit">
                {loading === "predictCustomer" ? (
                  <Loader2 className="animate-spin" />
                ) : (
                  <Search />
                )}
                Prediksi
              </Button>
            </form>

            <form onSubmit={handleManualPredict} className="mt-5 grid gap-3 sm:grid-cols-2">
              <TextInput
                label="Umur Piutang"
                type="number"
                value={manualForm.umur_piutang_hari}
                onChange={(value) =>
                  setManualForm((current) => ({
                    ...current,
                    umur_piutang_hari: value,
                  }))
                }
              />
              <TextInput
                label="Nominal Piutang"
                type="number"
                value={manualForm.nominal_piutang}
                onChange={(value) =>
                  setManualForm((current) => ({
                    ...current,
                    nominal_piutang: value,
                  }))
                }
              />
              <TextInput
                label="Frekuensi Telat"
                type="number"
                value={manualForm.frekuensi_keterlambatan}
                onChange={(value) =>
                  setManualForm((current) => ({
                    ...current,
                    frekuensi_keterlambatan: value,
                  }))
                }
              />
              <TextInput
                label="Invoice Belum Lunas"
                type="number"
                value={manualForm.jumlah_invoice_belum_lunas}
                onChange={(value) =>
                  setManualForm((current) => ({
                    ...current,
                    jumlah_invoice_belum_lunas: value,
                  }))
                }
              />
              <TextInput
                label="Umur Customer"
                type="number"
                value={manualForm.umur_customer_hari}
                onChange={(value) =>
                  setManualForm((current) => ({
                    ...current,
                    umur_customer_hari: value,
                  }))
                }
              />
              <div className="flex items-end">
                <Button className="w-full" disabled={loading !== null} type="submit">
                  {loading === "predictManual" ? (
                    <Loader2 className="animate-spin" />
                  ) : (
                    <Sparkles />
                  )}
                  Simulasi Manual
                </Button>
              </div>
            </form>

            {prediction ? (
              <div className="mt-5 border border-border p-4">
                <div className="flex items-center justify-between gap-3">
                  <p className="font-semibold">Hasil Prediksi</p>
                  <RisikoBadge value={prediction.risiko_piutang} />
                </div>
                <div className="mt-4 grid gap-2">
                  {(["rendah", "sedang", "tinggi"] as RisikoLabel[]).map(
                    (label) => (
                      <div key={label}>
                        <div className="mb-1 flex justify-between text-xs text-muted-foreground">
                          <span className="capitalize">{label}</span>
                          <span>{formatPercent(prediction.probabilitas[label])}</span>
                        </div>
                        <div className="h-2 bg-muted">
                          <div
                            className={cn("h-full", risikoConfig[label].bar)}
                            style={{
                              width: `${(prediction.probabilitas[label] ?? 0) * 100}%`,
                            }}
                          />
                        </div>
                      </div>
                    )
                  )}
                </div>
              </div>
            ) : null}
          </Card>
        </section>

        <Card>
          <SectionTitle
            icon={FileSpreadsheet}
            title="Referensi Fitur Dan Label"
            description="Aturan ini digunakan untuk membentuk dataset dan label target risiko_piutang."
          />
          <div className="grid gap-5 lg:grid-cols-[1fr_0.8fr]">
            <div className="overflow-x-auto border border-border">
              <table className="w-full min-w-[620px] text-left text-sm">
                <thead className="bg-muted text-xs uppercase text-muted-foreground">
                  <tr>
                    <th className="px-3 py-3">Fitur</th>
                    <th className="px-3 py-3">Kategori</th>
                    <th className="px-3 py-3">Aturan</th>
                    <th className="px-3 py-3">Skor</th>
                  </tr>
                </thead>
                <tbody>
                  {(referensi?.aturan_fitur ?? []).map((row, index) => (
                    <tr key={`${row.fitur}-${row.kategori}-${index}`} className="border-t border-border">
                      <td className="px-3 py-3 font-medium">{row.fitur}</td>
                      <td className="px-3 py-3">{row.kategori}</td>
                      <td className="px-3 py-3 text-muted-foreground">
                        {row.aturan}
                      </td>
                      <td className="px-3 py-3">{row.skor}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="grid content-start gap-3">
              {(referensi?.aturan_label ?? []).map((row) => (
                <div key={row.risiko_piutang} className="border border-border p-3">
                  <RisikoBadge value={row.risiko_piutang} />
                  <p className="mt-2 text-sm text-muted-foreground">
                    {row.aturan}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </Card>
      </div>
    </main>
  )
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="border border-border p-3">
      <p className="text-xs font-semibold uppercase text-muted-foreground">
        {label}
      </p>
      <p className="mt-2 text-lg font-semibold">{value}</p>
    </div>
  )
}
