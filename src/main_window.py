from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QTabWidget, QInputDialog, QMessageBox)
from PyQt6.QtCore import pyqtSignal, QTimer, QEvent
from src.history_tab import HistoryTabWidget
from src.image_tab import ImageTabWidget
from src.editable_tab import EditableTabWidget


class MainUI(QMainWindow):
    paste_requested = pyqtSignal(str)
    paste_image_requested = pyqtSignal(str)
    show_settings = pyqtSignal()
    clear_history_requested = pyqtSignal()
    clear_pinned_history_requested = pyqtSignal()
    clear_images_requested = pyqtSignal()
    filter_text_changed = pyqtSignal(str)
    pin_current_requested = pyqtSignal()
    remove_from_pinned_requested = pyqtSignal(str)
    remove_image_requested = pyqtSignal(str)

    def __init__(self, settings_manager, clipboard_manager):
        super().__init__()
        self.settings = settings_manager
        self.clipboard = clipboard_manager
        self.setup_ui()
        self.load_saved_tabs()
        self.restore_tabs_order()
        self.show_initial_history()

    def setup_ui(self):
        self.setGeometry(100, 100, 600, 600)
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
        self.tab_widget.tabBarDoubleClicked.connect(self.rename_tab)

        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self.save_tabs_order)
        self.tab_widget.currentChanged.connect(lambda: self.save_timer.start(500))

        self.main_tab = HistoryTabWidget('main')
        self.main_tab.paste_requested.connect(self.paste_requested.emit)

        self.images_tab = ImageTabWidget()
        self.images_tab.paste_requested.connect(self.paste_image_requested.emit)
        self.images_tab.remove_requested.connect(self.remove_image_requested.emit)

        self.pin_tab = HistoryTabWidget('pin')
        self.pin_tab.paste_requested.connect(self.paste_requested.emit)

        self.tab_widget_dict = {
            'Главная': self.main_tab,
            'Изображения': self.images_tab,
            'Избранное': self.pin_tab
        }

        layout.addWidget(self.tab_widget)

    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('Файл')

        settings_action = file_menu.addAction('Настройки')
        settings_action.triggered.connect(self.show_settings.emit)

        file_menu.addSeparator()

        clear_action = file_menu.addAction('Очистить историю')
        clear_action.triggered.connect(self.clear_history_requested.emit)

        clear_pin_action = file_menu.addAction('Очистить избранное')
        clear_pin_action.triggered.connect(self.clear_pinned_history_requested.emit)

        clear_images_action = file_menu.addAction('Очистить историю изображений')
        clear_images_action.triggered.connect(self.clear_images_requested.emit)

        file_menu.addSeparator()

        exit_action = file_menu.addAction('Выход')
        exit_action.triggered.connect(quit)

        edit_menu = menubar.addMenu('Правка')
        help_menu = menubar.addMenu('Справка')
        about_action = help_menu.addAction('О программе')

        tools_menu = menubar.addMenu('Инструменты')

        add_action = tools_menu.addAction('Добавить вкладку')
        add_action.triggered.connect(self.add_new_editable_tab)

        pin_action = tools_menu.addAction('Закрепить')
        pin_action.triggered.connect(self.pin_current_requested)

        unpin_action = tools_menu.addAction('Открепить')
        unpin_action.triggered.connect(self.unpin_selected_item)

    def restore_tabs_order(self):
        tabs_order = self.settings.get('tabs_order', ['Главная', 'Изображения', 'Избранное'])
        for tab_name, widget in self.tab_widget_dict.items():
            found = False
            for i in range(self.tab_widget.count()):
                if self.tab_widget.tabText(i) == tab_name:
                    found = True
                    break
            if not found:
                self.tab_widget.addTab(widget, tab_name)

        self.sort_tabs_according_to_order(tabs_order)

    def sort_tabs_according_to_order(self, tabs_order):
        position_dict = {}
        for i, tab_name in enumerate(tabs_order):
            position_dict[tab_name] = i

        tabs_info = []
        for i in range(self.tab_widget.count()):
            tab_name = self.tab_widget.tabText(i)
            widget = self.tab_widget.widget(i)
            position = position_dict.get(tab_name, len(tabs_order) + i)
            tabs_info.append((position, tab_name, widget, i))

        tabs_info.sort(key=lambda x: x[0])

        widgets_to_add = []
        for position, tab_name, widget, old_index in tabs_info:
            widgets_to_add.append((tab_name, widget))

        while self.tab_widget.count() > 0:
            self.tab_widget.removeTab(0)

        for tab_name, widget in widgets_to_add:
            self.tab_widget.addTab(widget, tab_name)

    def add_saved_custom_tabs(self, tabs_order):
        existing_tabs = []
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if isinstance(widget, EditableTabWidget):
                existing_tabs.append(widget.get_tab_name())

        for tab_name in self.settings.get('tabs_data', {}).keys():
            if tab_name not in existing_tabs and tab_name not in tabs_order:
                editable_tab = EditableTabWidget(tab_name, self.settings)
                editable_tab.paste_requested.connect(self.paste_requested.emit)
                self.tab_widget.addTab(editable_tab, tab_name)

    def save_tabs_order(self):
        tabs_order = []
        for i in range(self.tab_widget.count()):
            tab_name = self.tab_widget.tabText(i)
            tabs_order.append(tab_name)
        self.settings.set('tabs_order', tabs_order)

    def add_new_editable_tab(self):
        existing_names = []
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if isinstance(widget, EditableTabWidget):
                existing_names.append(widget.get_tab_name())

        tab_number = 1
        while f'Новая вкладка {tab_number}' in existing_names:
            tab_number += 1

        tab_name = f'Новая вкладка {tab_number}'

        editable_tab = EditableTabWidget(tab_name, self.settings)
        editable_tab.paste_requested.connect(self.paste_requested.emit)

        index = self.tab_widget.addTab(editable_tab, tab_name)
        self.tab_widget.setCurrentIndex(index)
        editable_tab.save_content()

        data = self.settings.get('tabs_data', {}).copy()
        self.settings.set('tabs_data', data)

        self.save_tabs_order()

    def rename_tab(self, index):
        widget = self.tab_widget.widget(index)

        if not isinstance(widget, EditableTabWidget):
            return

        current_name = widget.get_tab_name()

        new_name, ok = QInputDialog.getText(
            self,
            'Переименовать вкладку',
            'Введите новое имя для вкладки:',
            text=current_name
        )

        if not ok or not new_name or new_name == current_name:
            return

        for i in range(self.tab_widget.count()):
            w = self.tab_widget.widget(i)
            if isinstance(w, EditableTabWidget) and i != index and w.get_tab_name() == new_name:
                QMessageBox.warning(self, 'Ошибка', f'Вкладка с именем "{new_name}" уже существует!')
                return

        widget.set_tab_name(new_name)
        self.tab_widget.setTabText(index, new_name)
        self.save_tabs_order()

    def close_tab(self, index):
        w = self.tab_widget.widget(index)

        if w in (self.main_tab, self.images_tab, self.pin_tab):
            return

        self.tab_widget.removeTab(index)

        if isinstance(w, EditableTabWidget):
            name = w.get_tab_name()
            data = self.settings.get('tabs_data', {}).copy()
            if name in data:
                data.pop(name)
                self.settings.set('tabs_data', data)

        self.save_tabs_order()

    def show_initial_history(self):
        self.main_tab.update_history(self.settings.get('history'))
        self.pin_tab.update_history(self.settings.get('pinned_history'))
        self.images_tab.update_images(self.settings.get('images'))

    def load_saved_tabs(self):
        tabs_data = self.settings.get('tabs_data', {})

        existing_tab_names = []
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if isinstance(widget, EditableTabWidget):
                existing_tab_names.append(widget.get_tab_name())

        for tab_name in list(tabs_data.keys()):
            if tab_name not in ['Главная', 'Изображения', 'Избранное']:
                if tab_name not in existing_tab_names:
                    editable_tab = EditableTabWidget(tab_name, self.settings)
                    editable_tab.paste_requested.connect(self.paste_requested.emit)
                    self.tab_widget.addTab(editable_tab, tab_name)

    def update_history_list(self, history):
        self.main_tab.update_history(history)

    def update_pinned_history(self, pinned_history):
        self.pin_tab.update_history(pinned_history)

    def get_selected_text(self):
        current_tab = self.tab_widget.currentWidget()

        if isinstance(current_tab, EditableTabWidget):
            return current_tab.text_edit.toPlainText()

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
        self.save_tabs_order()
        event.ignore()
        self.hide()

    def update_images_list(self, images):
        self.images_tab.update_images(images)