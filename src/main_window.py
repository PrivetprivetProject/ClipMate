from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QTabWidget)
from PyQt6.QtCore import pyqtSignal
from src.history_tab import HistoryTabWidget

class MainUI(QMainWindow):
    paste_requested = pyqtSignal(str)
    show_settings = pyqtSignal()
    clear_history_requested = pyqtSignal()
    clear_pinned_history_requested = pyqtSignal()
    filter_text_changed = pyqtSignal(str)
    pin_current_requested = pyqtSignal()
    remove_from_pinned_requested = pyqtSignal(str)

    def __init__(self, settings_manager, clipboard_manager):
        super().__init__()
        self.settings = settings_manager
        self.clipboard = clipboard_manager
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

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        self.main_tab = HistoryTabWidget('main')
        self.main_tab.paste_requested.connect(self.paste_requested.emit)
        self.tab_widget.addTab(self.main_tab, 'Главная')

        self.pin_tab = HistoryTabWidget('pin')
        self.pin_tab.paste_requested.connect(self.paste_requested.emit)
        self.tab_widget.addTab(self.pin_tab, 'Избранное')



        toolbar = self.addToolBar('Действия')
        add_action = toolbar.addAction('Добавить вкладку')
        add_action.triggered.connect(self.add_new_tab)

        pin_action = toolbar.addAction('Закрепить')
        pin_action.triggered.connect(self.pin_current_requested)

        unpin_action = toolbar.addAction('Открепить')
        unpin_action.triggered.connect(self.unpin_selected_item)
        self.tab_widget.setCornerWidget(toolbar)

        layout.addWidget(self.tab_widget)

    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('Файл')

        settings_action = file_menu.addAction('Настройки')
        settings_action.triggered.connect(self.show_settings.emit)

        file_menu.addSeparator()

        clear_action = file_menu.addAction('Очистить историю')
        clear_action.triggered.connect(self.clear_history_requested.emit)

        clear_pin_action = file_menu.addAction('Очистить закреплённую историю')
        clear_pin_action.triggered.connect(self.clear_pinned_history_requested)

        file_menu.addSeparator()

        exit_action = file_menu.addAction('Выход')
        exit_action.triggered.connect(quit)

        edit_menu = menubar.addMenu('Правка')
        help_menu = menubar.addMenu('Справка')
        about_action = help_menu.addAction('О программе')

    def add_new_tab(self):
        tab_count = self.tab_widget.count()
        empty_tab = HistoryTabWidget('empty')
        self.tab_widget.addTab(empty_tab, f'Вкладка {tab_count+1}')

    def close_tab(self, index):
        self.tab_widget.removeTab(index)

    def show_initial_history(self):
        self.main_tab.update_history(self.settings.get_history())
        self.pin_tab.update_history(self.settings.get_pinned_history())

    def update_history_list(self, history):
        self.main_tab.update_history(history)

    def update_pinned_history(self, pinned_history):
        self.pin_tab.update_history(pinned_history)

    def get_selected_text(self):
        current_tab = self.tab_widget.currentWidget()
        if hasattr(current_tab, 'tab_type'):
            if current_tab.tab_type == 'main' and hasattr(current_tab, 'history_list'):
                selected = current_tab.history_list.selectedItems()
                if selected:
                    return current_tab.get_item_text(selected[0])
            elif current_tab.tab_type == 'pin' and hasattr(current_tab, 'pinned_history_list'):
                selected = current_tab.pinned_history_list.selectedItems()
                if selected:
                    return current_tab.get_item_text(selected[0])
        return None

    def pin_selected_item(self):
        selected_text = self.get_selected_text()
        if selected_text:
            self.clipboard.pin_selected_text(selected_text)
        else:
            self.clipboard.pin_current_item()

    def unpin_selected_item(self):
        selected_text = self.get_selected_text()
        if selected_text:
            self.remove_from_pinned_requested.emit(selected_text)

    def closeEvent(self, event):
        event.ignore()
        self.hide()