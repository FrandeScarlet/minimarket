# Development Guide - POS Minimarket

Panduan untuk developer yang akan melanjutkan implementasi modul-modul POS.

## 📂 Struktur Project (Current State)

```
minimarket/
├── config.py               ✅ Konfigurasi aplikasi (DB, Telegram, Printer, dll)
├── create_db.py            ✅ Script inisialisasi database + seed data
├── main.py                 ✅ Entry point aplikasi GUI
├── requirements.txt        ✅ Python dependencies
├── README.md              ✅ Dokumentasi user
├── setup.bat              ✅ Windows batch untuk auto-setup
├── run.bat                ✅ Windows batch untuk run aplikasi
├── .gitignore             ✅
│
├── db/
│   └── schema.sql         ✅ DDL lengkap (SQLite)
│
├── src/
│   ├── __init__.py        ✅
│   ├── db_manager.py      ✅ SQLAlchemy engine, session factory
│   ├── models.py          ✅ ORM models lengkap (User, Product, Transaction, dll)
│   │
│   ├── auth/              ⏳ TODO: Authentication & user management
│   ├── pos/               ⏳ TODO: Point of Sale / Transaksi
│   ├── products/          ⏳ TODO: Product & Category CRUD
│   ├── stock/             ⏳ TODO: Stock management & notifications
│   ├── customers/         ⏳ TODO: Customer management
│   ├── reports/           ⏳ TODO: Laporan & analytics
│   ├── payments/          ⏳ TODO: Payment processing
│   ├── integrations/      ⏳ TODO: Printer, Telegram, dll
│   └── utils/             ⏳ TODO: Helper functions
│
├── specs/
│   └── POS_spec.md        ✅ Spesifikasi lengkap semua modul
│
└── tests/
    ├── __init__.py        ✅
    ├── test_database.py   ✅ Basic DB tests
    └── test_*.py          ⏳ TODO: Tests per modul
```

## 🚀 Quick Start untuk Development

### 1. Setup environment (first time only)
```powershell
# Option A: Otomatis dengan batch file
.\setup.bat

# Option B: Manual
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python create_db.py
```

### 2. Aktivasi environment (setiap kali dev)
```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Run aplikasi
```powershell
# Option A: dengan batch
.\run.bat

# Option B: manual
python main.py
```

### 4. Run tests
```powershell
pytest tests/ -v
```

## 📝 Workflow Implementasi Modul Baru

### Template untuk modul baru

Misalnya membuat modul `auth`:

1. **Buat folder & file struktur:**
```
src/auth/
├── __init__.py
├── models.py      # (optional) jika ada model tambahan di luar src/models.py
├── service.py     # Business logic
├── ui.py          # GUI widgets/windows
└── utils.py       # Helper functions
```

2. **Contoh `auth/service.py`:**
```python
# -*- coding: utf-8 -*-
"""
auth/service.py - Authentication service
"""
import bcrypt
from src.db_manager import get_session
from src.models import User
from datetime import datetime

class AuthService:
    def __init__(self):
        self.current_user = None
    
    def login(self, username: str, password: str) -> bool:
        """Authenticate user with username and password"""
        session = get_session()
        try:
            user = session.query(User).filter_by(
                username=username,
                is_active=True
            ).first()
            
            if not user:
                return False
            
            # Verify password
            if bcrypt.checkpw(password.encode('utf-8'), 
                             user.password_hash.encode('utf-8')):
                # Update last login
                user.last_login = datetime.now()
                session.commit()
                self.current_user = user
                return True
            
            return False
        finally:
            session.close()
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def get_current_user(self):
        """Get currently logged in user"""
        return self.current_user
    
    def has_permission(self, permission: str) -> bool:
        """Check if current user has specific permission"""
        if not self.current_user:
            return False
        return self.current_user.role.name == 'admin'  # Simplified
```

3. **Contoh `auth/ui.py`:**
```python
# -*- coding: utf-8 -*-
"""
auth/ui.py - Login UI
"""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, 
                               QPushButton, QLabel, QMessageBox)
from PySide6.QtCore import Qt
from .service import AuthService

class LoginDialog(QDialog):
    def __init__(self, auth_service: AuthService, parent=None):
        super().__init__(parent)
        self.auth_service = auth_service
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Login - POS Minimarket")
        self.setModal(True)
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Login")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
        
        self.setLayout(layout)
        
        # Enter key triggers login
        self.password_input.returnPressed.connect(self.handle_login)
    
    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Username dan password harus diisi")
            return
        
        if self.auth_service.login(username, password):
            QMessageBox.information(self, "Success", 
                f"Login berhasil! Selamat datang, {self.auth_service.current_user.full_name}")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Username atau password salah")
            self.password_input.clear()
            self.username_input.setFocus()
```

4. **Contoh test `tests/test_auth.py`:**
```python
import pytest
from src.auth.service import AuthService

def test_login_success():
    auth = AuthService()
    # Default admin: username='admin', password='admin123'
    assert auth.login('admin', 'admin123') == True
    assert auth.current_user is not None
    assert auth.current_user.username == 'admin'

def test_login_failed():
    auth = AuthService()
    assert auth.login('admin', 'wrongpassword') == False
    assert auth.current_user is None

def test_logout():
    auth = AuthService()
    auth.login('admin', 'admin123')
    auth.logout()
    assert auth.current_user is None
```

5. **Integrate ke `main.py`:**
```python
from src.auth.service import AuthService
from src.auth.ui import LoginDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.auth_service = AuthService()
        self.init_ui()
    
    def show_login(self):
        dialog = LoginDialog(self.auth_service, self)
        if dialog.exec():
            # Login success, show main app
            self.show_main_interface()
