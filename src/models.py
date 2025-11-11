# -*- coding: utf-8 -*-
"""
models.py - SQLAlchemy ORM models for POS Minimarket
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db_manager import Base

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    permissions = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    users = relationship('User', back_populates='role')

class Outlet(Base):
    __tablename__ = 'outlets'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(Text)
    phone = Column(String)
    created_at = Column(DateTime, default=func.now())
    
    users = relationship('User', back_populates='outlet')
    transactions = relationship('Transaction', back_populates='outlet')

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    full_name = Column(String)
    email = Column(String)
    phone = Column(String)
    outlet_id = Column(Integer, ForeignKey('outlets.id'))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    last_login = Column(DateTime)
    
    role = relationship('Role', back_populates='users')
    outlet = relationship('Outlet', back_populates='users')
    transactions = relationship('Transaction', back_populates='user')
    shifts = relationship('Shift', back_populates='user')

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    created_at = Column(DateTime, default=func.now())
    
    products = relationship('Product', back_populates='category')

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String, unique=True)
    barcode = Column(String, unique=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    price_cents = Column(Integer, nullable=False)
    cost_cents = Column(Integer)
    alert_stock = Column(Integer, default=0)
    track_stock = Column(Boolean, default=True)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    category = relationship('Category', back_populates='products')
    stocks = relationship('ProductStock', back_populates='product')
    transaction_items = relationship('TransactionItem', back_populates='product')

class ProductStock(Base):
    __tablename__ = 'product_stocks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    outlet_id = Column(Integer, ForeignKey('outlets.id'), nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    product = relationship('Product', back_populates='stocks')

class StockMovement(Base):
    __tablename__ = 'stock_movements'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    outlet_id = Column(Integer, ForeignKey('outlets.id'), nullable=False)
    change_qty = Column(Integer, nullable=False)
    reason = Column(String)
    reference = Column(String)
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=func.now())

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, unique=True, nullable=False)
    outlet_id = Column(Integer, ForeignKey('outlets.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    subtotal_cents = Column(Integer, nullable=False)
    discount_cents = Column(Integer, default=0)
    tax_cents = Column(Integer, default=0)
    total_cents = Column(Integer, nullable=False)
    paid_cents = Column(Integer, default=0)
    change_cents = Column(Integer, default=0)
    status = Column(String, default='completed')
    payment_summary = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    outlet = relationship('Outlet', back_populates='transactions')
    user = relationship('User', back_populates='transactions')
    customer = relationship('Customer', back_populates='transactions')
    items = relationship('TransactionItem', back_populates='transaction')
    payments = relationship('Payment', back_populates='transaction')

class TransactionItem(Base):
    __tablename__ = 'transaction_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'))
    price_cents = Column(Integer, nullable=False)
    qty = Column(Integer, nullable=False)
    discount_cents = Column(Integer, default=0)
    tax_cents = Column(Integer, default=0)
    total_cents = Column(Integer, nullable=False)
    
    transaction = relationship('Transaction', back_populates='items')
    product = relationship('Product', back_populates='transaction_items')

class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    method = Column(String, nullable=False)
    amount_cents = Column(Integer, nullable=False)
    details = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    transaction = relationship('Transaction', back_populates='payments')

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, unique=True)
    name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)
    birthday = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    transactions = relationship('Transaction', back_populates='customer')

class Shift(Base):
    __tablename__ = 'shifts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    outlet_id = Column(Integer, ForeignKey('outlets.id'))
    start_at = Column(DateTime, default=func.now())
    end_at = Column(DateTime)
    starting_cash_cents = Column(Integer, default=0)
    ending_cash_cents = Column(Integer)
    note = Column(Text)
    
    user = relationship('User', back_populates='shifts')

class Discount(Base):
    __tablename__ = 'discounts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    applies_to = Column(String, default='transaction')

class Tax(Base):
    __tablename__ = 'taxes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    rate = Column(Float, nullable=False)
    auto_apply = Column(Boolean, default=True)

class Refund(Base):
    __tablename__ = 'refunds'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    amount_cents = Column(Integer, nullable=False)
    reason = Column(Text)
    processed_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=func.now())
