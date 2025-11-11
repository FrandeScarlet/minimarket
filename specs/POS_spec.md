# POS Minimarket — Spesifikasi Modul dan Rencana Implementasi

Dokumen ini merinci modul-modul aplikasi POS (Point of Sale) sederhana untuk minimarket yang berjalan di Windows menggunakan Python. Tujuan: membagi pekerjaan per modul, menentukan acceptance criteria, dependensi, dan langkah berikutnya.

## Ringkasan fitur utama
- Multi-user dengan 3 role: kasir, admin, executive
- Transaksi penjualan: keranjang, diskon, pajak (PPN), total, kembalian otomatis
- Manajemen produk: CRUD (nama, harga, stok, kategori)
- Manajemen stok: stok masuk/keluar, riwayat, notifikasi stok menipis (Telegram)
- Manajemen pelanggan: data pelanggan, riwayat pembelian
- Manajemen kasir/karyawan: multi user, login/logout, shift, laporan aktivitas
- Pembayaran multi-mode: tunai, kartu, QRIS, e-wallet, split-payment
- Laporan & analisis: harian/mingguan/bulanan, produk terlaris, stok
- Pengaturan pajak & diskon (per item / per transaksi)
- Retur/refund
- Integrasi printer thermal (struk ESC/POS)
- Multi-outlet/cabang
- Import/Export data (CSV/Excel)
- Backup & restore database

---

## Teknologi & library yang direkomendasikan
- Bahasa: Python 3.10+ (Windows)
- GUI: PySide6 (atau PyQt5) — aplikasi desktop native, lisensi PySide lebih ramah
- Database lokal: SQLite (awal) — mudah backup/restore; opsi naik ke PostgreSQL untuk multi-outlet terpusat
- ORM: SQLAlchemy (atau Peewee untuk yang ringan)
- Password hashing: bcrypt (package: bcrypt)
- Printer thermal: python-escpos (atau fallback ke raw ESC/POS via pyserial)
- Telegram notifications: python-telegram-bot
- CSV/Excel: pandas + openpyxl
- Export/Backup: salin file DB (.sqlite) atau SQL dump
- Testing: pytest

Alasan: stack ini mudah di-setup di Windows, mempunyai ekosistem lengkap untuk integrasi (printer, telegram, excel).

---

## Struktur modul (untuk implementasi satu-per-satu)
Setiap modul akan memiliki:
- Deskripsi fitur
- Model DB terkait
- API/internal function signatures atau GUI screens
- Acceptance criteria (to pass)
- Edge cases & notes

1) Auth & User Management (role: admin, kasir, executive)
   - Fungsi: login/logout, CRUD user, list roles, reset password, change role
   - DB: `users`, `roles`, `shifts`, `cashier_activity`
   - Acceptance: login sukses/failed dengan pesan, enforce role-based access control (RBAC)
   - Notes: hash password dengan bcrypt; simpan last_login

2) Produk & Kategori
   - Fungsi: tambah/ubah/hapus produk, foto produk, manajemen kategori
   - DB: `products`, `categories`, `product_stocks`
   - Acceptance: produk dapat dicari (by name, sku, barcode), harga dan stok tampil
   - Notes: harga simpan dalam integer (cents) untuk menghindari float

3) Stok & Riwayat Stok
   - Fungsi: stok masuk/keluar, adjustment, pencatatan riwayat, notifikasi low-stock
   - DB: `stock_movements`, `product_stocks`
   - Acceptance: stok terupdate saat transaksi; notifikasi telegram terkirim saat threshold
   - Notes: semua perubahan stok harus tercatat (actor, reason, reference)

4) Transaksi Penjualan (POS)
   - Fungsi: tambah ke keranjang, edit qty, diskon per item/atau per transaksi, apply tax, hitung subtotal/total, pembayaran split, cetak struk
   - DB: `transactions`, `transaction_items`, `payments`
   - Acceptance: total dan kembalian benar; stok dikurangi atomik; cetak struk dapat dipicu
   - Notes: transaksi harus atomic; gunakan transaction block DB dan rollback saat gagal

