LABEL_ORDER = ["rendah", "sedang", "tinggi"]

FEATURE_COLUMNS = [
    "kategori_umur_piutang",
    "kategori_nominal_piutang",
    "kategori_frekuensi_keterlambatan",
    "kategori_invoice_belum_lunas",
    "status_customer",
]

FEATURE_CATEGORIES = {
    "kategori_umur_piutang": ["tidak_diketahui", "rendah", "sedang", "tinggi"],
    "kategori_nominal_piutang": ["tidak_diketahui", "kecil", "sedang", "besar"],
    "kategori_frekuensi_keterlambatan": [
        "tidak_diketahui",
        "jarang",
        "kadang",
        "sering",
    ],
    "kategori_invoice_belum_lunas": [
        "tidak_diketahui",
        "sedikit",
        "sedang",
        "banyak",
    ],
    "status_customer": ["tidak_diketahui", "baru", "lama"],
}

ATURAN_FITUR = [
    {
        "fitur": "umur_piutang_hari",
        "kategori": "rendah",
        "aturan": "0 sampai 30 hari",
        "skor": 1,
    },
    {
        "fitur": "umur_piutang_hari",
        "kategori": "sedang",
        "aturan": "31 sampai 60 hari",
        "skor": 2,
    },
    {
        "fitur": "umur_piutang_hari",
        "kategori": "tinggi",
        "aturan": "lebih dari 60 hari",
        "skor": 3,
    },
    {
        "fitur": "nominal_piutang",
        "kategori": "kecil",
        "aturan": "kurang dari atau sama dengan Rp1.000.000",
        "skor": 1,
    },
    {
        "fitur": "nominal_piutang",
        "kategori": "sedang",
        "aturan": "Rp1.000.001 sampai Rp8.000.000",
        "skor": 2,
    },
    {
        "fitur": "nominal_piutang",
        "kategori": "besar",
        "aturan": "lebih dari Rp8.000.000",
        "skor": 3,
    },
    {
        "fitur": "frekuensi_keterlambatan",
        "kategori": "jarang",
        "aturan": "0 sampai 4 kali",
        "skor": 1,
    },
    {
        "fitur": "frekuensi_keterlambatan",
        "kategori": "kadang",
        "aturan": "5 sampai 27 kali",
        "skor": 2,
    },
    {
        "fitur": "frekuensi_keterlambatan",
        "kategori": "sering",
        "aturan": "lebih dari 27 kali",
        "skor": 3,
    },
    {
        "fitur": "jumlah_invoice_belum_lunas",
        "kategori": "sedikit",
        "aturan": "0 sampai 1 invoice",
        "skor": 1,
    },
    {
        "fitur": "jumlah_invoice_belum_lunas",
        "kategori": "sedang",
        "aturan": "2 sampai 4 invoice",
        "skor": 2,
    },
    {
        "fitur": "jumlah_invoice_belum_lunas",
        "kategori": "banyak",
        "aturan": "lebih dari 4 invoice",
        "skor": 3,
    },
    {
        "fitur": "status_customer",
        "kategori": "baru",
        "aturan": "umur customer kurang dari atau sama dengan 365 hari",
        "skor": 1,
    },
    {
        "fitur": "status_customer",
        "kategori": "lama",
        "aturan": "umur customer lebih dari 365 hari",
        "skor": 0,
    },
]

ATURAN_LABEL = [
    {"risiko_piutang": "rendah", "aturan": "skor risiko kurang dari atau sama dengan 6"},
    {"risiko_piutang": "sedang", "aturan": "skor risiko 7 sampai 9"},
    {"risiko_piutang": "tinggi", "aturan": "skor risiko lebih dari atau sama dengan 10"},
]
