# -*- coding: utf-8 -*-
"""
db_manager.py - Database connection and session management
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import config

# Base class for ORM models
Base = declarative_base()

# Create engine with foreign key support for SQLite
engine = create_engine(
    config.DB_URI,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
    echo=False  # Set to True for SQL debug logging
)

# Enable foreign key constraints for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_session():
    """Get a new database session"""
    return SessionLocal()

def init_db():
    """Initialize database tables (alternative to create_db.py)"""
    Base.metadata.create_all(bind=engine)
