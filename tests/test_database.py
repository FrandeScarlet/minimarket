# -*- coding: utf-8 -*-
"""
test_database.py - Basic database connection tests
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.db_manager import get_session, engine
from src.models import Role, User, Product
import config

def test_database_exists():
    """Test that database file exists"""
    assert config.DB_PATH.exists(), "Database file not found. Run create_db.py first."

def test_database_connection():
    """Test that we can connect to database"""
    session = get_session()
    assert session is not None
    session.close()

def test_roles_table():
    """Test that roles table has default data"""
    session = get_session()
    roles = session.query(Role).all()
    assert len(roles) >= 3, "Should have at least 3 default roles"
    role_names = [r.name for r in roles]
    assert 'admin' in role_names
    assert 'kasir' in role_names
    assert 'executive' in role_names
    session.close()

def test_admin_user_exists():
    """Test that default admin user exists"""
    session = get_session()
    admin = session.query(User).filter_by(username='admin').first()
    assert admin is not None, "Default admin user not found"
    assert admin.role.name == 'admin'
    assert admin.is_active == True
    session.close()

# Placeholder for more tests
# TODO: Add tests for:
# - User authentication
# - Product CRUD
# - Transaction processing
# - Stock movements
# - Payment processing
# - Report generation
