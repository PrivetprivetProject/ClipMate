from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QTabWidget, QInputDialog, QMessageBox)
from PyQt6.QtCore import pyqtSignal, QTimer, Qt

from src.history_tab import HistoryTabWidget
from src.image_tab import ImageTabWidget
from src.editable_tab import EditableTabWidget
from src.custom_title_bar import CustomTitleBar
from src.title_bar_styles import get_title_bar_styles


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
    quit_requested = pyqtSignal()

    def __init__(self, settings_manager, clipboard_manager):
        super().__init__()
        self.settings = settings_manager
        self.clipboard = clipboard_manager

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.setup_ui()
        self.load_saved_tabs()
        self.restore_tabs_order()
        self.show_initial_history()

        self.settings.settings_changed.connect(self.on_settings_changed)
        self.connect_tab_signals()

    def setup_ui(self):
        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle('ClipMate')
        self.setObjectName('main_window')

        main_container = QWidget()
        main_container.setObjectName('main_container')
        self.setCentralWidget(main_container)

        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.title_bar = CustomTitleBar(self)
        self.title_bar.set_title('ClipMate')
        self.title_bar.minimize_clicked.connect(self.showMinimized)
        self.title_bar.maximize_clicked.connect(self.toggle_maximized)
        self.title_bar.close_clicked.connect(self.close)

        self.title_bar.show_settings_clicked.connect(self.show_settings.emit)
        self.title_bar.clear_text_history_clicked.connect(self.clear_history_requested.emit)
        self.title_bar.clear_image_history_clicked.connect(self.clear_images_requested.emit)
        self.title_bar.clear_all_history_clicked.connect(self.clear_all_history)
        self.title_bar.quit_app_clicked.connect(self.requested_quit)
        self.title_bar.about_clicked.connect(self.show_about)
        self.title_bar.pin_item_clicked.connect(self.pin_current_requested)
        self.title_bar.unpin_item_clicked.connect(self.unpin_selected_item)
        self.title_bar.add_tab_clicked.connect(self.add_new_editable_tab)

        main_layout.addWidget(self.title_bar)

        content_container = QWidget()
        content_container.setObjectName('content_container')
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(10, 10, 10, 10)

        self.setMenuBar(None)

        history_label = QLabel('История буфера обмена:')
        history_label.setProperty('title', 'tab')
        content_layout.addWidget(history_label)

        self.search_edit = QLineEdit()
        self.search_edit.textChanged.connect(
            lambda item: self.filter_text_changed.emit(self.search_edit.text())
        )
        content_layout.addWidget(self.search_edit)

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

        content_layout.addWidget(self.tab_widget)

        main_layout.addWidget(content_container)
        self.apply_title_bar_style()

    def show_about(self):
        from PyQt6.QtWidgets import QMessageBox

        about_text = (
            "ClipMate - Менеджер буфера обмена\n\n"
            "Версия: 0.1\n"
            "Создано с использованием PyQt6\n\n"
            "Функции:\n"
            "• История текстового буфера обмена\n"
            "• История изображений\n"
            "• Закрепленные элементы\n"
            "• Настраиваемые вкладки\n"
            "• Тематическое оформление\n\n"
            "Все права защищены"
        )

        QMessageBox.about(self, "О программе", about_text)

    def connect_tab_signals(self):
        self.main_tab.context_menu_requested.connect(self.handle_context_menu_action)
        self.pin_tab.context_menu_requested.connect(self.handle_context_menu_action)

    def handle_context_menu_action(self, text, action_type):
        if action_type == 'pin':
            self.clipboard.pin_selected_text(text)
        elif action_type == 'unpin':
            self.remove_from_pinned_requested.emit(text)
        elif action_type == 'delete':
            self.delete_selected_text(text)

    def delete_selected_text(self, text):
        current_tab = self.tab_widget.currentWidget()
        if current_tab == self.main_tab:
            self.remove_from_history(text)
        elif current_tab == self.pin_tab:
            self.remove_from_pinned_requested.emit(text)

    def remove_from_history(self, text):
        history = self.settings.get('history', [])
        if text in history:
            new_history = [item for item in history if item != text]
            self.settings.set('history', new_history)
            self.main_tab.update_history(new_history)
            self.clipboard.history_updated.emit(new_history)

    def clear_all_history(self):
        from PyQt6.QtWidgets import QMessageBox

        reply = QMessageBox.question(
            self, 'Удалить всю историю',
            'Вы действительно хотите удалить ВСЮ историю?\n'
            'Это действие нельзя отменить.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.clear_history_requested.emit()
            self.clear_images_requested.emit()
            self.clear_pinned_history_requested.emit()

    def toggle_maximized(self):
        if self.isMaximized():
            self.showNormal()
            self.title_bar.set_maximized(False)

        else:
            self.showMaximized()
            self.title_bar.set_maximized(True)

    def apply_title_bar_style(self):
        from src.styles import THEMES
        current_theme = self.settings.get('current_theme', 'light')
        theme = THEMES.get(current_theme, THEMES['light'])

        styles = get_title_bar_styles(theme)
        self.title_bar.setStyleSheet(styles)

        self.title_bar.setProperty('theme', current_theme)
        self.title_bar.style().unpolish(self.title_bar)
        self.title_bar.style().polish(self.title_bar)

    def update_menu_style(self, theme_name):
        from src.styles import THEMES
        theme = THEMES.get(theme_name, THEMES["light"])

        menu_style = f"""
            QMenu {{
                background-color: {theme["secondary_background"]};
                color: {theme["text"]};
                border: 1px solid {theme["border"]};
                border-radius: 4px;
                padding: 5px;
            }}
            QMenu::item {{
                padding: 6px 20px;
                border-radius: 3px;
                color: {theme["text"]};
            }}
            QMenu::item:selected {{
                background-color: {theme["accent"]};
                color: white;
            }}
            QMenu::separator {{
                height: 1px;
                background-color: {theme["border"]};
                margin: 5px 10px;
            }}
        """

        if hasattr(self, 'context_menu'):
            self.context_menu.setStyleSheet(menu_style)

    def on_settings_changed(self, key, value):
        if key == 'current_theme':
            self.apply_title_bar_style()
            self.update_menu_style(value)

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

    def requested_quit(self):
        self.quit_requested.emit()

    def update_images_list(self, images):
        self.images_tab.update_images(images)