```

## 🧪 Testing Guidelines

### Run specific test file
```powershell
pytest tests/test_auth.py -v
```

### Run with coverage
```powershell
pytest --cov=src tests/
```

### Run specific test function
```powershell
pytest tests/test_auth.py::test_login_success -v
```

## 🔧 Common Tasks

### Menambah tabel baru ke database

1. Edit `db/schema.sql` - tambahkan DDL
2. Edit `src/models.py` - tambahkan ORM model
3. Drop dan recreate database:
```powershell
python create_db.py  # akan prompt overwrite
```

### Update password hash default user
```python
import bcrypt
password = 'newpassword'
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(hashed.decode('utf-8'))
```

### Query database langsung (debug)
```powershell
# Install sqlite3 CLI atau gunakan Python:
python -c "import sqlite3; conn = sqlite3.connect('minimarket.sqlite3'); cursor = conn.cursor(); cursor.execute('SELECT * FROM users'); print(cursor.fetchall())"
```

### Reset database dengan data seed custom
Edit `create_db.py`, tambahkan insert statements di bagian seed data.

## 📊 Database Schema Quick Reference

### Tabel Utama & Relationships

```
roles (id, name, permissions)
  └─→ users.role_id

outlets (id, name, address, phone)
  └─→ users.outlet_id
  └─→ transactions.outlet_id
  └─→ product_stocks.outlet_id

users (id, username, password_hash, role_id, outlet_id, ...)
  └─→ transactions.user_id
  └─→ shifts.user_id

categories (id, name, parent_id)
  └─→ products.category_id

products (id, sku, barcode, name, price_cents, ...)
  └─→ product_stocks.product_id
  └─→ transaction_items.product_id

transactions (id, uuid, user_id, outlet_id, total_cents, ...)
  └─→ transaction_items.transaction_id
  └─→ payments.transaction_id

customers (id, code, name, phone, email, ...)
  └─→ transactions.customer_id
```

### Monetary Values
**PENTING**: Semua nilai uang disimpan sebagai INTEGER dalam satuan terkecil (cents).
- Rp 10.000 → `1000000` cents
- Rp 500 → `50000` cents

Gunakan helper functions untuk konversi:
```python
def rupiah_to_cents(rupiah: float) -> int:
    return int(rupiah * 100)

def cents_to_rupiah(cents: int) -> float:
    return cents / 100
```

## 🎨 UI/UX Guidelines

### PySide6 Best Practices
- Gunakan `QMainWindow` untuk window utama
- Gunakan `QDialog` untuk modal dialogs
- Gunakan `QTableWidget` atau `QTableView` untuk list data
- Gunakan signals & slots untuk event handling
- Implement dark/light theme support (optional)

### Layout Patterns
```python
# Form layout
from PySide6.QtWidgets import QFormLayout
layout = QFormLayout()
layout.addRow("Label:", widget)

# Grid layout untuk POS
from PySide6.QtWidgets import QGridLayout
layout = QGridLayout()
layout.addWidget(widget, row, col, rowspan, colspan)

# Splitter untuk resizable panels
from PySide6.QtWidgets import QSplitter
splitter = QSplitter(Qt.Orientation.Horizontal)
splitter.addWidget(left_widget)
splitter.addWidget(right_widget)
```

## 🔐 Security Checklist

- ✅ Password hashing dengan bcrypt (NEVER store plaintext)
- ⏳ TODO: Input validation & sanitization
- ⏳ TODO: SQL injection prevention (use ORM, not raw SQL)
- ⏳ TODO: Session timeout implementation
- ⏳ TODO: Audit log untuk sensitive operations
- ⏳ TODO: Role-based access control (RBAC) enforcement

## 📦 Deployment Checklist (untuk production)

- [ ] Change default admin password
- [ ] Configure Telegram bot credentials
- [ ] Configure printer device
- [ ] Test backup/restore procedures
- [ ] Setup automatic backup schedule
- [ ] Test all critical paths (login, transaction, payment, receipt)
- [ ] Load test dengan data realistis
- [ ] Create user manual/training materials
- [ ] Setup error logging & monitoring

## 🐛 Debugging Tips

### Enable SQL logging
Edit `src/db_manager.py`:
```python
engine = create_engine(
    config.DB_URI,
    echo=True  # Set to True untuk debug
)
```

### Qt debug messages
```python
import sys
from PySide6.QtCore import qInstallMessageHandler, QtMsgType

def qt_message_handler(mode, context, message):
    print(f"Qt {mode}: {message}")

qInstallMessageHandler(qt_message_handler)
```

### Database inspector (visual)
Install DB Browser for SQLite: https://sqlitebrowser.org/
Open `minimarket.sqlite3` untuk inspect data.

## 📚 Resources

- **PySide6 Docs**: https://doc.qt.io/qtforpython-6/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **Python Telegram Bot**: https://python-telegram-bot.readthedocs.io/
- **python-escpos**: https://python-escpos.readthedocs.io/

## ✅ Next Implementation Priority

Urutan yang disarankan:
1. **Auth Module** (login UI, session management) — PRIORITAS TINGGI
2. **Product Module** (CRUD produk, kategori)
3. **POS Module** (keranjang, cash payment, print receipt)
4. **Stock Module** (stock movements, low-stock alerts)
5. **Reports Module** (laporan penjualan, export CSV)
6. **Multi-payment** (split payment, e-wallet, QRIS)
7. **Customer Module** (loyalty, riwayat)
8. **Advanced features** (refund, multi-outlet, backup automation)

Lihat `specs/POS_spec.md` untuk detail implementasi tiap modul.

---

**Happy coding!** 🚀
