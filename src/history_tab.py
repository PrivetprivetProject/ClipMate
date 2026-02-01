from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QMenu
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QAction


class HistoryTabWidget(QWidget):
    paste_requested = pyqtSignal(str)
    context_menu_requested = pyqtSignal(str, str)

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
        self.history_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.history_list.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.history_list)

        self.full_history = []
        self.context_menu = None

    def setup_pin_tab(self, layout):
        self.pinned_history_list = QListWidget()
        self.pinned_history_list.itemDoubleClicked.connect(
            lambda item: self.paste_requested.emit(self.get_item_text(item))
        )
        self.pinned_history_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.pinned_history_list.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.pinned_history_list)

        self.full_history = []
        self.context_menu = None

    def setup_empty_tab(self, layout):
        layout.addWidget(QLabel('Пустая вкладка'))

    def get_item_text(self, item):
        if hasattr(self, 'full_history') and self.full_history:
            if hasattr(self, 'history_list') and item.listWidget() == self.history_list:
                return self.full_history[self.history_list.row(item)]
            elif hasattr(self, 'pinned_history_list') and item.listWidget() == self.pinned_history_list:
                return self.full_history[self.pinned_history_list.row(item)]
        return ''

    def show_context_menu(self, position):
        if self.tab_type == 'main' and hasattr(self, 'history_list'):
            widget = self.history_list
            items = self.history_list.selectedItems()
        elif self.tab_type == 'pin' and hasattr(self, 'pinned_history_list'):
            widget = self.pinned_history_list
            items = self.pinned_history_list.selectedItems()
        else:
            return

        if not items:
            return

        selected_item = items[0]
        selected_text = self.get_item_text(selected_item)

        if not selected_text:
            return

        self.context_menu = QMenu(self)

        if self.tab_type == 'main':
            pin_action = QAction("Закрепить", self)
            pin_action.triggered.connect(
                lambda: self.context_menu_requested.emit(selected_text, 'pin')
            )
            self.context_menu.addAction(pin_action)

        elif self.tab_type == 'pin':
            unpin_action = QAction("Открепить", self)
            unpin_action.triggered.connect(
                lambda: self.context_menu_requested.emit(selected_text, 'unpin')
            )
            self.context_menu.addAction(unpin_action)

        delete_action = QAction("Удалить", self)
        delete_action.triggered.connect(
            lambda: self.context_menu_requested.emit(selected_text, 'delete')
        )
        self.context_menu.addAction(delete_action)

        self.context_menu.exec(widget.mapToGlobal(position))

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