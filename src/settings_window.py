from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QSpinBox, QFormLayout, QLineEdit, QPushButton, QGroupBox,
                             QComboBox)
from PyQt6.QtCore import Qt
from src.styles import AVAILABLE_THEMES
from src.custom_title_bar import CustomTitleBar
from src.title_bar_styles import get_title_bar_styles


class SettingsUI(QMainWindow):
    def __init__(self, settings_manager):
        super().__init__()
        self.settings = settings_manager
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setup_ui()
        self.settings.settings_changed.connect(self.on_settings_changed)

    def setup_ui(self):
        self.setGeometry(150, 150, 400, 250)
        self.setWindowTitle('Настройки ClipMate')
        self.setObjectName('settings_window')

        main_container = QWidget()
        main_container.setObjectName('settings_container')
        self.setCentralWidget(main_container)

        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.title_bar = CustomTitleBar(self)
        self.title_bar.set_title('Настройки ClipMate')
        self.title_bar.minimize_clicked.connect(self.showMinimized)
        self.title_bar.maximize_clicked.connect(self.toggle_maximized)
        self.title_bar.close_clicked.connect(self.close)

        self.title_bar.set_menu_visible(False)

        main_layout.addWidget(self.title_bar)

        content_container = QWidget()
        content_container.setObjectName('settings_content')
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(15, 15, 15, 15)

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

        theme_group = QGroupBox('Настройки темы')
        theme_layout = QFormLayout(theme_group)

        self.theme_combo = QComboBox()

        for theme_id, theme_name in AVAILABLE_THEMES:
            self.theme_combo.addItem(theme_name, theme_id)

        current_theme = self.settings.get('current_theme', 'light')
        index = self.theme_combo.findData(current_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)

        self.theme_combo.currentIndexChanged.connect(self.on_theme_changed)

        theme_layout.addRow('Тема приложения:', self.theme_combo)

        content_layout.addWidget(text_group)
        content_layout.addWidget(image_group)
        content_layout.addWidget(hotkey_group)
        content_layout.addWidget(theme_group)

        main_layout.addWidget(content_container)

        self.apply_title_bar_style()

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

    def on_settings_changed(self, key, value):
        if key == 'current_theme':
            self.apply_title_bar_style()

    def update_window_geometry(self):
        current_size = self.size()
        self.centralWidget().updateGeometry()
        self.layout().invalidate()
        self.layout().activate()
        self.resize(current_size)

    def on_theme_changed(self, index):
        if index >= 0:
            theme_id = self.theme_combo.itemData(index)
            self.settings.set('current_theme', theme_id)

    def update_hotkey_edit(self, text):
        self.settings.set('global_hotkey', text)

    def closeEvent(self, event):
        event.ignore()
        self.hide()