5) Pembayaran & Split Payment
   - Fungsi: metode pembayaran multiple, split by amount/method
   - DB: `payments`
   - Acceptance: jumlah total pembayaran == total transaksi; kembalian dihitung dari tunai portion

6) Refund / Retur
   - Fungsi: buat nota retur, update stok, buat entry refund
   - DB: `refunds`, `stock_movements`
   - Acceptance: refund menambah stok jika barang dikembalikan; audit trail tersedia

7) Pelanggan & Loyalty
   - Fungsi: CRUD pelanggan, simpan kontak/ulang tahun, riwayat pembelian
   - DB: `customers`, `customer_purchases`
   - Acceptance: riwayat pembelian dapat ditarik per pelanggan

8) Shift & Aktivitas Kasir
   - Fungsi: open/close shift, catat starting/ending cash, laporan aktivitas
   - DB: `shifts`, `cashier_activity`
   - Acceptance: shift tidak overlap per user, laporan ringkasan shift tersedia

9) Laporan & Analisis
   - Fungsi: laporan harian/mingguan/bulanan, produk terlaris, stok kritis
   - Acceptance: query berjalan cepat untuk dataset kecil-menengah; eksport CSV/Excel

10) Integrasi Printer Thermal
    - Fungsi: cetak struk transaksi, tes koneksi
    - Acceptance: cetak sukses ke printer ESC/POS; fallback log jika gagal

11) Integrasi Telegram (stok menipis)
    - Fungsi: kirim notifikasi ke chat id ketika stok < threshold
    - Acceptance: pesan berisi product, outlet, current stock

12) Import/Export, Backup & Restore
    - Fungsi: import produk/customers via CSV/Excel; export laporan; backup DB (file copy), restore from backup
    - Acceptance: format CSV/Excel terdefinisi; restore memulihkan DB ke kondisi backup

---

## Format kerja: per modul checklist minimal (MVP)
Untuk tiap modul, sediakan file implementasi / test minimal:
- Model DB (DDL / ORM model)
- CRUD minimal API / GUI screen
- Unit test (happy path)
- Demo manual steps

---

## Acceptance criteria umum untuk MVP (fase 1)
- User dengan role kasir dapat login dan melakukan transaksi sederhana (scan/add product, bayar tunai, cetak struk)
- Stok berkurang otomatis setelah transaksi selesai
- Admin dapat membuat produk dan user
- Laporan penjualan per hari dapat diekspor CSV
- Database backup & restore sederhana bekerja (copy / replace file)

---

## Keamanan & praktik baik
- Hash password (bcrypt) + salt
- Simpan minimal data sensitif; enkripsi konfigurasi (token Telegram, API keys) di file konfigurasi lokal atau Windows Credential Store
- Validasi input di client & server layer
- Atomic DB transactions untuk operasi stok dan transaksi

---

## Next steps (prioritas implementasi)
1. Setup project skeleton: virtualenv, requirements.txt, basic PySide6 window, DB connection (sqlite)
2. DB schema & migration (skrip SQL) — `db/schema.sql`
3. Implement auth + user management
4. Implement product CRUD + product listing
5. Implement POS UI: cart, payment (cash only first), stock decrement
6. Add printing & backup

---

## File terkait yang akan dibuat sekarang
- `db/schema.sql` — skema database (DDL)
- `specs/POS_spec.md` (file ini)

---

## Catatan asumsi
- Aplikasi awal menggunakan SQLite lokal untuk kemudahan instalasi di desktop Windows.
- Mata uang disimpan sebagai integer (mis. 1.000 rupiah = 100000 cents) atau skala yang disepakati — spesifikasi implementation: simpan dalam *cents* (integer) atau smallest currency unit.
- Pengiriman notifikasi Telegram membutuhkan konfigurasi `BOT_TOKEN` dan `CHAT_ID`.

Jika setuju dengan rencana ini, saya akan melanjutkan dengan membuat file `db/schema.sql` berisi DDL lengkap (SQLite) dan update todo list.
