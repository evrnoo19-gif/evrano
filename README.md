# EVRANOO — Personal Dashboard
> Dark luxury personal dashboard: IHSG · Emas · Rupiah · Tabungan · Kebiasaan Harian

---

## 📁 Struktur File

```
evranoo/
├── app.py              ← Backend Python (Flask)
├── requirements.txt    ← Library Python
├── Procfile            ← Perintah start untuk Railway
├── railway.toml        ← Konfigurasi Railway
└── templates/
    └── index.html      ← Frontend (HTML + CSS + JS)
```

---

## 🚀 Deploy ke Railway (GRATIS) — Langkah per Langkah

### 1. Buat akun GitHub
Kalau belum punya, daftar di https://github.com

### 2. Upload project ke GitHub
1. Buka https://github.com → klik **"New repository"**
2. Nama repo: `evranoo`
3. Pilih **Public** → klik **"Create repository"**
4. Upload semua file project ini ke repo tersebut
   (klik "uploading an existing file" di halaman repo)

### 3. Buat akun Railway
1. Buka https://railway.app
2. Klik **"Start a New Project"**
3. Login dengan akun GitHub kamu

### 4. Deploy project
1. Di Railway, klik **"New Project"**
2. Pilih **"Deploy from GitHub repo"**
3. Pilih repo `evranoo` yang tadi dibuat
4. Railway otomatis mendeteksi Python dan mulai build
5. Tunggu 2-3 menit sampai status **"Active"**

### 5. Buka website kamu
1. Di Railway, klik project → tab **"Settings"**
2. Scroll ke **"Domains"** → klik **"Generate Domain"**
3. Kamu dapat link seperti: `evranoo-production.up.railway.app`
4. Buka link itu di browser mana saja → masukkan password **E210**

---

## 🔑 Password
Password default: **E210**

Untuk ganti password, buka file `app.py`, cari baris:
```python
PASSWORD = "E210"
```
Ganti dengan password yang kamu inginkan, lalu push ulang ke GitHub.

---

## 💡 Tips
- Data tersimpan di server Railway, sinkron di semua device
- Grafik pasar pakai TradingView (real-time, gratis)
- Kalau Railway free tier habis, upgrade ke Hobby plan ($5/bulan)
