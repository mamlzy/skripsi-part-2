# Laporan Model dan Program

**Model Klasifikasi Piutang Pelanggan dengan Metode Naive Bayes pada PT Sarana Mulya Logistik**

Nama Mahasiswa: Imam Alfarizi Syahputra  
NPM: 202243500232  
Program Studi: Teknik Informatika  
Universitas: Universitas Indraprasta  
Tahun: 2026

## 2. Pendahuluan

PT Sarana Mulya Logistik memiliki aktivitas bisnis yang melibatkan transaksi pelanggan dan proses pembayaran piutang. Dalam praktiknya, terdapat pelanggan yang membayar tepat waktu, terlambat, atau masih memiliki invoice yang belum lunas. Kondisi tersebut dapat memengaruhi arus kas dan proses penagihan perusahaan.

Klasifikasi risiko piutang pelanggan diperlukan agar perusahaan dapat memahami tingkat risiko pembayaran secara lebih terarah. Dengan pengelompokan risiko, pelanggan dapat diprioritaskan untuk pemantauan, analisis, atau tindak lanjut penagihan sesuai tingkat risikonya.

Tujuan model ini adalah membantu mengklasifikasikan pelanggan ke dalam risiko rendah, sedang, atau tinggi berdasarkan data piutang dan riwayat pembayaran yang tersedia.

## 3. Gambaran Umum Sistem

Sistem yang akan dibuat digunakan untuk membantu proses klasifikasi risiko piutang pelanggan pada PT Sarana Mulya Logistik. Sistem membaca dataset pelanggan, membentuk fitur yang relevan, melatih model Naive Bayes, dan menampilkan hasil klasifikasi risiko.

Program dibuat dalam bentuk satu halaman utama. Halaman tersebut menampilkan informasi penting terkait dataset, model, evaluasi, dan hasil klasifikasi atau prediksi pelanggan.

Output klasifikasi terdiri dari tiga label, yaitu Risiko Rendah, Risiko Sedang, dan Risiko Tinggi. Manfaat sistem bagi perusahaan adalah membantu analisis risiko pembayaran pelanggan, mendukung prioritas penagihan, dan memberi gambaran awal terhadap pelanggan yang perlu diperhatikan lebih lanjut.

## 4. Penjelasan Model Naive Bayes

Naive Bayes adalah metode klasifikasi berbasis probabilitas. Model ini menghitung kemungkinan suatu data pelanggan termasuk ke dalam kelas risiko tertentu berdasarkan pola data yang telah dipelajari sebelumnya.

Metode ini cocok digunakan untuk klasifikasi risiko piutang pelanggan karena fitur yang digunakan dapat dikelompokkan ke dalam kategori, seperti umur piutang rendah/sedang/tinggi, nominal piutang kecil/sedang/besar, dan frekuensi keterlambatan jarang/kadang/sering. Dengan pendekatan probabilitas, model dapat memberikan hasil klasifikasi yang sederhana, cepat, dan mudah dijelaskan.

Dalam laporan ini, Naive Bayes digunakan untuk mempelajari hubungan antara karakteristik piutang pelanggan dan label risiko piutang.

## 5. Fitur Model / Atribut yang Digunakan

Kolom identitas seperti kode pelanggan dan nama pelanggan digunakan sebagai informasi pendukung. Fitur utama model berasal dari kondisi piutang, riwayat keterlambatan, jumlah invoice yang belum lunas, dan status pelanggan.

### 5.1 Fitur Numerik

| Fitur Numerik | Fungsi terhadap Klasifikasi Risiko |
| --- | --- |
| umur_piutang_hari | Menunjukkan umur invoice outstanding paling lama dalam satuan hari. Semakin lama umur piutang, semakin besar indikasi risiko pembayaran. |
| nominal_piutang | Menunjukkan total sisa piutang pelanggan dalam rupiah. Nilai piutang yang besar membutuhkan perhatian risiko lebih tinggi. |
| frekuensi_keterlambatan | Menunjukkan jumlah riwayat pembayaran yang melewati jatuh tempo. Riwayat keterlambatan menjadi indikator perilaku pembayaran pelanggan. |
| jumlah_invoice_belum_lunas | Menunjukkan banyaknya invoice pelanggan yang masih belum lunas. Semakin banyak invoice outstanding, semakin besar potensi risiko penagihan. |
| umur_customer_hari | Menunjukkan lamanya pelanggan tercatat sejak awal periode atau tanggal pembuatan data pelanggan. Nilai ini digunakan untuk membentuk status customer baru atau lama. |

### 5.2 Fitur Kategorikal

| Fitur Kategorikal | Fungsi terhadap Klasifikasi Risiko |
| --- | --- |
| kategori_umur_piutang | Hasil pengelompokan umur piutang menjadi rendah, sedang, atau tinggi. |
| kategori_nominal_piutang | Hasil pengelompokan nominal piutang menjadi kecil, sedang, atau besar. |
| kategori_frekuensi_keterlambatan | Hasil pengelompokan frekuensi keterlambatan menjadi jarang, kadang, atau sering. |
| kategori_invoice_belum_lunas | Hasil pengelompokan jumlah invoice belum lunas menjadi sedikit, sedang, atau banyak. |
| status_customer | Status pelanggan berdasarkan umur customer, yaitu baru atau lama. |

## 6. Aturan Label / Target Klasifikasi

