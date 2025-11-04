from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QListWidget, QSpinBox, QFormLayout, QLineEdit, QPushButton)
from PyQt6.QtCore import pyqtSignal


class MainUI(QMainWindow):
    paste_requested = pyqtSignal(str)
    show_settings = pyqtSignal()
    clear_history_requested = pyqtSignal()
    filter_text_changed = pyqtSignal(str)

    def __init__(self, settings_manager):
        super().__init__()
        self.settings = settings_manager
        self.setup_ui()
        self.show_initial_history()

    def setup_ui(self):
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('ClipMate')

        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)

        self.create_menu()

        layout.addWidget(QLabel('История буфера обмена:'))

        self.search_edit = QLineEdit()
        self.search_edit.textChanged.connect(
            lambda item: self.filter_text_changed.emit(self.search_edit.text())
        )
        layout.addWidget(self.search_edit)

        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(
            lambda item: self.paste_requested.emit(self.get_item_text(item))
        )
        layout.addWidget(self.history_list)

    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('Файл')

        settings_action = file_menu.addAction('Настройки')
        settings_action.triggered.connect(self.show_settings.emit)

        file_menu.addSeparator()

        clear_action = file_menu.addAction('Очистить историю')
        clear_action.triggered.connect(self.clear_history_requested.emit)

        file_menu.addSeparator()

        exit_action = file_menu.addAction('Выход')
        exit_action.triggered.connect(quit)

        edit_menu = menubar.addMenu('Правка')
        help_menu = menubar.addMenu('Справка')
        about_action = help_menu.addAction('О программе')

    def get_item_text(self, item):
        return self.full_history[self.history_list.row(item)]

    def show_initial_history(self):
        self.update_history_list(self.settings.get_history())

    def update_history_list(self, history):
        self.history_list.clear()
        self.full_history = history.copy()
        for i, text in enumerate(history, 1):
            display_text = text[:50] + '...' if len(text) > 50 else text
            self.history_list.addItem(f'{i}. {display_text}')

    def closeEvent(self, event):
        event.ignore()
        self.hide()


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