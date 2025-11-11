# MVP Implementation Checklist

Checklist untuk implementasi Minimum Viable Product (MVP) POS Minimarket.
Target: Aplikasi POS yang dapat digunakan untuk transaksi dasar kasir.

## ✅ Phase 0: Foundation (COMPLETED)
- [x] Project structure & folders
- [x] Database schema (SQLite)
- [x] ORM models (SQLAlchemy)
- [x] Configuration file
- [x] Database initialization script
- [x] Basic GUI entry point
- [x] Requirements.txt
- [x] README & documentation
- [x] Basic tests setup
- [x] Setup & run scripts (Windows batch)

## 🔄 Phase 1: Core POS Features (MVP PRIORITY)

### 1.1 Authentication & User Management
- [ ] `src/auth/service.py` — AuthService class
  - [ ] login(username, password) → bool
  - [ ] logout()
  - [ ] get_current_user() → User
  - [ ] change_password(old, new) → bool
  - [ ] has_permission(permission) → bool

- [ ] `src/auth/ui.py` — Login UI
  - [ ] LoginDialog (username, password fields)
  - [ ] Error handling & validation
  - [ ] Remember user session in MainWindow

- [ ] Test: `tests/test_auth.py`
  - [ ] test_login_success
  - [ ] test_login_failed
  - [ ] test_logout
  - [ ] test_password_change

**Acceptance Criteria:**
- Admin dapat login dengan username/password
- Password salah menampilkan error
- Session user tersimpan setelah login
- Logout clear session

---

### 1.2 Product Management
- [ ] `src/products/service.py` — ProductService
  - [ ] get_all_products() → List[Product]
  - [ ] get_product_by_id(id) → Product
  - [ ] search_products(query) → List[Product]
  - [ ] create_product(data) → Product
  - [ ] update_product(id, data) → bool
  - [ ] delete_product(id) → bool
  - [ ] get_categories() → List[Category]

- [ ] `src/products/ui.py` — Product CRUD UI
  - [ ] ProductListWindow (table view, search bar)
  - [ ] ProductFormDialog (add/edit form)
  - [ ] Category dropdown/selector

- [ ] Test: `tests/test_products.py`
  - [ ] test_create_product
  - [ ] test_update_product
  - [ ] test_delete_product
  - [ ] test_search_products

**Acceptance Criteria:**
- Admin dapat melihat list produk
- Admin dapat tambah produk baru (nama, harga, stok, kategori)
- Admin dapat edit & hapus produk
- Search produk by nama/SKU/barcode

---

### 1.3 POS / Transaction (Cash Only MVP)
- [ ] `src/pos/service.py` — POSService
  - [ ] Cart class (add_item, remove_item, update_qty, clear)
  - [ ] calculate_subtotal() → int
  - [ ] calculate_tax(subtotal) → int
  - [ ] calculate_total(subtotal, discount, tax) → int
  - [ ] process_cash_payment(total, paid) → change
  - [ ] save_transaction(cart, payments) → Transaction
  - [ ] update_stock_after_sale(cart) → bool

- [ ] `src/pos/ui.py` — POS UI
  - [ ] POSWindow
    - [ ] Product search/scan input
    - [ ] Cart display (table: product, qty, price, subtotal)
    - [ ] Total, Tax, Discount display
    - [ ] Cash payment input
    - [ ] Change display
    - [ ] Checkout button
    - [ ] Clear cart button
  - [ ] Receipt preview/print dialog (text format)

- [ ] Test: `tests/test_pos.py`
  - [ ] test_add_to_cart
  - [ ] test_remove_from_cart
  - [ ] test_calculate_total
  - [ ] test_cash_payment
  - [ ] test_save_transaction
  - [ ] test_stock_decrease

**Acceptance Criteria:**
- Kasir dapat scan/pilih produk → masuk keranjang
- Kasir dapat edit qty atau hapus item dari keranjang
- Total otomatis dihitung (subtotal + tax - discount)
- Input jumlah bayar tunai → hitung kembalian
- Transaksi tersimpan ke DB dengan status "completed"
- Stok produk berkurang otomatis
- Receipt dapat dicetak/preview (format teks)

---

### 1.4 Receipt Printing (Basic Text)
- [ ] `src/integrations/printer.py` — PrinterService
  - [ ] generate_receipt_text(transaction) → str
  - [ ] print_receipt(transaction) → bool (fallback: save to file)

- [ ] Format receipt:
  ```
  ========================================
  POS MINIMARKET
  Outlet: [nama]
  Kasir: [nama kasir]
  Tanggal: [datetime]
  ========================================
  [Produk]               [Qty]    [Total]
  ----------------------------------------
  Item 1                  2x     Rp 10.000
  Item 2                  1x     Rp 5.000
  ----------------------------------------
  Subtotal:                      Rp 15.000
  Pajak (10%):                   Rp 1.500
  Diskon:                        Rp 0
  ========================================
  TOTAL:                         Rp 16.500
  Bayar:                         Rp 20.000
  Kembali:                       Rp 3.500
  ========================================
  Terima kasih!
  ```

**Acceptance Criteria:**
- Receipt text ter-generate dengan format rapi
- Dapat disimpan ke file .txt jika printer belum tersedia
- (Optional) Print ke printer thermal jika sudah dikonfigurasi