Target klasifikasi adalah tingkat risiko piutang pelanggan yang disimpan dalam kolom `risiko_piutang`. Label terdiri dari Risiko Rendah, Risiko Sedang, dan Risiko Tinggi.

Label dibentuk dari skor risiko. Setiap fitur numerik dikelompokkan terlebih dahulu menjadi kategori, kemudian masing-masing kategori diberi skor. Skor akhir digunakan untuk menentukan kelas risiko.

### 6.1 Aturan Kategorisasi Fitur

| Fitur | Kategori | Aturan | Skor |
| --- | --- | --- | --- |
| umur_piutang_hari | rendah | 0 sampai 30 hari | 1 |
| umur_piutang_hari | sedang | 31 sampai 60 hari | 2 |
| umur_piutang_hari | tinggi | lebih dari 60 hari | 3 |
| nominal_piutang | kecil | kurang dari atau sama dengan Rp1.000.000 | 1 |
| nominal_piutang | sedang | Rp1.000.001 sampai Rp8.000.000 | 2 |
| nominal_piutang | besar | lebih dari Rp8.000.000 | 3 |
| frekuensi_keterlambatan | jarang | 0 sampai 4 kali | 1 |
| frekuensi_keterlambatan | kadang | 5 sampai 27 kali | 2 |
| frekuensi_keterlambatan | sering | lebih dari 27 kali | 3 |
| jumlah_invoice_belum_lunas | sedikit | 0 sampai 1 invoice | 1 |
| jumlah_invoice_belum_lunas | sedang | 2 sampai 4 invoice | 2 |
| jumlah_invoice_belum_lunas | banyak | lebih dari 4 invoice | 3 |
| status_customer | baru | umur customer kurang dari atau sama dengan 365 hari | 1 |
| status_customer | lama | umur customer lebih dari 365 hari | 0 |

### 6.2 Aturan Label Akhir

| Label Risiko | Aturan |
| --- | --- |
| Rendah | skor risiko kurang dari atau sama dengan 6 |
| Sedang | skor risiko 7 sampai 9 |
| Tinggi | skor risiko lebih dari atau sama dengan 10 |

## 7. Tahapan Pengolahan Data

1. Pengumpulan data dilakukan dari data piutang pelanggan perusahaan.
2. Seleksi atribut dilakukan dengan memilih atribut yang relevan terhadap risiko piutang.
3. Pembersihan data dilakukan agar nilai yang digunakan layak untuk proses analisis.
4. Transformasi data dilakukan dengan mengubah fitur numerik menjadi kategori risiko.
5. Pembentukan label dilakukan menggunakan skor risiko berdasarkan aturan yang telah ditentukan.
6. Pembagian data dilakukan menjadi data latih dan data uji. Berdasarkan evaluasi yang tersedia, terdapat 145 data latih dan 37 data uji.
7. Pelatihan model dilakukan menggunakan metode Naive Bayes pada data latih.
8. Evaluasi model dilakukan menggunakan data uji untuk melihat kemampuan model mengklasifikasikan risiko rendah, sedang, dan tinggi.

## 8. Tampilan Program

<div style="border: 2px solid #555; height: 220px; display: flex; align-items: center; justify-content: center; text-align: center;">
<strong>Screenshot Tampilan Utama Program</strong>
</div>

Tampilan ini menunjukkan halaman utama sistem klasifikasi risiko piutang pelanggan. Karena program hanya terdiri dari satu halaman utama, laporan ini hanya menyediakan satu placeholder screenshot.

## 9. Dataset Mentah

Dataset mentah diambil dari file `skripsi/backend/storage/dataset/dataset_risiko_piutang_raw.xlsx`, khususnya sheet `dataset_raw`. Dataset ini berisi fitur numerik asli sebelum proses kategorisasi. Tabel berikut menampilkan 12 baris pertama dari total 182 baris data. Data lengkap tersedia pada file Excel tersebut.

**Tabel Dataset Mentah**

