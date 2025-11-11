#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
main.py - Entry point for POS Minimarket application
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import config

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f"{config.APP_NAME} v{config.APP_VERSION}")
        self.setMinimumSize(1024, 768)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title
        title = QLabel(config.APP_NAME)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Version
        version = QLabel(f"Version {config.APP_VERSION}")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)
        
        layout.addSpacing(40)
        
        # Status
        db_status = "✅ Database connected" if config.DB_PATH.exists() else "❌ Database not found"
        status_label = QLabel(db_status)
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(status_label)
        
        if not config.DB_PATH.exists():
            help_text = QLabel("Run 'python create_db.py' to create the database first.")
            help_text.setStyleSheet("color: red;")
            help_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(help_text)
        
        layout.addSpacing(40)
        
        # Login button placeholder
        login_btn = QPushButton("Login")
        login_btn.setMinimumSize(200, 50)
        login_btn.clicked.connect(self.show_login)
        layout.addWidget(login_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Exit button
        exit_btn = QPushButton("Exit")
        exit_btn.setMinimumSize(200, 50)
        exit_btn.clicked.connect(self.close)
        layout.addWidget(exit_btn, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def show_login(self):
        """Show login dialog (placeholder)"""
        if not config.DB_PATH.exists():
            QMessageBox.critical(self, "Error", "Database not found! Please run 'python create_db.py' first.")
            return
        
        QMessageBox.information(
            self,
            "Login",
            "Login screen akan diimplementasikan di modul berikutnya.\n\n"
            "Default credentials:\nUsername: admin\nPassword: admin123"
        )

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application style (optional)
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
