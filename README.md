# POS Minimarket - Aplikasi Point of Sale untuk Minimarket

Aplikasi POS desktop berbasis Python untuk minimarket dengan fitur lengkap: transaksi, manajemen produk & stok, multi-user, laporan, integrasi printer thermal, notifikasi Telegram, dan backup/restore.

## � Dokumentasi Lengkap

- 🚀 **[QUICKSTART.md](QUICKSTART.md)** - Panduan cepat instalasi & penggunaan (mulai dari sini!)
- 👨‍💻 **[DEVELOPMENT.md](DEVELOPMENT.md)** - Panduan developer & coding guidelines
- ✅ **[MVP_CHECKLIST.md](MVP_CHECKLIST.md)** - Checklist implementasi MVP
- 📂 **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Struktur project lengkap
- 📝 **[CHANGELOG.md](CHANGELOG.md)** - Version history & roadmap
- 📋 **[specs/POS_spec.md](specs/POS_spec.md)** - Spesifikasi detail semua modul

## �📋 Fitur Utama

- ✅ Multi-user dengan 3 role: Admin, Kasir, Executive
- 🛒 Transaksi penjualan dengan keranjang, diskon, pajak (PPN), split payment
- 📦 Manajemen produk: CRUD, kategori, stok otomatis
- 📊 Manajemen stok: riwayat, notifikasi low-stock via Telegram
- 👥 Manajemen pelanggan & riwayat pembelian
- 💰 Multi-mode pembayaran: cash, kartu, QRIS, e-wallet
- 📈 Laporan & analisis: harian, mingguan, bulanan, produk terlaris
- 🖨️ Integrasi printer thermal (ESC/POS)
- 🏢 Support multi-outlet/cabang
- 📥 Import/Export data (CSV, Excel)
- 💾 Backup & restore database
- ♻️ Retur/refund

## 🛠️ Tech Stack

- **Python**: 3.10+
- **GUI**: PySide6 (Qt for Python)
- **Database**: SQLite (lokal) / PostgreSQL (multi-outlet terpusat)
- **ORM**: SQLAlchemy
- **Password**: bcrypt hashing
- **Printer**: python-escpos
- **Telegram**: python-telegram-bot
- **CSV/Excel**: pandas, openpyxl

## 📁 Struktur Project

```
minimarket/
├── config.py               # Konfigurasi aplikasi
├── create_db.py            # Script inisialisasi database
├── main.py                 # Entry point aplikasi
├── requirements.txt        # Python dependencies
├── README.md              # Dokumentasi ini
├── .gitignore
├── minimarket.sqlite3     # Database (dibuat setelah run create_db.py)
├── db/
│   └── schema.sql         # DDL schema database
├── src/
│   ├── __init__.py
│   ├── db_manager.py      # Database connection & session
│   ├── models.py          # SQLAlchemy ORM models
│   ├── auth/              # (akan dibuat) Modul authentication
│   ├── pos/               # (akan dibuat) Modul POS/transaksi
│   ├── products/          # (akan dibuat) Modul produk
│   ├── stock/             # (akan dibuat) Modul stok
│   ├── customers/         # (akan dibuat) Modul pelanggan
│   ├── reports/           # (akan dibuat) Modul laporan
│   └── utils/             # (akan dibuat) Utilities
├── specs/
│   └── POS_spec.md        # Spesifikasi lengkap modul
└── tests/                 # (akan dibuat) Unit tests
```

## 🚀 Setup & Instalasi (Windows)

### 1. Install Python