| Kode Pelanggan | Nama Pelanggan | Tipe | TOP (Hari) | Umur Piutang (Hari) | Nominal Piutang | Frekuensi Keterlambatan | Invoice Belum Lunas | Umur Customer (Hari) | Skor Risiko | Risiko Piutang | Sumber Database |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JKTB2B0080 | ABADI RIZKI MEDIKA | B2B | 30 | 175 | Rp14.509.872 | 0 | 1 | 256 | 9 | sedang | lms_prod_sml_03_04_26 |
| JKTC00002 | ABHIMATA MANUNGGAL | B2B | 30 | 80 | Rp98.708.338 | 289 | 8 | 2288 | 12 | tinggi | lms_prod_sml_03_04_26 |
| JKTB2B0136 | ABHINAYA KARYA PERKASA | B2B | 30 | 39 | Rp24.587.300 | 0 | 2 | 70 | 9 | sedang | lms_prod_sml_03_04_26 |
| JKTB2B0023 | AESCOMED HEALTHCARE INDONESIA | B2B | 30 | 60 | Rp1.452.836 | 10 | 2 | 443 | 8 | sedang | lms_prod_sml_03_04_26 |
| JKTB2B0103 | AESCOMED HEALTHCARE INDONESIA (EXIM) | B2B | 30 | 94 | Rp10.590.766 | 5 | 5 | 169 | 12 | tinggi | lms_prod_sml_03_04_26 |
| JKTC0605 | AGARINDO BIOLOGICAL COMPANY | B2B | 30 | 569 | Rp35.235 | 0 | 1 | 623 | 6 | rendah | lms_prod_sml_03_04_26 |
| JKTC00014 | AMPM HEALTHCARE INDONESIA | B2B | 30 | 58 | Rp1.379.550 | 57 | 2 | 2306 | 9 | sedang | lms_prod_sml_03_04_26 |
| JKTB2B0091 | ANEKA MEDIKA INDONESIA (EXIM) | B2B | 30 | 100 | Rp46.840.150 | 4 | 6 | 1039 | 10 | tinggi | lms_prod_sml_03_04_26 |
| SUBC00025 | ANEKA TIRTA KENCANA | B2B | 30 | 94 | Rp848.343 | 99 | 4 | 2306 | 9 | sedang | lms_prod_sml_03_04_26 |
| JKTB2B0063 | ANTARMITRA SEMBADA  | B2B | 30 | 80 | Rp10.044 | 7 | 1 | 324 | 8 | sedang | lms_prod_sml_03_04_26 |
| SUBB2B0036 | ANUGERAH CITRALOKA | B2B | 30 | 81 | Rp255.000 | 0 | 1 | 105 | 7 | sedang | lms_prod_sml_03_04_26 |
| JKTB2B0060 | ANUGERAH SAHABAT ASA | B2B | 30 | 294 | Rp141.540 | 0 | 1 | 343 | 7 | sedang | lms_prod_sml_03_04_26 |

## 10. Dataset Siap Digunakan

Dataset siap digunakan diambil dari file `skripsi/backend/storage/dataset/dataset_risiko_piutang.xlsx`, khususnya sheet `dataset`. Dataset ini sudah berisi fitur kategorikal yang digunakan oleh model dan kolom label `risiko_piutang`. Tabel berikut menampilkan seluruh 182 baris data yang tersedia pada file Excel tersebut.

**Tabel Dataset Siap Digunakan**

