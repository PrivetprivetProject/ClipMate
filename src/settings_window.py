from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QSpinBox, QFormLayout, QLineEdit, QPushButton, QGroupBox)
from PyQt6.QtCore import pyqtSignal


class SettingsUI(QMainWindow):
    def __init__(self, settings_manager):
        super().__init__()
        self.settings = settings_manager
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(150, 150, 400, 250)
        self.setWindowTitle('Настройки ClipMate')

        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)

        text_group = QGroupBox('Настройки текста')
        text_layout = QFormLayout(text_group)

        self.history_size = QSpinBox()
        self.history_size.setRange(1, 100)
        self.history_size.setValue(self.settings.get('max_history_size'))
        self.history_size.valueChanged.connect(
            lambda value: self.settings.set('max_history_size', value)
        )
        text_layout.addRow('Максимальный размер истории:', self.history_size)

        image_group = QGroupBox('Настройки изображений')
        image_layout = QFormLayout(image_group)

        self.image_size = QSpinBox()
        self.image_size.setRange(1, 20)
        self.image_size.setValue(self.settings.get('max_images_size', 10))
        self.image_size.valueChanged.connect(
            lambda value: self.settings.set('max_images_size', value)
        )
        image_layout.addRow('Максимум изображений:', self.image_size)

        hotkey_group = QGroupBox('Горячие клавиши')
        hotkey_layout = QHBoxLayout(hotkey_group)
        self.hotkey_edit = QLineEdit()
        self.hotkey_edit.setText(self.settings.get('global_hotkey'))

        hotkey_btn = QPushButton('Применить')
        hotkey_btn.clicked.connect(lambda: self.update_hotkey_edit(self.hotkey_edit.text()))

        hotkey_layout.addWidget(QLabel('Горячая клавиша:'))
        hotkey_layout.addWidget(self.hotkey_edit)
        hotkey_layout.addWidget(hotkey_btn)

        layout.addWidget(text_group)
        layout.addWidget(image_group)
        layout.addWidget(hotkey_group)

    def update_hotkey_edit(self, text):
        self.settings.set('global_hotkey', text)

    def closeEvent(self, event):
        event.ignore()
        self.hide()