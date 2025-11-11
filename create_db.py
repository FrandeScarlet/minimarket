#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
create_db.py - Initialize the database schema for POS Minimarket
Run this script once to create the SQLite database from schema.sql
"""
import sqlite3
from pathlib import Path
import config

def create_database():
    """Create database from schema.sql"""
    schema_path = config.BASE_DIR / 'db' / 'schema.sql'
    db_path = config.DB_PATH
    
    if not schema_path.exists():
        print(f"❌ Schema file not found: {schema_path}")
        return False
    
    if db_path.exists():
        overwrite = input(f"⚠️  Database already exists at {db_path}. Overwrite? (y/N): ")
        if overwrite.lower() != 'y':
            print("Cancelled.")
            return False
        db_path.unlink()
    
    print(f"📦 Creating database at: {db_path}")
    
    try:
        conn = sqlite3.connect(str(db_path))
        conn.execute("PRAGMA foreign_keys = ON")
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        conn.executescript(schema_sql)
        conn.commit()
        
        # Insert default roles
        print("➕ Inserting default roles...")
        conn.execute("INSERT INTO roles (name, permissions) VALUES ('admin', 'all')")
        conn.execute("INSERT INTO roles (name, permissions) VALUES ('kasir', 'pos,sales')")
        conn.execute("INSERT INTO roles (name, permissions) VALUES ('executive', 'reports')")
        
        # Insert default outlet
        print("➕ Inserting default outlet...")
        conn.execute("INSERT INTO outlets (name, address, phone) VALUES ('Toko Pusat', 'Alamat Toko', '08123456789')")
        
        # Insert default admin user (password: admin123)
        # bcrypt hash of 'admin123'
        import bcrypt
        password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        print("➕ Inserting default admin user (username: admin, password: admin123)...")
        conn.execute(
            "INSERT INTO users (username, password_hash, role_id, full_name, outlet_id, is_active) VALUES (?, ?, 1, 'Administrator', 1, 1)",
            ('admin', password_hash)
        )
        
        # Insert default tax
        print("➕ Inserting default tax (PPN 10%)...")
        conn.execute("INSERT INTO taxes (name, rate, auto_apply) VALUES ('PPN', 10.0, 1)")
        
        conn.commit()
        conn.close()
        
        print(f"✅ Database created successfully at: {db_path}")
        print(f"🔑 Default admin user: admin / admin123")
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

if __name__ == '__main__':
    create_database()
