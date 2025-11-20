from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QSpinBox, QFormLayout, QLineEdit, QPushButton)
from PyQt6.QtCore import pyqtSignal


class SettingsUI(QMainWindow):
    def __init__(self, settings_manager):
        super().__init__()
        self.settings = settings_manager
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(150, 150, 400, 150)
        self.setWindowTitle('Настройки ClipMate')

        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)

        form_layout = QFormLayout()

        self.history_size = QSpinBox()
        self.history_size.setRange(1, 100)
        self.history_size.setValue(self.settings.get('max_history_size'))
        self.history_size.valueChanged.connect(
            lambda value: self.settings.set('max_history_size', value)
        )
        form_layout.addRow('Максимальный размер истории:', self.history_size)

        hotkey_layout = QHBoxLayout()
        self.hotkey_edit = QLineEdit()
        self.hotkey_edit.setText(self.settings.get('global_hotkey'))

        hotkey_btn = QPushButton('Принять')
        hotkey_btn.clicked.connect(lambda: self.update_hotkey_edit(self.hotkey_edit.text()))

        hotkey_layout.addWidget(QLabel('Горячая клавиша:'))
        hotkey_layout.addWidget(self.hotkey_edit)
        hotkey_layout.addWidget(hotkey_btn)

        form_layout.addRow(hotkey_layout)
        layout.addLayout(form_layout)

    def update_hotkey_edit(self, text):
        self.settings.set('global_hotkey', text)

    def closeEvent(self, event):
        event.ignore()
        self.hide()