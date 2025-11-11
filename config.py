# Configuration file for POS Minimarket
import os
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent

# Database configuration
DB_PATH = BASE_DIR / 'minimarket.sqlite3'
DB_URI = f'sqlite:///{DB_PATH}'

# Telegram bot configuration (set via environment or edit here)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# Printer configuration
PRINTER_ENABLED = False  # Set to True when printer is configured
PRINTER_TYPE = 'usb'  # or 'serial', 'network'
PRINTER_DEVICE = None  # e.g., '/dev/usb/lp0' or COM port on Windows

# Business settings
CURRENCY_SYMBOL = 'Rp'
CURRENCY_DECIMAL_PLACES = 0  # Indonesian Rupiah typically has no decimals
STORE_CENTS = True  # We store amounts as integer cents/smallest unit

# Tax settings
DEFAULT_TAX_RATE = 10.0  # PPN 10%
AUTO_APPLY_TAX = True

# Low stock threshold (default)
LOW_STOCK_THRESHOLD = 10

# Session / Security
SESSION_TIMEOUT_MINUTES = 120  # Auto-logout after inactivity

# Application info
APP_NAME = 'POS Minimarket'
APP_VERSION = '0.1.0'