---

## 📊 Phase 2: Reports & Admin Features

### 2.1 Daily Sales Report
- [ ] `src/reports/service.py` — ReportService
  - [ ] get_daily_sales(date) → summary
  - [ ] get_sales_by_range(start, end) → List[Transaction]
  - [ ] export_to_csv(transactions, path) → bool

- [ ] `src/reports/ui.py` — Report UI
  - [ ] DailySalesDialog (date picker, summary display)
  - [ ] Export to CSV button

**Acceptance Criteria:**
- Admin dapat pilih tanggal → lihat total penjualan
- Export laporan ke CSV

---

### 2.2 Stock Management
- [ ] `src/stock/service.py` — StockService
  - [ ] get_stock_by_product(product_id, outlet_id) → int
  - [ ] add_stock(product_id, outlet_id, qty, reason) → bool
  - [ ] get_low_stock_products(threshold) → List[Product]
  - [ ] send_low_stock_alert(product) → bool

- [ ] UI: Stock adjustment form
- [ ] Integration: Telegram notification untuk low stock

**Acceptance Criteria:**
- Admin dapat tambah stok (stock in)
- Notifikasi Telegram terkirim saat stok < threshold

---

### 2.3 User Management (Admin Panel)
- [ ] `src/auth/admin_ui.py` — User management UI
  - [ ] UserListWindow
  - [ ] UserFormDialog (create/edit user, assign role)

**Acceptance Criteria:**
- Admin dapat CRUD user
- Admin dapat assign role ke user

---

## 🚀 Phase 3: Advanced Features (Post-MVP)

### 3.1 Multi-Payment & Split Payment
- [ ] Support multiple payment methods (cash, card, e-wallet, QRIS)
- [ ] Split payment UI & logic

### 3.2 Customer Loyalty
- [ ] Customer CRUD
- [ ] Purchase history tracking
- [ ] Birthday & promo alerts

### 3.3 Discount & Promo
- [ ] Discount per item
- [ ] Discount per transaction
- [ ] Promo code system

### 3.4 Refund / Return
- [ ] Refund UI
- [ ] Stock adjustment on return

### 3.5 Multi-Outlet
- [ ] Outlet CRUD
- [ ] Stock per outlet tracking
- [ ] Consolidated reports

### 3.6 Advanced Integrations
- [ ] Thermal printer (ESC/POS)
- [ ] Barcode scanner hardware
- [ ] Cloud backup (optional)

### 3.7 Import/Export
- [ ] Import products from CSV/Excel
- [ ] Import customers from CSV/Excel
- [ ] Bulk data operations

### 3.8 Backup & Restore Automation
- [ ] Scheduled automatic backup
- [ ] Restore from backup UI
- [ ] Backup encryption (optional)

---

## 🎯 MVP Definition of Done

**Minimum requirements untuk MVP siap digunakan:**

1. ✅ Database setup & seed data
2. ⏳ User dapat login (role: kasir atau admin)
3. ⏳ Admin dapat CRUD produk
4. ⏳ Kasir dapat melakukan transaksi:
   - Tambah produk ke keranjang
   - Hitung total + pajak
   - Input bayar tunai
   - Simpan transaksi
   - Cetak/preview receipt
   - Stok berkurang otomatis
5. ⏳ Admin dapat lihat laporan penjualan harian
6. ⏳ Admin dapat tambah stok produk
7. ⏳ Basic error handling & validation

**Estimated Time:**
- Phase 1.1 (Auth): 1-2 hari
- Phase 1.2 (Products): 1-2 hari
- Phase 1.3 (POS): 2-3 hari
- Phase 1.4 (Receipt): 0.5 hari
- **Total MVP: ~1 minggu full-time development**

---

## 📝 Implementation Order (Recommended)

1. **Auth Module** (login UI → dapat mulai test dengan user role)
2. **Product Module** (agar ada data produk untuk transaksi)
3. **POS Module** (core feature, paling kompleks)
4. **Receipt Printing** (finalisasi transaksi)
5. **Reports** (monitoring penjualan)
6. **Stock Management** (maintenance stok)
7. Advanced features (iterasi berikutnya)

---

## 🧪 Testing Strategy

### Unit Tests (pytest)
- Test semua service functions (auth, product, pos, stock)
- Mock DB untuk isolasi

### Integration Tests
- Test flow lengkap: login → add product → do transaction → check stock

### Manual Testing
- Test dengan data realistis (10+ products, 50+ transactions)
- Test edge cases: stok habis, payment insufficient, dll

### User Acceptance Testing (UAT)
- Test dengan real kasir & admin user
- Gather feedback & iterate

---

## 🎉 Launch Checklist

- [ ] All MVP features tested & working
- [ ] Default admin password changed
- [ ] Sample products & categories loaded
- [ ] Training materials prepared (user manual)
- [ ] Backup procedure documented & tested
- [ ] On-site support plan ready
- [ ] Rollback plan if issues occur

---

**Good luck with implementation!** 🚀

Untuk memulai, jalankan:
```powershell
.\setup.bat
```

Lalu mulai implement Auth Module di `src/auth/` — lihat contoh di `DEVELOPMENT.md`.
