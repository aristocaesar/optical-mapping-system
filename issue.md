# Project Planning: Optical Mapping System (CABLEMAP)

## Deskripsi Proyek
**Nama Aplikasi:** CABLEMAP
**Deskripsi:** Proyek web aplikasi ini bertujuan untuk menerima dan memvisualisasikan data (GPS, NPK / Soil Sensor 7 in 1) yang dikirimkan dari perangkat IoT (mikrokontroller) melalui HTTP POST. Dokumen ini mendefinisikan langkah awal untuk inisialisasi proyek, struktur direktori (MVC), serta migrasi database yang dibutuhkan.

## Spesifikasi Data IoT
Data yang akan dikirimkan oleh mikrokontroller memiliki format JSON berikut:
```json
{
  "lat": -8.439643,
  "lon": 114.189667,
  "hum": 24.7,
  "temp": 29.4,
  "ec": 447,
  "ph": 6.4,
  "n": 54,
  "p": 172,
  "k": 166
}
```

## Spesifikasi Teknologi
- **Bahasa Pemrograman:** Python
- **Framework Web:** Flask
- **Database:** PostgreSQL + PostGIS
- **ORM & Migrasi:** Flask-SQLAlchemy, GeoAlchemy2 (untuk PostGIS), dan Flask-Migrate
- **Library Peta (Frontend):** Leaflet.js
- **Kredensial Database:**
  - Database: `ocm_app`
  - Username: `aristocaesar`
  - Password: `aristo0407`

## Struktur Tabel Database

1. **`users`** (Untuk menyimpan pengguna yang login ke sistem)
   - `id` (Primary Key)
   - `fullname` (String)
   - `email` (String, Unique)
   - `password` (String, Hashed)
   - `created_at` (DateTime)
   - `updated_at` (DateTime)

2. **`sessions`** (Untuk menyimpan sesi pemetaan, sebagai parent data IoT)
   - `id` (Primary Key)
   - `session_id` (String, Unique, misal: OCM-XXXXX)
   - `name` (String)
   - `is_active` (Boolean, Default: false)
   - `created_at` (DateTime)
   - `updated_at` (DateTime)

3. **`session_data`** (Untuk menyimpan data point dari IoT)
   - `id` (Primary Key)
   - `session_id` (Foreign Key ke `sessions.id`)
   - `lat` (Float)
   - `lon` (Float)
   - `hum` (Float)
   - `temp` (Float)
   - `ec` (Integer/Float)
   - `ph` (Float)
   - `n` (Integer)
   - `p` (Integer)
   - `k` (Integer)
   - `score` (Float/Integer, nullable)

## Langkah-langkah Pengerjaan (Task List)

Silakan kerjakan langkah-langkah inisialisasi di bawah ini secara berurutan. **PENTING: Jangan bangun bagian View/UI frontend terlebih dahulu, fokus pada inisialisasi backend, struktur, database, dan API endpoint yang diminta.**

- [ ] **Langkah 1: Setup Proyek & Instalasi Dependencies**
  - Buat virtual environment (misal `venv`) dan inisialisasi proyek Flask.
  - Install dependencies yang dibutuhkan: `Flask`, `Flask-SQLAlchemy`, `GeoAlchemy2`, `psycopg2-binary`, `Flask-Migrate`, `python-dotenv`.
  - Buat file `.env` untuk menyimpan koneksi database: `DATABASE_URL=postgresql://aristocaesar:aristo0407@localhost/ocm_app` (Sesuaikan port jika perlu).

- [ ] **Langkah 2: Inisialisasi Struktur Direktori (MVC)**
  - Buat struktur direktori MVC yang rapi dan modular. Contoh struktur yang disarankan:
    ```text
    /
    ├── app/
    │   ├── __init__.py        # Setup Flask app, DB, Migrate
    │   ├── models/            # Definisi model SQLAlchemy (users, sessions, session_data)
    │   ├── controllers/       # Logika API dan Endpoint
    │   └── utils/             # Helper/Utility functions
    ├── migrations/            # Folder hasil Flask-Migrate
    ├── seeders/               # File untuk seeding data awal
    ├── .env                   # Environment variables
    ├── config.py              # Konfigurasi aplikasi Flask
    ├── requirements.txt       # Daftar dependencies
    └── run.py                 # Entry point aplikasi
    ```

- [ ] **Langkah 3: Definisi Model & Inisialisasi File Migrasi**
  - Buat model untuk tabel `users`, `sessions`, dan `session_data` menggunakan `Flask-SQLAlchemy`.
  - Lakukan inisialisasi Flask-Migrate (`flask db init`, `flask db migrate`, `flask db upgrade`) untuk membuat tabel-tabel tersebut di database `ocm_app`.

- [ ] **Langkah 4: Pembuatan Seeder**
  - Buat script seeder (misal `seeders/seed.py` atau custom Flask CLI command) untuk mengisi data awal dummy pada ketiga tabel tersebut (`users`, `sessions`, dan `session_data`).
  - Pastikan ada setidaknya satu record di tabel `sessions` yang memiliki nilai `is_active = true`.

- [ ] **Langkah 5: Pembuatan Endpoint API**
  - Buat endpoint `POST /api/store-session`.
  - **Logika Endpoint:**
    - Terima payload JSON sesuai format IoT di atas.
    - Cari *single record* dari tabel `sessions` dimana `is_active = true`.
    - Jika ada sesi yang aktif, simpan data dari IoT ke tabel `session_data` dengan `session_id` yang merujuk ke id sesi aktif tersebut.
    - Jika tidak ada sesi yang aktif, kembalikan response error (misal: HTTP 400 Bad Request, "Tidak ada sesi pemetaan yang aktif").
    - Kembalikan response sukses (HTTP 201/200) jika data berhasil disimpan.

**Catatan:** Pastikan kode ditulis dengan rapi (clean code), gunakan error handling yang baik (terutama saat parsing JSON dan koneksi DB), serta berikan komentar yang jelas agar mudah dilanjutkan.
