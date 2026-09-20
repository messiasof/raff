"""
Estilos e tema visual do R.A.F.F
Paleta com bom contraste, amigável e acessível para foco cognitivo.
"""

THEME_STYLESHEET = """
QMainWindow, QDialog, QWidget {
    background-color: #F8F9FA;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
    color: #212529;
}

QLabel {
    font-size: 14px;
    color: #333333;
}

QLabel#titleLabel {
    font-size: 20px;
    font-weight: bold;
    color: #1E3A8A;
    margin-bottom: 10px;
}

QLabel#subtitleLabel {
    font-size: 13px;
    color: #6C757D;
}

QLineEdit, QTextEdit, QTimeEdit, QSpinBox, QComboBox {
    background-color: #FFFFFF;
    border: 2px solid #CED4DA;
    border-radius: 6px;
    padding: 8px;
    font-size: 14px;
    color: #212529;
}

QLineEdit:focus, QTextEdit:focus, QTimeEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 2px solid #3B82F6;
    outline: none;
}

QPushButton {
    background-color: #3B82F6;
    color: #FFFFFF;
    font-weight: bold;
    border: none;
    border-radius: 6px;
    padding: 10px 18px;
    font-size: 14px;
}

QPushButton:hover {
    background-color: #2563EB;
}

QPushButton:pressed {
    background-color: #1D4ED8;
}

QPushButton#secondaryButton {
    background-color: #6C757D;
}
QPushButton#secondaryButton:hover {
    background-color: #5A6268;
}

QPushButton#successButton {
    background-color: #10B981;
}
QPushButton#successButton:hover {
    background-color: #059669;
}

QPushButton#dangerButton {
    background-color: #EF4444;
}
QPushButton#dangerButton:hover {
    background-color: #DC2626;
}

QGroupBox {
    font-weight: bold;
    border: 2px solid #E5E7EB;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 16px;
    background-color: #FFFFFF;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 4px;
    color: #1E3A8A;
}

QProgressBar {
    border: 2px solid #E5E7EB;
    border-radius: 6px;
    text-align: center;
    background-color: #FFFFFF;
    height: 22px;
}

QProgressBar::chunk {
    background-color: #3B82F6;
    border-radius: 4px;
}

QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #CED4DA;
    border-radius: 6px;
    gridline-color: #E5E7EB;
}

QHeaderView::section {
    background-color: #F1F5F9;
    padding: 6px;
    font-weight: bold;
    border: 1px solid #E5E7EB;
}
"""
