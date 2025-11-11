# Project Structure - POS Minimarket

Visualisasi lengkap struktur project untuk referensi cepat.

```
C:\xampp\htdocs\minimarket\
│
├── 📄 README.md                    ✅ Dokumentasi utama (user-facing)
├── 📄 QUICKSTART.md                ✅ Panduan cepat instalasi & usage
├── 📄 DEVELOPMENT.md               ✅ Panduan developer (coding guidelines)
├── 📄 MVP_CHECKLIST.md             ✅ Checklist implementasi MVP
├── 📄 PROJECT_STRUCTURE.md         ✅ File ini (struktur project)
│
├── 📄 config.py                    ✅ Konfigurasi aplikasi (DB, Telegram, Printer)
├── 📄 create_db.py                 ✅ Script inisialisasi database + seed data
├── 📄 main.py                      ✅ Entry point aplikasi GUI
├── 📄 requirements.txt             ✅ Python dependencies
├── 📄 .gitignore                   ✅ Git ignore rules
│
├── 🖥️ setup.bat                    ✅ Windows batch: auto-setup
├── 🖥️ run.bat                      ✅ Windows batch: run aplikasi
│
├── 💾 minimarket.sqlite3           ⏳ Database file (created after setup)
│
├── 📁 db/
│   └── 📄 schema.sql               ✅ DDL lengkap SQLite (19 tables)
│
├── 📁 specs/
│   └── 📄 POS_spec.md              ✅ Spesifikasi detail semua modul
│
├── 📁 src/                         
│   ├── 📄 __init__.py              ✅ Package init
│   ├── 📄 db_manager.py            ✅ SQLAlchemy engine & session factory
│   ├── 📄 models.py                ✅ ORM models lengkap (14 models)
│   │
│   ├── 📁 auth/                    ⏳ TODO: Authentication & user management
│   │   ├── __init__.py
│   │   ├── service.py              → AuthService (login, logout, permissions)
│   │   ├── ui.py                   → LoginDialog, UserManagementUI
│   │   └── utils.py                → Password helpers
│   │
│   ├── 📁 pos/                     ⏳ TODO: Point of Sale / Transaksi
│   │   ├── __init__.py
│   │   ├── service.py              → POSService, Cart class
│   │   ├── ui.py                   → POSWindow (keranjang, payment, checkout)
│   │   └── utils.py                → Calculation helpers
│   │
│   ├── 📁 products/                ⏳ TODO: Product & Category management
│   │   ├── __init__.py
│   │   ├── service.py              → ProductService (CRUD)
│   │   ├── ui.py                   → ProductListWindow, ProductFormDialog
│   │   └── utils.py                → Product helpers
│   │
│   ├── 📁 stock/                   ⏳ TODO: Stock management & alerts
│   │   ├── __init__.py
│   │   ├── service.py              → StockService (movements, alerts)
│   │   ├── ui.py                   → StockAdjustmentDialog
│   │   └── utils.py                → Stock calculation helpers
│   │
│   ├── 📁 customers/               ⏳ TODO: Customer management & loyalty
│   │   ├── __init__.py
│   │   ├── service.py              → CustomerService (CRUD, history)
│   │   ├── ui.py                   → CustomerListWindow, CustomerFormDialog
│   │   └── utils.py                → Customer helpers
│   │
│   ├── 📁 reports/                 ⏳ TODO: Reports & analytics
│   │   ├── __init__.py
│   │   ├── service.py              → ReportService (sales, stock, cashier)
│   │   ├── ui.py                   → ReportWindow, filters, charts
│   │   └── export.py               → CSV/Excel export
│   │
│   ├── 📁 payments/                ⏳ TODO: Payment processing
│   │   ├── __init__.py
│   │   ├── service.py              → PaymentService (multi-payment, split)
│   │   ├── ui.py                   → PaymentDialog
│   │   └── utils.py                → Payment calculation
│   │
│   ├── 📁 integrations/            ⏳ TODO: External integrations
│   │   ├── __init__.py
│   │   ├── printer.py              → PrinterService (ESC/POS, receipt)
│   │   ├── telegram.py             → TelegramService (low-stock alerts)
│   │   └── backup.py               → BackupService (DB backup/restore)
│   │
│   └── 📁 utils/                   ⏳ TODO: Shared utilities
│       ├── __init__.py
│       ├── currency.py             → rupiah_to_cents, cents_to_rupiah
│       ├── validators.py           → Input validation helpers
│       ├── formatters.py           → Date, number formatting
│       └── logger.py               → Logging setup
│
└── 📁 tests/                       
    ├── 📄 __init__.py              ✅ Test package init
    ├── 📄 test_database.py         ✅ Basic DB connection tests
    │
    ├── 📄 test_auth.py             ⏳ TODO: Auth module tests
    ├── 📄 test_products.py         ⏳ TODO: Product CRUD tests
    ├── 📄 test_pos.py              ⏳ TODO: POS transaction tests
    ├── 📄 test_stock.py            ⏳ TODO: Stock movement tests
    ├── 📄 test_payments.py         ⏳ TODO: Payment processing tests
    ├── 📄 test_reports.py          ⏳ TODO: Report generation tests
    ├── 📄 test_integrations.py     ⏳ TODO: Printer, Telegram tests
    └── 📄 conftest.py              ⏳ TODO: pytest fixtures & config
```

---

## 📊 Database Schema Overview

