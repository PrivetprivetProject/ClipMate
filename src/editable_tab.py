import time
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout,
                             QLabel)
from PyQt6.QtCore import pyqtSignal, Qt


class EditableTabWidget(QWidget):
    save_requested = pyqtSignal(str, str)
    paste_requested = pyqtSignal(str)

    def __init__(self, tab_name, settings_manager):
        super().__init__()
        self.tab_name = tab_name
        self.settings = settings_manager
        self.setup_ui()
        self.load_saved_content()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title_label = QLabel(f'Текстовая вкладка: {self.tab_name}')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setProperty('title', 'tab')
        layout.addWidget(title_label)

        self.text_edit = QTextEdit()
        self.text_edit.setObjectName('text_edit')
        self.text_edit.setPlaceholderText('Введите текст здесь...')
        self.text_edit.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.text_edit)

        button_layout = QHBoxLayout()

        self.save_btn = QPushButton('Сохранить')
        self.save_btn.clicked.connect(self.save_content)
        button_layout.addWidget(self.save_btn)

        self.paste_btn = QPushButton('Вставить весь текст')
        self.paste_btn.clicked.connect(self.paste_all_content)
        button_layout.addWidget(self.paste_btn)

        self.clear_btn = QPushButton('Очистить')
        self.clear_btn.clicked.connect(self.clear_content)
        button_layout.addWidget(self.clear_btn)

        layout.addLayout(button_layout)

        self.status_label = QLabel('Сохранено')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.status_label.setStyleSheet('color: green')
        layout.addWidget(self.status_label)

        self.unsaved_changes = False
        self.last_save_time = 0

    def on_text_changed(self):
        self.unsaved_changes = True
        self.status_label.setText('Есть несохранённые изменения')
        self.status_label.setStyleSheet('color: orange')

    def save_content(self):
        content = self.text_edit.toPlainText()
        tabs_data = self.settings.get('tabs_data', {})
        tabs_data[self.tab_name] = content
        self.settings.set('tabs_data', tabs_data)
        self.settings.save_settings()
        self.unsaved_changes = False
        self.last_save_time = time.time()
        self.status_label.setText(f'Сохранено ({time.strftime("%H:%M:%S")})')
        self.status_label.setStyleSheet('color: green')
        return True

    def load_saved_content(self):
        tabs_data = self.settings.get('tabs_data', {})
        if self.tab_name in tabs_data:
            content = tabs_data[self.tab_name]
            self.text_edit.setPlainText(content)
            self.unsaved_changes = False
            self.status_label.setText('Загружено из сохранения')
            self.status_label.setStyleSheet('color: green')

    def paste_all_content(self):
        content = self.text_edit.toPlainText()
        if content:
            self.paste_requested.emit(content)

    def clear_content(self):
        self.text_edit.clear()
        self.unsaved_changes = True
        self.status_label.setText('Текст очищен')
        self.status_label.setStyleSheet('color: orange')

    def get_tab_name(self):
        return self.tab_name

    def set_tab_name(self, new_name):
        if self.tab_name == new_name:
            return

        data = self.settings.get('tabs_data', {}).copy()

        current_text = self.text_edit.toPlainText()

        if self.tab_name in data:
            data.pop(self.tab_name)

        data[new_name] = current_text

        self.settings.set('tabs_data', data)
        self.settings.save_settings()

        self.tab_name = new_name
        self.unsaved_changes = False