| Kode Pelanggan | Nama Pelanggan | Tipe | Kategori Umur Piutang | Kategori Nominal Piutang | Kategori Keterlambatan | Kategori Invoice | Status Customer | Skor Risiko | Risiko Piutang |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JKTB2B0080 | ABADI RIZKI MEDIKA | B2B | tinggi | besar | jarang | sedikit | baru | 9 | sedang |
| JKTC00002 | ABHIMATA MANUNGGAL | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| JKTB2B0136 | ABHINAYA KARYA PERKASA | B2B | sedang | besar | jarang | sedang | baru | 9 | sedang |
| JKTB2B0023 | AESCOMED HEALTHCARE INDONESIA | B2B | sedang | sedang | kadang | sedang | lama | 8 | sedang |
| JKTB2B0103 | AESCOMED HEALTHCARE INDONESIA (EXIM) | B2B | tinggi | besar | kadang | banyak | baru | 12 | tinggi |
| JKTC0605 | AGARINDO BIOLOGICAL COMPANY | B2B | tinggi | kecil | jarang | sedikit | lama | 6 | rendah |
| JKTC00014 | AMPM HEALTHCARE INDONESIA | B2B | sedang | sedang | sering | sedang | lama | 9 | sedang |
| JKTB2B0091 | ANEKA MEDIKA INDONESIA (EXIM) | B2B | tinggi | besar | jarang | banyak | lama | 10 | tinggi |
| SUBC00025 | ANEKA TIRTA KENCANA | B2B | tinggi | kecil | sering | sedang | lama | 9 | sedang |
| JKTB2B0063 | ANTARMITRA SEMBADA  | B2B | tinggi | kecil | kadang | sedikit | baru | 8 | sedang |
| SUBB2B0036 | ANUGERAH CITRALOKA | B2B | tinggi | kecil | jarang | sedikit | baru | 7 | sedang |
| JKTB2B0060 | ANUGERAH SAHABAT ASA | B2B | tinggi | kecil | jarang | sedikit | baru | 7 | sedang |
| SUBC00026 | ANUGERAH SANTOSA ABADI CAB SURABAYA | B2B | rendah | kecil | kadang | sedikit | lama | 5 | rendah |
| JKTC0409 | ANUGERAH TETAP MAKMUR | B2B | tinggi | kecil | sering | sedang | lama | 9 | sedang |
| JKTC0442 | ANUGRAH BIO NUTRISI INDONESIA | B2B | tinggi | kecil | sering | sedang | lama | 9 | sedang |
| JKTC0444 | ANUGRAH INOVASI MAKMUR INDONESIA | B2B | sedang | besar | sering | sedang | lama | 10 | tinggi |
| SUBB2B0029 | ARETE MEDIKA UTAMA | B2B | tinggi | kecil | jarang | sedang | baru | 8 | sedang |
| JKTC00024 | ARINDA PHARMA | B2B | tinggi | sedang | sering | sedang | lama | 10 | tinggi |
| SUBC0066 | ASIAGLOW BERLIAN | B2B | tinggi | sedang | sering | sedang | lama | 10 | tinggi |
| SUBC0113 | BADAN INTIDAYA DINAMIKA SEJATI | B2B | tinggi | kecil | jarang | sedikit | lama | 6 | rendah |
| SUBB2B0011 | BADAN MURNI SOLUSINDO NUSANTARA | B2B | tinggi | kecil | kadang | sedikit | lama | 7 | sedang |
| JKTC00032 | BAHANA ANDALAN PASTI | B2B | tinggi | kecil | kadang | sedikit | lama | 7 | sedang |
| SUBB2B0020 | BARIK MAKMUR JAYA | B2B | rendah | sedang | jarang | sedang | baru | 7 | sedang |
| JKTC0597 | BETASAINS OPTIMA SINERGI  | B2B | tinggi | sedang | kadang | sedikit | lama | 8 | sedang |
| JKTC00051 | BINTANG SARANA MEDIKA | B2B | tinggi | sedang | kadang | sedikit | lama | 8 | sedang |
| SUBB2B0024 | BIO ANALITIKAL | B2B | tinggi | sedang | jarang | sedikit | baru | 8 | sedang |
| JKTC0585 | BIOGENOME TOTAL SOLUSI  | B2B | sedang | kecil | jarang | sedang | lama | 6 | rendah |
| JKTB2B0008 | BIOGENOME TOTAL SOLUSI (EXIM) | B2B | sedang | besar | jarang | banyak | lama | 9 | sedang |
| JKTB2B0020 | BIOMED GLOBAL SINERGI  | B2B | tinggi | kecil | sering | banyak | lama | 10 | tinggi |
| JKTB2B0094 | BIOMED GLOBAL SINERGI (EXIM) | B2B | tinggi | besar | jarang | sedang | lama | 9 | sedang |
| JKTDIS0010 | BOLD TECHNOLOGIES LEADING INDONESIA  | DISTRI | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| SUBB2B0033 | BORNEO ETAM MANDIRI | B2B | tinggi | besar | jarang | sedikit | baru | 9 | sedang |
| JKTB2B0038 | CAHYA INTAN MEDIKA  | B2B | rendah | sedang | jarang | sedikit | lama | 5 | rendah |
| JKTC0590 | CBC PRIMA  | B2B | tinggi | sedang | kadang | sedang | lama | 9 | sedang |
| JKTC00069 | COBRA DENTAL INDONESIA | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| SUBC0090 | COBRA DENTAL INDONESIA CAB. SUB | B2B | tinggi | sedang | kadang | sedang | lama | 9 | sedang |
| JKTC00072 | CURIE MEDIKA INDONESIA | B2B | tinggi | kecil | sering | sedang | lama | 9 | sedang |
| JKTB2B0132 | DAIHAN LABTECH  | B2B | sedang | kecil | jarang | sedang | baru | 7 | sedang |
| SUBB2B0032 | DARMA LABORA INDONESIA | B2B | tinggi | sedang | jarang | sedang | baru | 9 | sedang |
| JKTC0453 | DAYA MUDA AGUNG | B2B | tinggi | sedang | sering | banyak | lama | 11 | tinggi |
| JKTC0479 | DEMAZ NOER ABADI | B2B | tinggi | besar | sering | sedang | lama | 11 | tinggi |
| JKTC0604 | DENTALITIES GROUP ASIA | B2B | tinggi | kecil | kadang | sedikit | lama | 7 | sedang |
| JKTB2B0113 | DEXA ARFINDO PRATAMA  | B2B | sedang | sedang | jarang | sedang | baru | 8 | sedang |
| JKTB2B0018 | DHH | B2B | tinggi | kecil | jarang | sedikit | lama | 6 | rendah |
| JKTC00077 | DIAGNOSTIK INDONESIA | B2B | tinggi | sedang | kadang | sedikit | lama | 8 | sedang |
| JKTC00080 | DIASTIKA BIOTEKINDO | B2B | sedang | sedang | kadang | sedang | lama | 8 | sedang |
| SUBB2B0027 | DIMENSI CITRA SEMESTA  | B2B | tinggi | sedang | kadang | sedang | baru | 10 | tinggi |
| JKTB2B0109 | DIPA PUSPA LABSAINS (EXIM) | B2B | tinggi | besar | jarang | sedikit | baru | 9 | sedang |
| SUBB2B0023 | DUA PILAR ABADI | B2B | tinggi | kecil | jarang | sedang | baru | 8 | sedang |
| JKTC00096 | ENSEVAL PUTERA MEGATRADING TBK | B2B | sedang | sedang | sering | sedang | lama | 9 | sedang |
| JKTC00099 | ERA MITRA PERDANA | B2B | tinggi | sedang | kadang | sedang | lama | 9 | sedang |
| JKTC0611 | EUREKA SUKSES ABADI  | B2B | tinggi | besar | kadang | sedang | lama | 10 | tinggi |
| JKTB2B0083 | FAIRMED IMAGING NUSAJAYA | B2B | tinggi | kecil | jarang | sedang | baru | 8 | sedang |
| JKTC00103 | FAST BEAUTY INDONESIA | B2B | tinggi | kecil | kadang | sedikit | lama | 7 | sedang |
| JKTB2B0076 | FOKUS DIAGNOSTIC INDONESIA  | B2B | tinggi | sedang | kadang | banyak | baru | 11 | tinggi |
| JKTC00106 | FOKUS KELUARGA SEHAT | B2B | tinggi | kecil | kadang | sedikit | lama | 7 | sedang |
| JKTB2B0129 | FONDASI TIANG NUSANTARA INDONESIA  | B2B | tinggi | kecil | jarang | sedikit | baru | 7 | sedang |
| JKTC00108 | FRESENIUS KABI INDONESIA | B2B | tinggi | sedang | sering | banyak | lama | 11 | tinggi |
| SUBC0032 | FRISMED HOSLAB INDONESIA | B2B | tinggi | kecil | kadang | sedikit | lama | 7 | sedang |
| SUBC0070 | GENLIGHT TUJUH SINERGI | B2B | tinggi | kecil | kadang | sedang | lama | 8 | sedang |
| JKTB2B0079 | GLOBAL MEDIK PERSADA  | B2B | tinggi | besar | kadang | banyak | baru | 12 | tinggi |
| JKTC00119 | GLOBAL PROMEDIKA SERVICES | B2B | rendah | sedang | sering | sedang | lama | 8 | sedang |
| JKTB2B0144 | GPS LANDS INDOSOLUTIONS  | B2B | rendah | kecil | jarang | sedikit | baru | 5 | rendah |
| JKTC00122 | GRAHA MEGATAMA INDONESIA | B2B | tinggi | kecil | kadang | sedikit | lama | 7 | sedang |
| SUBC0086 | HANSA PRATAMA ENGINEERING | B2B | tinggi | kecil | jarang | sedikit | lama | 6 | rendah |
| JKTC0384 | HIDAYAH TRIPUTRA MEDIKA | B2B | tinggi | kecil | sering | sedikit | lama | 8 | sedang |
| JKTB2B0125 | I TECH LAFACOS  | B2B | tinggi | kecil | jarang | sedikit | baru | 7 | sedang |
| SUBC00008 | IMAR KARYA TAMA | B2B | tinggi | kecil | sering | banyak | lama | 10 | tinggi |
| JKTC00135 | INDEC DIAGNOSTICS | B2B | tinggi | besar | kadang | sedang | lama | 10 | tinggi |
| JKTC00137 | INDOFARMA GLOBAL MEDIKA | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| JKTC0480 | INDOMED KAHANASTI INDONESIA | B2B | tinggi | kecil | jarang | sedang | lama | 7 | sedang |
| JKTB2B0011 | INDOPAL HARVEST BLISS | B2B | tinggi | kecil | jarang | sedikit | lama | 6 | rendah |
| JKTB2B0130 | INDOPAL HARVEST BLISS (EXIM) | B2B | tinggi | besar | jarang | banyak | baru | 11 | tinggi |
| JKTC0541 | INDOTECH SAINS INTI | B2B | tinggi | kecil | kadang | sedikit | lama | 7 | sedang |
| JKTC0494 | INDOTECH SCIENTIFIC | B2B | tinggi | kecil | sering | sedang | lama | 9 | sedang |
| SUBC0103 | INNOTEK MEGAH INDONESIA | B2B | tinggi | sedang | kadang | banyak | lama | 10 | tinggi |
| JKTB2B0057 | INTISUMBER HASIL SEMPURNA GLOBAL  | B2B | tinggi | besar | jarang | sedang | baru | 10 | tinggi |
| JKTC00153 | ITS SCIENCE INDONESIA | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| JKTC0439 | KARUNIAJAYA ANDALAN PRIMA | B2B | sedang | sedang | sering | banyak | lama | 10 | tinggi |
| JKTC0503 | KARYA PRATAMA | B2B | tinggi | kecil | kadang | sedikit | lama | 7 | sedang |
| SUBC00013 | KASA HUSADA WIRA JATIM | B2B | tinggi | besar | kadang | banyak | lama | 11 | tinggi |
| JKTB2B0037 | KHALISA PRATAMA SUKSES  | B2B | tinggi | besar | kadang | banyak | lama | 11 | tinggi |
| JKTB2B0049 | KHAZANAH MEDIKA PRATAMA INDONESIA (EXIM) | B2B | tinggi | kecil | kadang | sedikit | lama | 7 | sedang |
| JKTC00171 | KRISTALAB SURYA MEDIKA | B2B | tinggi | sedang | sering | banyak | lama | 11 | tinggi |
| JKTB2B0088 | LABORATORIUM SOLUSI INDONESIA (EXIM) | B2B | sedang | sedang | kadang | sedikit | lama | 7 | sedang |
| SUBB2B0005 | LABORATORIUM SOLUSI INDONESIA CAB. SURABAYA | B2B | tinggi | kecil | kadang | sedikit | lama | 7 | sedang |
| JKTB2B0134 | LAMI INDO MEDIKA (EXIM) | B2B | rendah | besar | jarang | sedang | baru | 8 | sedang |
| JKTB2B0137 | LEITER INDONESIA  | B2B | sedang | sedang | jarang | sedang | baru | 8 | sedang |
| JKTB2B0053 | LEY HARMONY KHATULISTIWA  | B2B | tinggi | besar | kadang | sedang | baru | 11 | tinggi |
| JKTB2B0092 | LIMAFITA USADA PASIFINDO | B2B | tinggi | sedang | kadang | banyak | baru | 11 | tinggi |
| SUBB2B0028 | LINTAS CITRA ANDALAS | B2B | tinggi | kecil | jarang | sedikit | baru | 7 | sedang |
| SUBC0034 | LOREN IRMA PRATMA | B2B | sedang | sedang | kadang | sedang | lama | 8 | sedang |
| JKTC0591 | MACBRAMINDO HARUM ABADI | B2B | tinggi | kecil | kadang | sedikit | lama | 7 | sedang |
| JKTB2B0072 | MAJA BINTANG INDONESIA TBK  | B2B | sedang | besar | kadang | sedang | baru | 10 | tinggi |
| JKTC00187 | MANOV TRENGGANA SUMAPALA | B2B | tinggi | kecil | sering | banyak | lama | 10 | tinggi |
| JKTC00347 | MEDQUEST JAYA GLOBAL | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| SUBC00007 | MEDQUEST JAYA GLOBAL CAB SURABAYA | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| JKTC0593 | MEGA INTER DISTRINDO  | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| JKTC0426 | MEKAR ABADI PRATAMA | B2B | tinggi | sedang | sering | sedang | lama | 10 | tinggi |
| JKTB2B0059 | MEPROFARM | B2B | tinggi | kecil | kadang | sedang | baru | 9 | sedang |
| JKTC00203 | MERAPI UTAMA PHARMA | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| SUBC00011 | MERAPI UTAMA PHARMA CAB SIDOARJO | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| JKTC00204 | MILLENIUM PHARMACON INTERNATIONAL TBK | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| SUBC0117 | MILLENIUM PHARMACON INTERNATIONAL TBK CAB. SIDOARJO | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| SUBB2B0010 | MIMAR CITRA ABADI | B2B | tinggi | sedang | kadang | sedang | lama | 9 | sedang |
| JKTB2B0115 | MITRA DIBA MANDIRI  | B2B | sedang | kecil | jarang | sedikit | baru | 6 | rendah |
| JKTC0428 | MITRA MANDIRI TEHNIK | B2B | tinggi | kecil | jarang | sedikit | lama | 6 | rendah |
| JKTC00213 | MITRASAMAYA SEJATI | B2B | tinggi | sedang | sering | sedang | lama | 10 | tinggi |
| JKTC00215 | MRK DIAGNOSTICS | B2B | tinggi | kecil | sering | sedang | lama | 9 | sedang |
| SUBC0120 | MULIA MESIN INDUSTRI | B2B | tinggi | kecil | kadang | sedang | lama | 8 | sedang |
| JKTC0517 | MULIA MESIN INDUSTRI | B2B | tinggi | kecil | sering | sedang | lama | 9 | sedang |
| SUBB2B0001 | MULTI AXIS SURGICAL | B2B | sedang | kecil | jarang | sedikit | lama | 5 | rendah |
| JKTC0412 | MULTIKARYA ASIA PASIFIK RAYA | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| JKTC0586 | MULTIKARYA ASIA PASIFIK RAYA (EXIM) | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| SUBC0104 | MULTISERA MIRATAMA SURABAYA | B2B | rendah | sedang | jarang | sedikit | lama | 5 | rendah |
| JKTC00219 | MURTI INDAH SENTOSA | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| JKTC0589 | NAFAST (NADYA FRANSISKA) | B2B | tinggi | kecil | kadang | sedikit | lama | 7 | sedang |
| JKTC0536 | NAWASENA GALA MEDIKA | B2B | tinggi | kecil | kadang | sedikit | lama | 7 | sedang |
| JKTC0603 | OPTO PERSADA NUSANTARA  | B2B | tinggi | kecil | jarang | sedikit | lama | 6 | rendah |
| SUBC0125 | PANCARAYA KRISNAMANDIRI | B2B | rendah | kecil | kadang | sedikit | lama | 5 | rendah |
| JKTC00237 | PASIFIK INTERNUSA | B2B | tinggi | sedang | sering | sedang | lama | 10 | tinggi |
| JKTC00241 | PELITA SANTOSO JAYA | B2B | sedang | sedang | sering | sedang | lama | 9 | sedang |
| SUBC0049 | PERMATA GEMILANG SURYATAMA | B2B | tinggi | kecil | kadang | sedikit | lama | 7 | sedang |
| JKTC0522 | PERORANGAN ( SYIFA REVITA ARFA ) | B2B | tinggi | kecil | jarang | sedikit | lama | 6 | rendah |
| PROC0030 | PERORANGAN (FARIZ NURKARTIKAHADI) | B2B | tinggi | kecil | jarang | sedang | lama | 7 | sedang |
| PROC0022 | PERORANGAN (HERIANSYAH (MKT)) | B2B | tinggi | kecil | jarang | sedang | lama | 7 | sedang |
| PROC0014 | PERORANGAN (NURRAHMAD DIYANTAMA) | B2B | tinggi | sedang | jarang | sedikit | lama | 7 | sedang |
| JKTC0433 | PRADINA NARATAMA SOLUSINDO | B2B | tinggi | kecil | kadang | sedikit | lama | 7 | sedang |
| JKTC0437 | PYRIDAM FARMA | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| SUBB2B0016 | RAAH INTERNATIONAL INDONESIA | B2B | tinggi | besar | kadang | banyak | baru | 12 | tinggi |
| JKTB2B0025 | RAF CAHAYA LESTARI | B2B | tinggi | kecil | jarang | sedikit | lama | 6 | rendah |
| JKTC00256 | RAJAWALI NUSINDO | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| JKTB2B0030 | RIZQULLAH MEDISKA INDONESIA ( EXIM ) | B2B | tinggi | besar | kadang | sedikit | lama | 9 | sedang |
| JKTB2B0042 | SABA INDOMEDIKA | B2B | tinggi | sedang | kadang | sedang | lama | 9 | sedang |
| JKTC00263 | SALI POLAPA BERSAMA | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| JKTB2B0142 | SAMMARIE TRAMEDIFA  | B2B | sedang | kecil | jarang | sedikit | baru | 6 | rendah |
| JKTB2B0012 | SAMUDERA JAYA MEDIKA  | B2B | tinggi | besar | kadang | banyak | lama | 11 | tinggi |
| SUBB2B0038 | SANDANA | B2B | rendah | sedang | jarang | sedikit | baru | 6 | rendah |
| JKTB2B0140 | SANDANA  | B2B | rendah | kecil | jarang | sedikit | baru | 5 | rendah |
| JKTC0599 | SANDRAINDAH SASMAYA  | B2B | tinggi | besar | kadang | banyak | lama | 11 | tinggi |
| JKTC0510 | SANSICO NATURA RESOURCES | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| JKTB2B0135 | SARANA MEDIKAL PRISMA  | B2B | sedang | kecil | jarang | sedikit | baru | 6 | rendah |
| SUBC0046 | SARI WARNA PELANGI | B2B | tinggi | kecil | sering | sedikit | lama | 8 | sedang |
| JKTB2B0067 | SEDULUR TEKNIK MADANI  | B2B | tinggi | besar | jarang | sedang | baru | 10 | tinggi |
| SUBC0092 | SEGAR MANDIRI ABADI | B2B | tinggi | kecil | kadang | sedikit | lama | 7 | sedang |
| JKTC00273 | SEGARA HUSADA MANDIRI | B2B | sedang | kecil | sering | sedang | lama | 8 | sedang |
| SUBB2B0018 | SEKAR | B2B | rendah | sedang | jarang | sedikit | baru | 6 | rendah |
| SUBB2B0019 | SEKAR | B2B | tinggi | kecil | jarang | sedikit | baru | 7 | sedang |
| JKT0001C0001 | SEL REGENERASI BIOTEK | B2B | sedang | sedang | kadang | banyak | lama | 9 | sedang |
| SUBC0123 | SEMESTA PERKAKAS MANDIRI | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| JKTB2B0118 | SENTRAL MEDIKA INDOPUTRA  | B2B | sedang | sedang | jarang | sedang | baru | 8 | sedang |
| JKTB2B0131 | SINAR RODA UTAMA  | B2B | sedang | sedang | jarang | sedang | baru | 8 | sedang |
| JKTC0420 | SINERGI UTAMA SEJAHTERA | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| JKTC00286 | SMI MESIN INDONESIA | B2B | tinggi | kecil | kadang | sedang | lama | 8 | sedang |
| JKTB2B0052 | SNIBE DIAGNOSTIC INDONESIA ( EXIM ) | B2B | tinggi | sedang | kadang | banyak | baru | 11 | tinggi |
| JKTC0467 | SOLUSI SENYUM INDONESIA | B2B | tinggi | sedang | kadang | sedang | lama | 9 | sedang |
| JKTC00288 | SOMETECH INDONESIA | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| JKTB2B0141 | SONNA MEDIKA JAYA CAB. JAKARTA | B2B | rendah | kecil | jarang | sedikit | baru | 5 | rendah |
| SUBC0069 | SUMBER UTAMA KIMIAMURNI | B2B | tinggi | kecil | jarang | sedang | lama | 7 | sedang |
| JKTB2B0047 | SUNINDO GAPURA PRIMA  | B2B | tinggi | kecil | jarang | sedikit | lama | 6 | rendah |
| JKTC00297 | SURYA TAMA MEDIKA | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| JKTC00299 | SYSMEX INDONESIA | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| JKTC00300 | TAMARA OVERSEAS CORPORINDO | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| SUBB2B0015 | TEK MANDIRI | B2B | tinggi | sedang | jarang | sedikit | baru | 8 | sedang |
| JKTC00306 | TIRTA MEDICAL INDONESIA | B2B | tinggi | sedang | sering | banyak | lama | 11 | tinggi |
| SUBC0074 | TITIEN ANDARU JAYA | B2B | tinggi | besar | kadang | banyak | lama | 11 | tinggi |
| JKTC00310 | TOPSINDO MEGAH UTAMA | B2B | tinggi | sedang | sering | banyak | lama | 11 | tinggi |
| SUBC0126 | TOTO TENTREM | B2B | tinggi | besar | kadang | sedang | lama | 10 | tinggi |
| JKTB2B0073 | TRAKTOR UTAMA NUSANTARA (EXIM) | B2B | tinggi | kecil | kadang | sedikit | baru | 8 | sedang |
| JKTC00313 | TRANSMEDIC INDONESIA | B2B | tinggi | besar | sering | banyak | lama | 12 | tinggi |
| JKTC0527 | TRANSNATIONAL SOLUTIONS (EXIM) | B2B | tinggi | besar | jarang | sedikit | lama | 8 | sedang |
| SUBC0052 | TRIASTRI MEDITAMA | B2B | rendah | kecil | jarang | sedikit | lama | 4 | rendah |
| JKTC0559 | TRIMEGA PRIMA TEKNOLOGI | B2B | tinggi | besar | jarang | banyak | lama | 10 | tinggi |
| JKTC00316 | TRINITY SUKSES | B2B | tinggi | kecil | kadang | sedang | lama | 8 | sedang |
| JKTC00317 | TRIPATRIA ANDALAN MEDIKA | B2B | tinggi | sedang | sering | sedang | lama | 10 | tinggi |
| JKTC00318 | TRIPUTRA TECHNO MED | B2B | sedang | sedang | sering | sedang | lama | 9 | sedang |
| JKTB2B0009 | UNIT DONOR DARAH PMI KOTA PONTIANAK  | B2B | tinggi | besar | kadang | banyak | lama | 11 | tinggi |
| JKTC0579 | UNITED DICO CITAS | B2B | tinggi | besar | sering | sedang | lama | 11 | tinggi |
| JKTDIS0006 | UTD PMI PEKANBARU  | DISTRI | sedang | besar | kadang | banyak | lama | 10 | tinggi |
| SUBB2B0031 | VIRTUE DIAGNOSTICS INDONESIA | B2B | tinggi | besar | jarang | sedang | baru | 10 | tinggi |
| JKTB2B0127 | VISI YOSINDO MEDIKAL  | B2B | tinggi | sedang | jarang | sedikit | baru | 8 | sedang |
| SUBC00012 | WAHANA RIZKY GUMILANG | B2B | tinggi | besar | kadang | sedikit | lama | 9 | sedang |