Download dan install Python 3.10+ dari [python.org](https://www.python.org/downloads/)
- ✅ Centang "Add Python to PATH" saat instalasi

Verifikasi instalasi:
```powershell
python --version
```

### 2. Clone atau Download Project

```powershell
cd C:\xampp\htdocs
# Atau jika sudah ada:
cd C:\xampp\htdocs\minimarket
```

### 3. Buat Virtual Environment

```powershell
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
.\venv\Scripts\Activate.ps1
```

**Catatan**: Jika ada error "execution policy", jalankan:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install Dependencies

```powershell
# Pastikan venv aktif (ada prefix (venv) di prompt)
pip install --upgrade pip
pip install -r requirements.txt
```

Proses ini akan menginstall:
- PySide6 (GUI framework)
- SQLAlchemy (ORM)
- bcrypt (password hashing)
- pandas, openpyxl (CSV/Excel)
- python-telegram-bot (notifikasi)
- python-escpos (printer thermal)
- pytest (testing)

### 5. Inisialisasi Database

```powershell
python create_db.py
```

Script ini akan:
- Membuat file `minimarket.sqlite3`
- Membuat semua tabel dari `db/schema.sql`
- Insert data default: roles, outlet, admin user, pajak PPN

**Default credentials**:
- Username: `admin`
- Password: `admin123`

### 6. Jalankan Aplikasi

```powershell
python main.py
```

Aplikasi akan membuka window GUI utama.

## ⚙️ Konfigurasi

Edit file `config.py` untuk mengatur:

### Database
```python
DB_PATH = BASE_DIR / 'minimarket.sqlite3'  # Path database
```

### Telegram Bot (untuk notifikasi low-stock)
```python
TELEGRAM_BOT_TOKEN = 'your_bot_token_here'
TELEGRAM_CHAT_ID = 'your_chat_id_here'
```

Cara dapat token:
1. Buat bot baru di Telegram via [@BotFather](https://t.me/botfather)
2. Copy token yang diberikan
3. Dapatkan chat_id dengan kirim pesan ke bot, lalu buka:
   `https://api.telegram.org/bot<TOKEN>/getUpdates`

### Printer Thermal
```python
PRINTER_ENABLED = True
PRINTER_TYPE = 'usb'  # atau 'serial', 'network'
PRINTER_DEVICE = 'USB\\VID_XXXX&PID_XXXX'  # Device path
```

### Pajak & Mata Uang
```python
DEFAULT_TAX_RATE = 10.0  # PPN 10%
AUTO_APPLY_TAX = True
CURRENCY_SYMBOL = 'Rp'
```

## 📝 Development Workflow

### Menjalankan Tests
```powershell
pytest tests/
```

### Reset Database (hati-hati!)
```powershell
# Backup dulu jika ada data penting
python create_db.py
# Jawab 'y' untuk overwrite
```

### Export/Backup Database
```powershell
# Copy manual
copy minimarket.sqlite3 backups\minimarket_backup_YYYYMMDD.sqlite3

# Atau gunakan fitur backup di aplikasi (akan diimplementasikan)
```

## 🔐 Security Notes

- Password disimpan ter-hash dengan bcrypt (never plaintext)
- Default admin password **harus diganti** setelah first login
- File `config.py` berisi setting sensitif - jangan commit ke public repo
- Gunakan `.env` file atau Windows Credential Store untuk production

## 📚 Next Steps - Implementasi Modul

Lihat `specs/POS_spec.md` untuk detail lengkap per modul.

**Urutan implementasi yang disarankan:**
1. ✅ Setup project skeleton (done)
2. ⏳ Modul Auth & Login UI
3. ⏳ Modul Product CRUD
4. ⏳ Modul POS (transaksi cash only)
5. ⏳ Multi-payment & split payment
6. ⏳ Laporan & export CSV
7. ⏳ Integrasi printer
8. ⏳ Stock notification (Telegram)
9. ⏳ Refund/retur
10. ⏳ Multi-outlet

## 🐛 Troubleshooting

### Import Error: PySide6/SQLAlchemy tidak ditemukan
```powershell
# Pastikan venv aktif
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Database error: "unable to open database file"
- Pastikan `create_db.py` sudah dijalankan
- Cek path di `config.py` sudah benar
- Pastikan folder writable

### Printer tidak terdeteksi
- Install driver printer thermal
- Cek device path di Device Manager (Windows)
- Test dengan aplikasi lain (mis. notepad) untuk memastikan printer berfungsi

### Telegram bot tidak kirim notifikasi
- Verifikasi `TELEGRAM_BOT_TOKEN` dan `TELEGRAM_CHAT_ID` benar
- Test dengan kirim pesan manual via Python:
```python
from telegram import Bot
bot = Bot(token='YOUR_TOKEN')
bot.send_message(chat_id='YOUR_CHAT_ID', text='Test')
```

## 📄 License

Proprietary / Internal use only (atau sesuaikan dengan kebutuhan)

## 👨‍💻 Development

Untuk kontribusi atau pertanyaan, hubungi team development.

---

**Version**: 0.1.0 (MVP in development)  
**Last Updated**: November 11, 2025
