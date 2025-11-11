# Quick Start Guide - POS Minimarket

Panduan cepat untuk mulai menggunakan aplikasi POS Minimarket.

## 🚀 Instalasi Pertama Kali (5 menit)

### Windows (Recommended: Double-click batch file)

1. **Download & Extract** project ke `C:\xampp\htdocs\minimarket`

2. **Run Setup** — Double-click file ini:
   ```
   setup.bat
   ```
   Script akan otomatis:
   - Check Python (jika belum ada, install dari python.org)
   - Buat virtual environment
   - Install dependencies
   - Buat database + seed data
   - Run tests

3. **Jalankan Aplikasi** — Double-click:
   ```
   run.bat
   ```

**Default Login:**
- Username: `admin`
- Password: `admin123`

---

## 💻 Instalasi Manual (jika batch gagal)

### Langkah 1: Install Python
Download dari https://python.org/downloads/ (versi 3.10+)
✅ Centang "Add Python to PATH"

### Langkah 2: Buka PowerShell/Terminal
```powershell
cd C:\xampp\htdocs\minimarket
```

### Langkah 3: Setup Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Jika error "execution policy":**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Langkah 4: Install Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### Langkah 5: Buat Database
```powershell
python create_db.py
```

### Langkah 6: Run Aplikasi
```powershell
python main.py
```

---

## 📱 Menggunakan Aplikasi

### Pertama Kali Login
1. Klik tombol "Login"
2. Username: `admin` | Password: `admin123`
3. **WAJIB**: Ganti password default setelah login pertama (fitur akan ditambahkan)

### Role & Permission
- **Admin**: Akses penuh (user management, products, reports, settings)
- **Kasir**: POS/transaksi, lihat produk, cetak struk
- **Executive**: Lihat laporan saja (read-only)

---

## 🛠️ Konfigurasi (Optional)

Edit file `config.py`:

### Database Path
```python
DB_PATH = BASE_DIR / 'minimarket.sqlite3'
```

### Telegram Notifications
```python
TELEGRAM_BOT_TOKEN = 'your_bot_token'
TELEGRAM_CHAT_ID = 'your_chat_id'
```

### Printer Thermal
```python
PRINTER_ENABLED = True
PRINTER_DEVICE = 'USB\\VID_XXXX&PID_XXXX'  # Lihat Device Manager
```

---

## 🧪 Testing (untuk Developer)

```powershell
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_database.py -v

# Run with coverage
pytest --cov=src tests/
```

---

## 📂 File Penting

| File                  | Deskripsi                                      |
|-----------------------|------------------------------------------------|
| `setup.bat`           | Auto-setup (first time only)                   |
| `run.bat`             | Jalankan aplikasi                              |
| `main.py`             | Entry point aplikasi                           |
| `create_db.py`        | Inisialisasi database + seed                   |
| `config.py`           | Konfigurasi (DB, Telegram, Printer)            |
| `README.md`           | Dokumentasi lengkap                            |
| `DEVELOPMENT.md`      | Panduan developer                              |
| `MVP_CHECKLIST.md`    | Checklist implementasi                         |
| `specs/POS_spec.md`   | Spesifikasi detail semua modul                 |
| `db/schema.sql`       | DDL database                                   |
| `minimarket.sqlite3`  | Database file (created after setup)            |

---

## ❓ Troubleshooting

### "Python not found"
→ Install Python dari python.org, centang "Add to PATH"

### "No module named 'PySide6'"
→ Aktifkan venv: `.\venv\Scripts\Activate.ps1`, lalu `pip install -r requirements.txt`

### "Database not found"
→ Run: `python create_db.py`

### Login gagal
→ Reset database: `python create_db.py` (jawab 'y'), lalu login dengan `admin` / `admin123`

### Lupa password
→ Reset via database atau script manual (lihat DEVELOPMENT.md)

---

## 📞 Support

Untuk bantuan atau pertanyaan:
- Baca dokumentasi: `README.md`, `DEVELOPMENT.md`
- Check issue di specs: `specs/POS_spec.md`
- Review checklist: `MVP_CHECKLIST.md`

---

## 🎯 Next Steps (untuk Developer)

1. ✅ Setup selesai
2. ⏳ Implement Auth Module (lihat `DEVELOPMENT.md`)
3. ⏳ Implement Product Module
4. ⏳ Implement POS Module
5. ⏳ Testing & UAT

**Total estimasi MVP: ~1 minggu**

---

**Selamat menggunakan POS Minimarket!** 🎉