Distribusi label pada dataset siap digunakan adalah 25 data Risiko Rendah, 87 data Risiko Sedang, dan 70 data Risiko Tinggi.

## 11. Evaluasi Model

Evaluasi digunakan untuk mengetahui seberapa baik model mengklasifikasikan pelanggan ke dalam risiko rendah, sedang, dan tinggi. Metrik yang digunakan meliputi akurasi, precision, recall, F1-Score, dan confusion matrix.

Akurasi menunjukkan persentase prediksi yang benar dari seluruh data uji. Precision menunjukkan ketepatan model ketika memberikan prediksi pada suatu kelas risiko. Recall menunjukkan kemampuan model menemukan seluruh data yang seharusnya masuk ke kelas risiko tertentu. F1-Score menunjukkan keseimbangan antara precision dan recall. Confusion matrix menunjukkan perbandingan antara label sebenarnya dan hasil prediksi model.

### 11.1 Ringkasan Evaluasi

| Metrik | Nilai | Keterangan |
| --- | --- | --- |
| Jumlah data | 182 | Total data yang digunakan dalam proses model. |
| Data latih | 145 | Data yang digunakan untuk mempelajari pola risiko piutang. |
| Data uji | 37 | Data yang digunakan untuk menguji kemampuan klasifikasi model. |
| Akurasi | 86,49% | Persentase prediksi yang tepat dari seluruh data uji. |
| Macro Precision | 92,75% | Rata-rata ketepatan prediksi pada setiap kelas risiko. |
| Macro Recall | 79,52% | Rata-rata kemampuan model menemukan data pada setiap kelas risiko. |
| Macro F1-Score | 83,60% | Rata-rata keseimbangan antara precision dan recall. |

