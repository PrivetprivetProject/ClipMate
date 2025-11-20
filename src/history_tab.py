from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget
from PyQt6.QtCore import pyqtSignal


class HistoryTabWidget(QWidget):
    paste_requested = pyqtSignal(str)

    def __init__(self, tab_type='main'):
        super().__init__()
        self.tab_type = tab_type
        self.full_history = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        if self.tab_type == 'main':
            self.setup_main_tab(layout)
        elif self.tab_type == 'pin':
            self.setup_pin_tab(layout)
        else:
            self.setup_empty_tab(layout)

    def setup_main_tab(self, layout):
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(
            lambda item: self.paste_requested.emit(self.get_item_text(item))
        )
        layout.addWidget(self.history_list)

        self.full_history = []

    def setup_pin_tab(self, layout):
        self.pinned_history_list = QListWidget()
        self.pinned_history_list.itemDoubleClicked.connect(
            lambda item: self.paste_requested.emit(self.get_item_text(item))
        )
        layout.addWidget(self.pinned_history_list)

        self.full_history = []

    def setup_empty_tab(self, layout):
        layout.addWidget(QLabel('Пустая вкладка'))

    def get_item_text(self, item):
        if hasattr(self, 'full_history') and self.full_history:
            if hasattr(self, 'history_list') and item.listWidget() == self.history_list:
                return self.full_history[self.history_list.row(item)]
            elif hasattr(self, 'pinned_history_list') and item.listWidget() == self.pinned_history_list:
                return self.full_history[self.pinned_history_list.row(item)]
        return ''

    def update_history(self, history):
        self.full_history = history.copy()
        if self.tab_type == 'main' and hasattr(self, 'history_list'):
            self.history_list.clear()
            for i, text in enumerate(history, 1):
                display_text = text[:50] + '...' if len(text) > 50 else text
                self.history_list.addItem(f'{i}. {display_text}')

        elif self.tab_type == 'pin' and hasattr(self, 'pinned_history_list'):
            self.pinned_history_list.clear()
            for i, text in enumerate(history, 1):
                display_text = text[:50] + '...' if len(text) > 50 else text
                self.pinned_history_list.addItem(f'{i}. {display_text}')