### Core Tables (19 total)
```
users ─────┬──→ roles
           ├──→ outlets
           └──→ transactions

products ──┬──→ categories
           ├──→ product_stocks (per outlet)
           ├──→ stock_movements (history)
           └──→ transaction_items

transactions ──┬──→ users (kasir)
               ├──→ outlets
               ├──→ customers
               ├──→ transaction_items
               └──→ payments

customers ──→ transactions (via customer_id)

shifts ──→ users (kasir shifts)

discounts (predefined discount rules)
taxes (PPN, etc.)
refunds ──→ transactions
telegram_notifications (low stock alerts)
backups (backup metadata)
```

Lihat detail DDL di `db/schema.sql`.

---

## 🎨 UI Components (PySide6)

### Main Window
```
┌─────────────────────────────────────────┐
│ POS Minimarket v0.1.0           [User]▼ │ ← Menu bar
├─────────────────────────────────────────┤
│  [POS] [Products] [Reports] [Settings]  │ ← Tab navigation
├─────────────────────────────────────────┤
│                                         │
│  (Content area - dynamic per module)    │
│                                         │
│                                         │
└─────────────────────────────────────────┘
```

### POS Window Layout
```
┌─────────────────────────────────────────────────┐
│  Search/Scan: [___________________] [Add]       │
├─────────────┬───────────────────────────────────┤
│  Product    │  CART                             │
│  List       │  ┌─────────────────────────────┐  │
│  ┌────────┐ │  │ Item    Qty  Price  Total   │  │
│  │ Item 1 │ │  │ ─────────────────────────── │  │
│  │ Item 2 │ │  │ Susu    2x   5000   10000   │  │
│  │ Item 3 │ │  │ Roti    1x   3000   3000    │  │
│  │ ...    │ │  └─────────────────────────────┘  │
│  └────────┘ │                                   │
│             │  Subtotal:           Rp 13.000    │
│             │  Pajak (10%):        Rp 1.300     │
│             │  Diskon:             Rp 0         │
│             │  ─────────────────────────────    │
│             │  TOTAL:              Rp 14.300    │
│             │                                   │
│             │  Bayar:  [_______] Rp             │
│             │  Kembali:           Rp 0          │
│             │                                   │
│             │  [Checkout] [Clear Cart]          │
└─────────────┴───────────────────────────────────┘
```

---

## 🔌 Tech Stack & Libraries

### Core
- **Python**: 3.10+ (Windows)
- **GUI**: PySide6 (Qt for Python)
- **Database**: SQLite 3
- **ORM**: SQLAlchemy 2.0

### Security
- **bcrypt**: Password hashing

### Data Processing
- **pandas**: CSV/Excel processing
- **openpyxl**: Excel file format support

### Integrations
- **python-telegram-bot**: Telegram notifications
- **python-escpos**: Thermal printer (ESC/POS)

### Testing
- **pytest**: Unit testing framework
- **pytest-qt**: PySide6 testing utilities

### Optional/Future
- **Pillow**: Image processing (product photos)
- **matplotlib/seaborn**: Charts & graphs (reports)
- **reportlab**: PDF generation (advanced receipts)

---

## 📦 Deployment Files (when ready)

```
📁 release/                         ⏳ Production build
├── minimarket.exe                  → PyInstaller bundled app
├── config.ini                      → User-editable config (not .py)
├── minimarket.sqlite3              → Production database
├── backups/                        → Auto-backup folder
├── logs/                           → Application logs
└── README.txt                      → End-user instructions
```

### Build Script (future)
```powershell
# build.bat
pyinstaller --onefile --windowed --name minimarket main.py
```

---

## 🔐 Security Considerations

### ✅ Implemented
- Password hashing (bcrypt)
- SQL injection prevention (ORM)
- .gitignore untuk sensitive files

### ⏳ TODO
- Session timeout
- Audit logging
- Role-based access control (RBAC) enforcement
- Encrypted config for production
- Database encryption at rest (optional)

---

## 📈 Performance Notes

### Database Optimization
- Indexes sudah dibuat untuk query sering (user, product, transaction)
- Foreign keys diaktifkan (data integrity)
- SQLite cukup untuk single-outlet (tested up to 100k records)
- Untuk multi-outlet terpusat: migrate ke PostgreSQL

### UI Responsiveness
- Async/threading untuk long operations (reports, backup)
- Lazy loading untuk large datasets
- Pagination untuk table views

---

## 🚀 Roadmap

### v0.1.0 - MVP (current)
- ✅ Database schema
- ✅ Project skeleton
- ⏳ Auth module
- ⏳ Product CRUD
- ⏳ POS (cash only)
- ⏳ Basic reports
- ⏳ Text receipt

### v0.2.0 - Enhanced
- Multi-payment
- Customer management
- Stock alerts (Telegram)
- Thermal printer integration
- Import/Export CSV

### v0.3.0 - Advanced
- Refund/return
- Discount & promo
- Multi-outlet
- Advanced reports & charts
- Backup automation

### v1.0.0 - Production
- Full RBAC
- Audit logging
- Cloud sync (optional)
- Mobile app companion (optional)
- Hardware integration (barcode scanner, cash drawer)

---

## 📚 Documentation Index

| File                    | Audience     | Purpose                              |
|-------------------------|--------------|--------------------------------------|
| `README.md`             | End User     | Installation, usage, configuration   |
| `QUICKSTART.md`         | End User     | Quick setup guide                    |
| `DEVELOPMENT.md`        | Developer    | Coding guidelines, examples          |
| `MVP_CHECKLIST.md`      | Developer    | Implementation checklist             |
| `PROJECT_STRUCTURE.md`  | All          | Project overview (this file)         |
| `specs/POS_spec.md`     | Developer    | Detailed module specifications       |
| `db/schema.sql`         | Developer/DBA| Database schema reference            |

---

**Last Updated**: November 11, 2025  
**Version**: 0.1.0 (MVP in development)
