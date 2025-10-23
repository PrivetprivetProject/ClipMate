from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction, QPixmap
from PyQt6.QtCore import QObject, pyqtSignal, Qt

class TrayManager(QObject):
    show_main_requested = pyqtSignal()
    show_settings_requested = pyqtSignal()
    hide_requested = pyqtSignal()
    quit_requested = pyqtSignal()

    def __init__(self, main_ui, clipboard_manager, settings_manager):
        super().__init__()
        self.main_ui = main_ui
        self.clipboard_manager = clipboard_manager
        self.settings_manager = settings_manager

        self.setup_tray()

    def setup_tray(self):
        self.tray = QSystemTrayIcon()
        self.create_tray_icon()
        self.create_tray_menu()
        self.tray.show()

        self.tray.activated.connect(self.on_tray_activated)

    def create_tray_icon(self):
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.GlobalColor.lightGray)
        self.tray.setIcon(QIcon(pixmap))

    def create_tray_menu(self):
        tray_menu = QMenu()

        show_action = QAction('Показать', self.main_ui)
        show_action.triggered.connect(self.show_main_requested.emit)
        tray_menu.addAction(show_action)

        hide_action = QAction('Скрыть', self.main_ui)
        hide_action.triggered.connect(self.hide_requested.emit)
        tray_menu.addAction(hide_action)

        tray_menu.addSeparator()

        self.add_clipboard(tray_menu)

        tray_menu.addSeparator()

        settings_action = QAction('Настройки', self.main_ui)
        settings_action.triggered.connect(self.show_settings_requested.emit)
        tray_menu.addAction(settings_action)

        tray_menu.addSeparator()

        quit_action = QAction('Выход', self.main_ui)
        quit_action.triggered.connect(self.quit_requested.emit)
        tray_menu.addAction(quit_action)

        self.tray.setContextMenu(tray_menu)

    def add_clipboard(self, menu):
        clear_history_action = QAction('Очистить историю', self.main_ui)
        clear_history_action.triggered.connect(self.clipboard_manager.clear_history)
        menu.addAction(clear_history_action)

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_main_requested.emit()