### 11.2 Evaluasi per Kelas

| Kelas Risiko | Precision | Recall | F1-Score | Jumlah Data Uji |
| --- | --- | --- | --- | --- |
| Rendah | 100,00% | 60,00% | 75,00% | 5 |
| Sedang | 78,26% | 100,00% | 87,80% | 18 |
| Tinggi | 100,00% | 78,57% | 88,00% | 14 |

### 11.3 Confusion Matrix

| Label Sebenarnya / Prediksi | Rendah | Sedang | Tinggi |
| --- | --- | --- | --- |
| Rendah | 3 | 2 | 0 |
| Sedang | 0 | 18 | 0 |
| Tinggi | 0 | 3 | 11 |

## 12. Hasil Klasifikasi

Hasil klasifikasi model berupa label risiko piutang pelanggan, yaitu Risiko Rendah, Risiko Sedang, atau Risiko Tinggi. Pada program, hasil ini dapat disertai probabilitas untuk menunjukkan tingkat keyakinan model terhadap label yang dipilih.

Tabel berikut menampilkan contoh hasil klasifikasi berdasarkan model yang tersedia dan dataset siap digunakan.

| Kode Pelanggan | Nama Pelanggan | Skor Risiko | Label Aturan | Hasil Model | Probabilitas Tertinggi |
| --- | --- | --- | --- | --- | --- |
| SUBC00026 | ANUGERAH SANTOSA ABADI CAB SURABAYA | 5 | Rendah | Rendah | 52,85% |
| JKTB2B0080 | ABADI RIZKI MEDIKA | 9 | Sedang | Sedang | 84,76% |
| JKTC00002 | ABHIMATA MANUNGGAL | 12 | Tinggi | Tinggi | 99,73% |

## 13. Kesimpulan

Model klasifikasi piutang pelanggan dengan metode Naive Bayes dapat membantu perusahaan mengelompokkan pelanggan berdasarkan tingkat risiko piutangnya. Model menggunakan atribut yang relevan, yaitu umur piutang, nominal piutang, frekuensi keterlambatan, jumlah invoice belum lunas, dan status customer.

Sistem ini dapat membantu proses analisis risiko piutang pelanggan dan menjadi alat bantu awal bagi perusahaan dalam menentukan prioritas pemantauan atau penagihan. Hasil klasifikasi sebaiknya digunakan sebagai bahan pertimbangan, bukan sebagai keputusan mutlak, karena keputusan akhir tetap perlu memperhatikan kebijakan dan pertimbangan bisnis perusahaan.
