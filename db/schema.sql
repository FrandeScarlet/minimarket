-- Schema SQL untuk POS Minimarket (SQLite)
-- Catatan: simpan monetary values sebagai INTEGER (satuan: cents)
-- Aktifkan foreign keys saat menjalankan: PRAGMA foreign_keys = ON;

PRAGMA foreign_keys = ON;

-- roles
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE, -- 'admin', 'kasir', 'executive'
    permissions TEXT, -- optional JSON or comma-separated permissions
    created_at DATETIME DEFAULT (datetime('now'))
);

-- outlets (multi-cabang)
CREATE TABLE IF NOT EXISTS outlets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT,
    phone TEXT,
    created_at DATETIME DEFAULT (datetime('now'))
);

-- users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    full_name TEXT,
    email TEXT,
    phone TEXT,
    outlet_id INTEGER REFERENCES outlets(id) ON DELETE SET NULL,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT (datetime('now')),
    last_login DATETIME
);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- categories
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    created_at DATETIME DEFAULT (datetime('now'))
);

-- products
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT UNIQUE,
    barcode TEXT UNIQUE,
    name TEXT NOT NULL,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    price_cents INTEGER NOT NULL, -- store price in cents
    cost_cents INTEGER,
    alert_stock INTEGER DEFAULT 0, -- threshold for low stock notification
    track_stock INTEGER DEFAULT 1, -- 1=yes, 0=no
    description TEXT,
    created_at DATETIME DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku);

-- product_stocks per outlet
CREATE TABLE IF NOT EXISTS product_stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    outlet_id INTEGER NOT NULL REFERENCES outlets(id) ON DELETE CASCADE,
    stock INTEGER NOT NULL DEFAULT 0,
    updated_at DATETIME DEFAULT (datetime('now')),
    UNIQUE(product_id, outlet_id)
);
CREATE INDEX IF NOT EXISTS idx_product_stocks_product ON product_stocks(product_id);

-- stock_movements (history of stock in/out)
CREATE TABLE IF NOT EXISTS stock_movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    outlet_id INTEGER NOT NULL REFERENCES outlets(id) ON DELETE CASCADE,
    change_qty INTEGER NOT NULL, -- positive for in, negative for out
    reason TEXT, -- e.g., 'sale', 'purchase', 'adjustment', 'return'
    reference TEXT, -- e.g., transaction id or invoice
    created_by INTEGER REFERENCES users(id),
    created_at DATETIME DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_stock_movements_prod ON stock_movements(product_id);

-- transactions
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT UNIQUE NOT NULL,
    outlet_id INTEGER REFERENCES outlets(id),
    user_id INTEGER REFERENCES users(id),
    customer_id INTEGER REFERENCES customers(id),
    subtotal_cents INTEGER NOT NULL,
    discount_cents INTEGER DEFAULT 0,
    tax_cents INTEGER DEFAULT 0,
    total_cents INTEGER NOT NULL,
    paid_cents INTEGER DEFAULT 0,
    change_cents INTEGER DEFAULT 0,
    status TEXT DEFAULT 'completed', -- 'pending', 'completed', 'refunded', 'cancelled'
    payment_summary TEXT, -- JSON or serialized
    created_at DATETIME DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_transactions_uuid ON transactions(uuid);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(created_at);

-- transaction_items
CREATE TABLE IF NOT EXISTS transaction_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    price_cents INTEGER NOT NULL,
    qty INTEGER NOT NULL,
    discount_cents INTEGER DEFAULT 0,
    tax_cents INTEGER DEFAULT 0,
    total_cents INTEGER NOT NULL -- price*qty - discount + tax
);
CREATE INDEX IF NOT EXISTS idx_tx_items_tx ON transaction_items(transaction_id);

-- payments (one or multiple per transaction -> support split payment)
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    method TEXT NOT NULL, -- 'cash','card','qris','e-wallet', etc
    amount_cents INTEGER NOT NULL,
    details TEXT, -- e.g., card last4, provider, or raw json
    created_at DATETIME DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_payments_tx ON payments(transaction_id);

-- refunds / returns
CREATE TABLE IF NOT EXISTS refunds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER REFERENCES transactions(id),
    amount_cents INTEGER NOT NULL,
    reason TEXT,
    processed_by INTEGER REFERENCES users(id),
    created_at DATETIME DEFAULT (datetime('now'))
);

-- customers
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    birthday DATE,
    notes TEXT,
    created_at DATETIME DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_customers_phone ON customers(phone);

-- customer_purchases (link customer -> transactions history)
CREATE TABLE IF NOT EXISTS customer_purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    created_at DATETIME DEFAULT (datetime('now'))
);

-- discounts table (optional, for named discounts)
CREATE TABLE IF NOT EXISTS discounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL, -- 'percentage' or 'fixed'
    value REAL NOT NULL, -- percent (e.g., 10.0) or fixed in cents if type='fixed'
    applies_to TEXT DEFAULT 'transaction' -- 'item' or 'transaction'
);

-- taxes
CREATE TABLE IF NOT EXISTS taxes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rate REAL NOT NULL, -- percent e.g., 10.0 for 10%
    auto_apply INTEGER DEFAULT 1
);

-- shifts
CREATE TABLE IF NOT EXISTS shifts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    outlet_id INTEGER REFERENCES outlets(id),
    start_at DATETIME DEFAULT (datetime('now')),
    end_at DATETIME,
    starting_cash_cents INTEGER DEFAULT 0,
    ending_cash_cents INTEGER,
    note TEXT
);

-- cashier activity log
CREATE TABLE IF NOT EXISTS cashier_activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    action TEXT NOT NULL,
    details TEXT,
    created_at DATETIME DEFAULT (datetime('now'))
);

-- backups metadata
CREATE TABLE IF NOT EXISTS backups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT NOT NULL,
    note TEXT,
    created_at DATETIME DEFAULT (datetime('now'))
);

-- telegram notifications config
CREATE TABLE IF NOT EXISTS telegram_notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id TEXT NOT NULL,
    enabled INTEGER DEFAULT 1,
    product_id INTEGER REFERENCES products(id), -- optional single-product watch
    outlet_id INTEGER REFERENCES outlets(id),
    threshold INTEGER DEFAULT 0,
    last_sent_at DATETIME
);

-- optional: product images metadata
CREATE TABLE IF NOT EXISTS product_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    file_path TEXT NOT NULL,
    created_at DATETIME DEFAULT (datetime('now'))
);

-- Indexes helpful untuk laporan
CREATE INDEX IF NOT EXISTS idx_transactions_outlet_date ON transactions(outlet_id, created_at);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);

-- Example trigger (optional) untuk menjaga product_stocks saat insert stock_movements
-- NOTE: triggers can be adapted to your application logic; many prefer update via app code

CREATE TRIGGER IF NOT EXISTS trg_stock_movements_after_insert
AFTER INSERT ON stock_movements
BEGIN
    -- update product_stocks table atomically
    UPDATE product_stocks
    SET stock = stock + NEW.change_qty,
        updated_at = datetime('now')
    WHERE product_id = NEW.product_id AND outlet_id = NEW.outlet_id;

    -- if no row, insert one
    INSERT INTO product_stocks(product_id, outlet_id, stock, updated_at)
    SELECT NEW.product_id, NEW.outlet_id, NEW.change_qty, datetime('now')
    WHERE (SELECT changes() ) IS NOT NULL
      AND NOT EXISTS(SELECT 1 FROM product_stocks WHERE product_id = NEW.product_id AND outlet_id = NEW.outlet_id);
END;

-- End of schema
