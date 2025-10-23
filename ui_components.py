from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QListWidget, QPushButton, QStackedLayout)
from PyQt6.QtCore import pyqtSignal

class MainUI(QMainWindow):
    paste_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('ClipMate')

        self.central_container = QWidget()
        self.setCentralWidget(self.central_container)

        self.stacked_layout = QStackedLayout(self.central_container)

        self.main_widget = QWidget()
        self.settings_widget = QWidget()

        self.stacked_layout.addWidget(self.main_widget)
        self.stacked_layout.addWidget(self.settings_widget)

        self.init_main_ui()
        self.init_settings_ui()

    def init_main_ui(self):
        layout = QVBoxLayout(self.main_widget)
        layout.addWidget(QLabel('Главное окно ClipMate'))

        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.history_list)

    def init_settings_ui(self):
        layout = QVBoxLayout(self.settings_widget)
        layout.addWidget(QLabel('Настройки ClipMate'))

    def on_item_double_clicked(self, item):
        text = item.text()
        self.paste_requested.emit(text)

    def update_history_list(self, history):
        self.history_list.clear()
        for i, text in enumerate(history, 1):
            display_text = text[:50] + '...' if len(text) > 50 else text
            self.history_list.addItem(f'{i}. {display_text}')

    def show_main_window(self):
        self.stacked_layout.setCurrentIndex(0)
        self.show()
        self.raise_()
        self.activateWindow()

    def show_settings_window(self):
        self.stacked_layout.setCurrentIndex(1)
        self.show()
        self.raise_()
        self.activateWindow()