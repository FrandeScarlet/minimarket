# Changelog - POS Minimarket

Semua perubahan penting pada project ini akan didokumentasikan di file ini.

Format berdasarkan [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
dan project ini mengikuti [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### To Be Implemented (see MVP_CHECKLIST.md)
- Auth module (login UI, user management)
- Product CRUD & category management
- POS transaction (cash payment)
- Receipt printing (text format)
- Daily sales report
- Stock management & Telegram alerts

---

## [0.1.0] - 2025-11-11

### 🎉 Initial Release - Project Foundation

### Added
- **Project Structure**
  - Folder structure: `src/`, `db/`, `specs/`, `tests/`
  - `.gitignore` for Python projects
  
- **Database**
  - SQLite schema (`db/schema.sql`) with 19 tables
  - SQLAlchemy ORM models (`src/models.py`) - 14 models
  - Database initialization script (`create_db.py`)
  - Default seed data:
    - 3 roles: admin, kasir, executive
    - 1 default outlet
    - 1 default admin user (admin/admin123)
    - 1 default tax (PPN 10%)
  
- **Configuration**
  - `config.py` for app settings (DB, Telegram, Printer)
  - Support for environment variables
  
- **Application Entry Point**
  - `main.py` with basic PySide6 GUI window
  - Login button placeholder
  - Database connection check
  
- **Documentation**
  - `README.md` - User documentation & setup guide
  - `QUICKSTART.md` - Quick installation guide
  - `DEVELOPMENT.md` - Developer guidelines & examples
  - `MVP_CHECKLIST.md` - Implementation checklist
  - `PROJECT_STRUCTURE.md` - Project structure reference
  - `specs/POS_spec.md` - Detailed module specifications
  - `CHANGELOG.md` - This file
  
- **Dependencies** (`requirements.txt`)
  - PySide6 (GUI)
  - SQLAlchemy (ORM)
  - bcrypt (password hashing)
  - pandas, openpyxl (CSV/Excel)
  - python-telegram-bot (notifications)
  - python-escpos (thermal printer)
  - pytest, pytest-qt (testing)
  
- **Automation Scripts**
  - `setup.bat` - Windows auto-setup script
  - `run.bat` - Windows run application script
  
- **Testing**
  - Basic test structure (`tests/`)
  - `test_database.py` - Database connection tests
  - pytest configuration ready

### Database Schema Tables
1. `roles` - User roles
2. `outlets` - Store branches
3. `users` - Application users
4. `categories` - Product categories
5. `products` - Product catalog
6. `product_stocks` - Stock per outlet
7. `stock_movements` - Stock history
8. `transactions` - Sales transactions
9. `transaction_items` - Transaction line items
10. `payments` - Payment records (multi-payment support)
11. `customers` - Customer database
12. `customer_purchases` - Purchase history link
13. `shifts` - Cashier shifts
14. `cashier_activity` - Activity log
15. `discounts` - Discount definitions
16. `taxes` - Tax configurations
17. `refunds` - Refund records
18. `backups` - Backup metadata
19. `telegram_notifications` - Notification configs

### Technical Decisions
- **Database**: SQLite for simplicity (Windows desktop app)
- **Monetary values**: Stored as INTEGER (cents/smallest unit) to avoid floating point issues
- **Password**: bcrypt hashing with salt
- **Foreign keys**: Enabled in SQLite for referential integrity
- **ORM**: SQLAlchemy for database abstraction

### Known Limitations (to be fixed in next version)
- No actual login flow yet (placeholder UI only)
- No product management UI
- No POS transaction UI
- No reports
- No printer integration
- No Telegram integration

---

## Version History & Roadmap

### v0.1.0 (Current) - Foundation ✅
- Database schema & models
- Project structure
- Documentation
- Basic entry point

### v0.2.0 (Next) - Core Features 🚧
Target: Basic usable MVP
- Auth module (login, user management)
- Product CRUD
- POS transaction (cash only)
- Basic receipt printing
- Daily sales report
- Stock adjustment

### v0.3.0 - Enhanced Features 📋
- Multi-payment & split payment
- Customer management
- Low-stock Telegram alerts
- Thermal printer integration
- CSV/Excel import/export

### v0.4.0 - Advanced Features 📋
- Refund/return processing
- Discount & promo management
- Multi-outlet support
- Advanced reports & analytics
- Backup automation

### v1.0.0 - Production Ready 🎯
- Full RBAC implementation
- Audit logging
- Performance optimization
- Security hardening
- User manual & training materials

---

## Development Guidelines

### Commit Message Format
```
[TYPE] Brief description

BREAKING CHANGE: (if applicable)
- Details of breaking change

Body: Detailed description if needed

Closes: #issue-number
```

**Types**: 
- `[FEAT]` - New feature
- `[FIX]` - Bug fix
- `[DOCS]` - Documentation update
- `[TEST]` - Test additions/changes
- `[REFACTOR]` - Code refactoring
- `[CHORE]` - Build/tooling changes

### Version Bump Rules
- **MAJOR** (1.0.0): Breaking changes, major feature overhaul
- **MINOR** (0.x.0): New features, non-breaking
- **PATCH** (0.0.x): Bug fixes, small improvements

---

## Contributors

- Initial setup & foundation: [OpenAI Assistant]

---

**Note**: Untuk perubahan detail per modul, lihat commit history dan dokumentasi modul di `src/<module>/`.
